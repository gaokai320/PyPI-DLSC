import json
from datetime import timedelta

import numpy as np
import pandas as pd
import pymongo
from packaging.version import Version
from pymongo import MongoClient
from tqdm import tqdm

from setting import FRAMEWORK_PACKAGES

client = MongoClient(host="127.0.0.1", port=27017)
distribution_metadata = client["dlsc"]["distribution_metadata"]
sc_db = client["dlsc"]


def package_versions(col: pymongo.collection.Collection, name: str, start_time: str):
    pipeline = [
        {"$match": {"name": name, "upload_time": {"$gte": start_time}}},
        {"$group": {"_id": None, "versions": {"$addToSet": "$version"}}},
    ]

    versions = list(col.aggregate(pipeline))
    if versions:
        versions = versions[0]["versions"]
        versions = [
            v
            for v in versions
            if not (Version(v).is_prerelease or Version(v).is_devrelease)
        ]
        versions.sort(key=Version)
    return versions


def package_sc_versions(name: str, start_time: str, sc: str = None):
    if sc is None:
        return package_versions(distribution_metadata, name, start_time)
    col = sc_db[f"{sc}_nodes"]
    return package_versions(col, name, start_time)


def sc_packages_info(sc: str):
    pipeline = [{"$group": {"_id": None, "packages": {"$addToSet": "$name"}}}]
    packages = list(sc_db[f"{sc}_nodes"].aggregate(pipeline))[0]["packages"]
    res = {}
    layer1_packages = list(
        sc_db[f"{sc}_edges"]
        .find({"layer": 1}, projection={"name": 1, "_id": 0})
        .distinct("name")
    )
    start_time = list(
        sc_db[f"{sc}_nodes"].find(
            {"name": {"$in": layer1_packages}}, sort=[("upload_time", 1)]
        )
    )[0]["upload_time"]
    for p in tqdm(packages, desc=sc):
        res[p] = {}
        res[p]["pypi_version"] = package_sc_versions(p, start_time)
        res[p]["sc_version"] = package_sc_versions(p, start_time, sc)

    with open(f"data/{sc}/package_version_info.json", "w") as outf:
        json.dump(res, outf, indent=4)


def single_version_sc(frmwk: str, version: str, edges: pd.DataFrame):
    sc = {}
    layer1 = edges[(edges["layer"] == 1) & (edges["version"] == version)][
        ["name", "version"]
    ].drop_duplicates()
    sc[1] = list(layer1["name"].unique())

    layer = 1
    right_df = layer1.copy()
    all_df = layer1.copy()

    while not right_df.empty:
        layer += 1
        cur_layer = edges.merge(
            right_df,
            left_on=["dependency", "dependency_version"],
            right_on=["name", "version"],
        )

        if not cur_layer.empty:
            sc[layer] = list(cur_layer["name_x"].unique())
            right_df = (
                cur_layer[["name_x", "version_x"]]
                .drop_duplicates()
                .rename(columns={"name_x": "name", "version_x": "version"})
            )
            right_df = right_df[
                ~(
                    right_df["name"].isin(all_df["name"])
                    & right_df["version"].isin(all_df["version"])
                )
            ]
            all_df = all_df.append(right_df)
        else:
            break
    return sc


def versioned_sc(frmwk: str):
    res = {}
    edges = sc_db[f"{frmwk}_edges"]
    versions = list(edges.find({"layer": 1}).distinct("version"))
    edges = pd.DataFrame(edges.find({}, projection={"_id": 0}))

    for v in tqdm(versions, desc=frmwk):
        res[v] = single_version_sc(frmwk, v, edges)

    with open(f"data/{frmwk}/versioned_sc.json", "w") as outf:
        json.dump(res, outf, indent=4)




if __name__ == "__main__":
    frameworks = list(FRAMEWORK_PACKAGES.keys())

    for f in frameworks:
        sc_packages_info(f)
        versioned_sc(f)
