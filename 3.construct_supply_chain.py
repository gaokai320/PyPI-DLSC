# import logging

import pandas as pd
import pymongo
from packaging.version import Version
from pymongo import MongoClient

import setting

pypi_db = MongoClient(host="127.0.0.1", port=27017)["dlsc"]
distribution_metadata = pypi_db["distribution_metadata"]
versioned_dependencies = pypi_db["versioned_dependencies"]
supply_chains = MongoClient(host="127.0.0.1", port=27017)["dlsc"]
# LOG_PATH = "log/dl_package_metadata.log"

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# handler = logging.FileHandler(LOG_PATH, "w", "utf-8")
# handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
# logger.addHandler(handler)


def is_pre_dev_release(v):
    try:
        v = Version(v)
        return v.is_prerelease or v.is_devrelease
    except:
        return False


def all_versions(pkg: str) -> list:
    pipeline = [
        {"$match": {"name": pkg}},
        {"$group": {"_id": None, "versions": {"$addToSet": "$version"}}},
    ]
    versions = list(distribution_metadata.aggregate(pipeline=pipeline))
    if versions:
        versions = versions[0]["versions"]
        versions = [v for v in versions if not is_pre_dev_release(v)]
        return sorted(versions, key=Version)
    else:
        return []


def direct_dependents(package: str, versions: list):
    query = {
        "dependency": package,
        "dependency_version": {"$in": versions},
        "extra": False,
    }
    query_results = versioned_dependencies.find(
        query,
        projection={
            "_id": 0,
            "name": 1,
            "version": 1,
            "dependency": 1,
            "dependency_version": 1,
        },
    )
    df = pd.DataFrame(list(query_results))
    if not df.empty:
        df = df[
            ~(
                df["version"].apply(is_pre_dev_release)
                | df["dependency_version"].apply(is_pre_dev_release)
            )
        ]
    return df


def next_layer(packages: list, versions: list):
    res = pd.DataFrame()
    assert len(packages) == len(versions)
    for p, v in zip(packages, versions):
        tmp = direct_dependents(p, v)
        if not tmp.empty:
            res = pd.concat([res, direct_dependents(p, v)])
    return res


def all_layers(packages: list):
    layer = 1
    res = pd.DataFrame()
    versions = []
    tmp = packages
    for p in packages:
        versions.append(all_versions(p))
        res = pd.concat([res, pd.DataFrame({"name": p, "version": all_versions(p)})])
    res.loc[:, "layer"] = layer
    while packages:
        layer = layer + 1
        # logging.info(f"===============Finding layer {layer} packages===============")
        nl = next_layer(packages, versions)
        # logging.info(f"Finding {len(nl)} releases.")
        if nl.empty:
            break
        nl.loc[:, "layer"] = layer
        next_pkgs = nl[["name", "version"]].drop_duplicates()
        prior_pkgs = res[["name", "version"]].drop_duplicates()
        new_pkgs = next_pkgs[
            ~(
                next_pkgs["name"].isin(prior_pkgs["name"])
                & next_pkgs["version"].isin(prior_pkgs["version"])
            )
        ]
        # logging.info(f"{len(next_pkgs)} unique releases, {len(new_pkgs)} new releases")
        new_pkgs = new_pkgs.groupby("name")["version"].apply(list)
        # logging.info(f"{len(new_pkgs)} new packages")
        res = pd.concat([res, nl])
        packages = list(new_pkgs.index)
        versions = list(new_pkgs.values)
    res = res[~(res["name"].isin(tmp) & (res["layer"] > 1))]
    return res


def get_upload_time(name: str, version: str):
    return list(
        distribution_metadata.find(
            {"name": name, "version": version}, projection={"_id": 0, "upload_time": 1}
        )
    )[0]["upload_time"]


def construct_SC(framework: str, package_names: list):
    col = supply_chains[f"{framework}_edges"]
    col.drop()
    col = supply_chains[f"{framework}_edges"]
    res = all_layers(package_names)
    col.insert_many(res.to_dict("records"))
    print(f"{framework}, {len(res)} documents")
    if len(res) > 5000:
        col.create_index([("dependency", pymongo.DESCENDING)])
        col.create_index(
            [
                ("dependency", pymongo.DESCENDING),
                ("dependency_version", pymongo.ASCENDING),
            ]
        )
        col.create_index([("name", pymongo.ASCENDING)])
        col.create_index([("name", pymongo.ASCENDING), ("version", pymongo.ASCENDING)])
        col.create_index(
            [("name", pymongo.ASCENDING), ("dependency", pymongo.DESCENDING)]
        )

    nodes = []
    for _, row in res[["name", "version"]].drop_duplicates().iterrows():
        name, version = row["name"], row["version"]
        upload_time = get_upload_time(name, version)
        nodes.append({"name": name, "version": version, "upload_time": upload_time})
    col = supply_chains[f"{framework}_nodes"]
    col.drop()
    col = supply_chains[f"{framework}_nodes"]
    col.insert_many(nodes)
    print(f"{framework}, {len(nodes)} distributions")
    col.create_index([("name", pymongo.ASCENDING), ("version", pymongo.ASCENDING)])


if __name__ == "__main__":
    framework_packages = setting.FRAMEWORK_PACKAGES
    for framework, package_names in framework_packages.items():
        construct_SC(framework, package_names)
