# PyPI-DLSC
Supplementary materials for "Characterizing Deep Learning Package Supply Chains in PyPI: Domains, Clusters, and Disengagement"

This is the replication package for our TOSEM Submission *Characterizing Deep Learning Package Supply Chains in PyPI: Domains, Clusters, and Disengagement*. It can be used to replicate all three research questions in the paper using our preprocessed and manually labeled data.

## Replication Package Setup

We use Anaconda for Python development, so please configure to use a new Conda environment by executing the following commands step by step.
```shell
conda create -n CompareDLSC python=3.8
conda activate CompareDLSC
pip install -r requirements.txt
pip install ipykernel
```

## Folder Structure

1. `coding guide`: contains code books developed in this paper.

2. `data`:
   - `community types.xlsx`: data and results for cluster shape labelling in RQ2.
   - `downloads.csv`: monthly downloads data for all PyPI packages between Nov 4, 2021 and Dec 4, 2021.
   - `labeled_detached_packages.xlsx`: data and results for disengagement reason labelling in RQ3.
   - `most_downloaded_packages.xlsx`: data and results for package domain labelling in RQ1.
   - `pytorch_most_downloaded.csv`: information for the 259 most downloaded packages in PyTorch SC.
   - `tensorflow_most_downloaded.csv`: information for the 219 most downloaded packages in TensorFlow SC.
   - `TensorFlow` folder:
      - `package_version_info.json`: contains the PyPI versions and SC versions for packages in TensorFlow SC.
      - `TensorFlow_communities`: contains the packages in each cluster. Clusters are sorted by the number of packages in it and the alpha order. Packages in each cluster are sorted by the Katz centrality within the cluster.
      - `TensorFlow_community_info.csv`: contains the cluster information for each package.
      - `TensorFlow_edges.csv`: each row contains a dependent and its dependency.
      - `TensorFlow_nodes.csv`: the information of all packages in TensorFlow SC.
      - `versioned_sc.json`: the SC for each version of TensorFlow.
   - `PyTorch` folder: similar to `TensorFlow` folder.

3. `Figures` folder:
   - `cluster_centralities.pdf`: corresponds to Figure 5 in the paper.
   - `deprecation_trend.pdf`: corresponds to Figure 6 in the paper.
   - `most_downloaded_package_domains.pdf`: corresponds to Figure 2 in the paper.
   - `shape_distribution.pdf`: corresponds to Figure 4 in the paper.
   - `TensorFlow` folder: each file corresponds to a visualization of a cluster in TensorFlow SC. Files are sorted by cluster size and alpha order.
   - `PyTorch` folder: similar to `TensorFlow` folder.

4. `mongodb_dump` folder: contains the dump of `distribution_metadata` collection and `versioned_dependencies` collection.

5. `SupplyChains`: contains the dump of edges and nodes in TensorFlow SC and PyTorch SC.

## Replication Results
1. Construct PyPI DL SCs

   We retrieve the PyPI distribution metadata dump from [Google Big query](https://console.cloud.google.com/marketplace/product/gcp-public-data-pypi/pypi) with the following query:

   ```SQL
   SELECT
     metadata_version, name, version, summary, author, author_email, maintainer, maintainer_email,
      license, keywords, classifiers, platform, home_page, download_url, requires_python, requires,
      provides, obsoletes, requires_dist, provides_dist, obsoletes_dist, requires_external, project_urls,
      upload_time, filename, size, python_version, packagetype, comment_text
   FROM
     `bigquery-public-data.pypi.distribution_metadata`
   WHERE
   ```
   We import the results as a json file `distribution_metadata.json`. Then import it into a MongoDB database:

   We need to build index on the `name` field to speed up the construction process.

   Then, we build the ecosystem-wise and version-sensitive database using the following commands:

   ```shell
   python 1.parse_distribution_metadata.py
   python 2.parse_package_versions.py
   ```
   We provide the MongoDB database dump in the replication package, please refer to the `mongodb_dump` folder:

   We construct PyPI DL SCs with this command:

   ```shell
   python 3.construct_supply_chain.py
   ```
   We also provide the SC database dump in the replication package, please refer to the `mongodb_dump` folder:

2. There are three jupyter notebooks: `RQ1_domains.ipynb`, `RQ2_clusters.ipynb`, and `RQ3_deprecations.ipynb`, corresponding to the three RQs in our paper. You can directly see the plots and numbers used in our paper in the cells' output. For each notebook, you can start a Python kernel and run all cells, and then you should be able to replicate all the results in this notebook. The results should look identical or similar to the plots in the paper if it is working properly. `4.deprecation_utils.py` are used to construct datasets for RQ3: `python 4.deprecation_utils.py`. `utils.ipynb` are to generate some statistics in the paper, including footnote 2, the manual inspection of bloated dependencies in Section 4.