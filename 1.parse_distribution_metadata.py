# import logging
from collections import defaultdict

import pymongo
from packaging.markers import UndefinedEnvironmentName
from packaging.requirements import InvalidRequirement, Requirement
from pymongo import MongoClient
from tqdm import tqdm

db = MongoClient(host="127.0.0.1", port=27017)["dlsc"]
distribution_metadata = db["distribution_metadata"]
# LOG_PATH = "log/extract_dependency.log"


def parse_requirement(requirement_str: str):
    try:
        req = Requirement(requirement_str)
    except InvalidRequirement:
        # logging.error("InvalidRequirement: {}".format(requirement_str))
        return
    except:
        # logging.error("ParseError: {}".format(requirement_str))
        return
    name, extras, specifier, marker = req.name, req.extras, req.specifier, req.marker
    if len(extras) > 0:
        name = name + "[" + ",".join(extras) + "]"
    specifier = [str(s) for s in specifier]
    extra = False
    if marker is not None:
        try:
            marker.evaluate()
        except UndefinedEnvironmentName:
            extra = True
        except:
            # logging.error("MarkerError: {}".format(marker))
            extra = False
    return name, tuple(specifier), extra


def parse_distribution_metadata():
    dependencies = db["dependencies"]
    dependencies.drop()
    dependencies = db["dependencies"]
    deps = defaultdict(list)
    for doc in tqdm(
        distribution_metadata.find(
            {}, {"name": 1, "version": 1, "_id": 0, "requires_dist": 1}
        )
    ):
        name = doc.get("name", "")
        version = doc.get("version", "")
        requires_dist = doc.get("requires_dist", [])
        key_name = name + " " + version
        for req in requires_dist:
            res = parse_requirement(req)
            if res is not None:
                dependency, dependency_version, extra = res
                deps[key_name].append((dependency, dependency_version, extra))
    transformed_docs = []
    print("Inserting")
    for k, v in tqdm(deps.items()):
        name, version = k.split(" ", 1)
        for dependency, dependency_version, extra in set(v):
            transformed_docs.append(
                {
                    "name": name,
                    "version": version,
                    "dependency": dependency,
                    "dependency_version": dependency_version,
                    "extra": extra,
                }
            )
    print(len(transformed_docs))
    dependencies.insert_many(transformed_docs)
    dependencies.create_index(
        [("name", pymongo.ASCENDING), ("version", pymongo.ASCENDING)]
    )
    dependencies.create_index([("dependency", pymongo.ASCENDING)])
    print("Finished")


if __name__ == "__main__":
    # logging.basicConfig(
    #     format="%(asctime)s [%(levelname)s] %(message)s",
    #     level=logging.INFO,
    #     filename=LOG_PATH,
    #     filemode="w",
    # )
    parse_distribution_metadata()
