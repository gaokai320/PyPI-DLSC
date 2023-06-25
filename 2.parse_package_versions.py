# import logging

import packaging
import pymongo
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from pymongo import MongoClient
from tqdm import tqdm

client = MongoClient(host="127.0.0.1", port=27017)
db = client.get_database("dlsc")
dependencies = db.get_collection("dependencies")
distribution_metadata = db.get_collection("distribution_metadata")
# LOG_PATH = "log/versioned_dependency.log"

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# handler = logging.FileHandler(LOG_PATH, "w", "utf-8")
# handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
# logger.addHandler(handler)


def contain_version(dependency_version: list, package_version: str):
    specs = SpecifierSet(prereleases=True)
    for s in dependency_version:
        specs &= s
    try:
        v = Version(package_version)
    except packaging.version.InvalidVersion:
        # logging.error("InvalidVersion: {}".format(package_version))
        return False
    return v in specs


def get_package_versions(package: str):
    pipeline = [
        {"$match": {"name": package}},
        {"$project": {"_id": False, "version": 1}},
        {"$group": {"_id": None, "versions": {"$addToSet": "$version"}}},
    ]
    versions = list(distribution_metadata.aggregate(pipeline=pipeline))
    tmp = []
    if versions:
        versions = list(versions)[0]["versions"]
        for v in versions:
            try:
                if Version(v):
                    tmp.append(v)
            except packaging.version.InvalidVersion:
                # logging.error("InvalidVersion: {}".format(v))
                pass
        tmp.sort(key=Version)
    return tmp


def build_versioned_graph_per_package(package: str):
    versions = get_package_versions(package)
    if not versions:
        return []
    query = {"dependency": package}
    tmp = []
    result = list(dependencies.find(query))
    if result:
        for doc in result:
            name = doc["name"]
            ver = doc["version"]
            dependency_version = doc["dependency_version"]
            extra = doc["extra"]
            for v in versions:
                if contain_version(dependency_version, v):
                    tmp.append(
                        {
                            "name": name,
                            "version": ver,
                            "dependency": package,
                            "dependency_version": v,
                            "extra": extra,
                        }
                    )
    return tmp


def parse_ecosystem_dependency_version():
    coll = db["versioned_dependencies"]
    coll.drop()
    coll = db["versioned_dependencies"]
    deps = dependencies.distinct("dependency", {"dependency": {"$ne": None}})
    # logging.info("{} dependencies".format(len(deps)))
    for dep in tqdm(deps):
        # logging.info("Begin building versioned graph for {}".format(dep))
        tmp = build_versioned_graph_per_package(dep)
        if tmp:
            coll.insert_many(tmp)
        # logging.info(
        #     "Finish building ver1{}, {} records in total".format(dep, len(tmp))
        # )
    coll.create_index(
        [("dependency", pymongo.ASCENDING), ("dependency_version", pymongo.ASCENDING)]
    )
    coll.create_index([("name", pymongo.ASCENDING), ("dependency", pymongo.ASCENDING)])
    coll.create_index([("name", pymongo.ASCENDING), ("version", pymongo.ASCENDING)])


if __name__ == "__main__":
    parse_ecosystem_dependency_version()
