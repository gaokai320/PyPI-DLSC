# Mongodb Database dump

The Mongodb database dumps are too large to fit in the Git repository. We upload them to Zenodo.

1. Download `mongodb_dump.tar.gz` from https://zenodo.org/record/8079662

2. Decompress it and move all its files to current folder.

3. Restore the Mongodb database.

```shell
mongorestore --db dlsc --gzip ./distribution_metadata.bson.gz
mongorestore --db dlsc --gzip ./versioned_dependencies.bson.gz
mongorestore --db dlsc ./PyTorch_edges.bson
mongorestore --db dlsc ./PyTorch_nodes.bson
mongorestore --db dlsc ./TensorFlow_edges.bson
mongorestore --db dlsc ./TensorFlow_nodes.bson
```