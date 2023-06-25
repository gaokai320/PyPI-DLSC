# Coding Guide for Disengagement Reasons

This is a coding guide for labelling disengagement reasons. This coding guide includes three parts:
1. what materials we have for coding;
2. an operating manual that explains what the steps are for labelling the materials;
3. a Codesbook that explains what codes we have, and how the codes are defined.

## Materials for Coding
We have already prepared meterials for coding in [labeled_detached_packages.xlsx](../data/labeled_detached_packages.xlsx), which contains 364 and 201 disengaged packages in TensorFlow SC and PyTorch SC respectively.

| Column Name | Column Data |
| ----------- | ----------- |
| framework | the SC that the package disengages from |
| package | the disengaged package's name |
| dependencies | dependencies in the SC of the disengaged package |
| Repo URL | the disengaged package's repository url |
| Reason Location | the url of disengagement-relevant text |
| Reason Text | disengagement-relevant text |
| Inspector1 | labeller A's code based on the Codesbook |
| Inspector2 | labeller B's code based on the Codesbook |
| Final | the final codes after resolving lebller A and B' code conflicts |

## Operating Manual
The steps of labeling guidelines are as follows:
1. Get familliar with the coding materials and the Codesbook.
    - Read all the Reason Text in `labeled_detached_packages.xlsx`;
    - Read the Codesbook, which describes the codes we define for labelling. In the Codebook table, each line represents a code, `Definition` explains what the code is, and `Code` is the term used for labelling the materials. We also list some labelling rules after the table to help resolve ambiguities and the conflicts encountered in our labelling process.

2.  Conduct coding. For each line in the `labeled_detached_packages.xlsx`, read the `description` column, label them with matching codes. Each package is assigned to one code. For packages that you think don't have matching codes, you can label it as unclear. For packages that you think match multiple codes, please refer to the labelling rules in the next section.

## Codesbook

<table>
    <thead>
        <tr>
            <th colspan=2>Codes</th>
            <th>Definition</th>
            <th>Example</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=2>Dependency</td>
            <td>Incompatibility</td>
            <td>A package disengages from SC because its dependency induce incompatibility <b>issues (errors)</b>  with other packages, hardware, or operating systems, and the package decides to remove dependencies on them. The most common case is the confliects between TensorFlow packages. TensorFlow framework releases many packages for different hardware and operating systems, like <code>tensorflow</code>, <code>tensorflow-gpu</code>, <code>tf-nightly</code>, etc. But these packages are not <a href="https://github.com/tensorflow/tensorflow/issues/7166"> incompatible </a>.</td>
            <td>Took out pytorch dependency, since it caused errors</td>
        </tr>
        <tr>
            <td>Bloated</td>
            <td>A package disengages from SC because it doesn't use the dependencies at all, or the dependencies have been already installed in the environment.</td>
            <td>removed several useless dependencies</td>
        </tr>
        <tr>
            <td rowspan=3>Functionality</td>
            <td>Performance</td>
            <td>A package disengages from SC for better performance, e.g., cleaner code, better maintenance, faster import time, etc. The package typically migrates to another package or simply removes current upstream package.</td>
            <td>But, this development history means that nowcasting_dataset still uses PyTorch (e.g. using the PyTorch DataLoader to run multiple processes). The code may become cleaner and faster and more flexible if we strip out PyTorch, and instead (maybe) use concurrent.futures.ProcessPoolExecutor to use multiple processes.</td>
        </tr>
        <tr>
            <td>Simplification</td>
            <td>Some packages disengages from SC to decouple functionalities for clarity and simplicity. These packages may split into multiple packages or <a href="https://setuptools.pypa.io/en/latest/userguide/dependency_management.html#optional-dependencies"> extra functionalities </a> and the upstream packages may be removed completely or turnt into extra dependencies.</td>
            <td>We have recently migrated the pipeline deeplearning-prepare-datato our sister project ClinicaDL which handles everything related to deep-learning.</td>
        </tr>
        <tr>
            <td>Framework-Independent</td>
            <td>The package disengages from SC to support more frameworks and not limited to current framework.</td>
            <td>Tonic is now free from direct PyTorch and PyTorch Vision dependencies, meaning that if someone wanted to use it with another pipeline (e.g. TensorFlow), they would be able to do so. This release is the first step to making Tonic more flexible in that respect.</td>
        </tr>
        <tr>
            <td rowspan=2>Installation</td>
            <td>Flexibility</td>
            <td>The disengagement happens because the disengaged packages want to ease ans simplify the installation procedure to adapt to various environment. The main difference between <i>Flexibility</i> and <i>Compatibility</i> is that the latter is triggered by errors while the former is not triggered by errors.</td>
            <td>There are multiple official and community TensorFlow packages out there: tensorflow, tensorflow-cpu, tensorflow-gpu, tf-nightly, tensorflow-rocm, intel-tensorflow, tensorflow-macos, etc.  The main "tensorflow" package works in most cases but ultimately we should allow users to install an alternative package.</td>
        </tr>
        <tr>
            <td>Size Trimming</td>
            <td>A package disengages from SC to trim its binary size. Indeed, DL frameworks like PyTorch and TensorFlow are very huge occupying hundreds of MB spaces.</td>
            <td>In order to make AugLy less heavy for users to install, let's separate the heavier dependencies that are specific to the audio/video modules and only require the dependencies for the module that the user specifies</td>
        </tr>
    </tbody>
</table>
