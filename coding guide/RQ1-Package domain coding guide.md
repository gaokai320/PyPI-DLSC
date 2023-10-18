# Package type coding guide

This is a coding guide for labelling package domains. This coding guide includes three parts:
1. what materials we have for coding;
2. an operating manual that explains what the steps are for labelling the materials;
3. a Codesbook that explains what codes we have, and how the codes are defined.

## Materials for Coding
We have already prepared meterials for coding in [most_downloaded_package.xlsx](../data/most_downloaded_packages.xlsx), which contains 219 and 259 packages with more than 3825 monthly downloads in TensorFlow SC and PyTorch SC respectively. Note that there are only 437 unique packages in total since there are 41 packages existing in both SCs.

| Column Name | Column Data |
| ----------- | ----- |
| name | the package name |
| PyTorch | whether the package exists in PyTorch SC |
| TensorFlow | whether the package exists in TensorFlow SC |
| has_dependents | whether the package has dependents |
| num_downloads | the package's monthly downloads between 2021-11-04 and 2021-12-04 |
| pypi page | the package's pypi project page url |
| repository | the packages' code repository or homepage url |
| description | natural language descriptions on the packages' functionality collected from its pypi project page or code repository or homepage |
| A' code | labeller A's code based on the Codesbook |
| B' code | labeller B's code based on the Codesbook |
| final code | the final codes after resolving lebller A and B' code conflicts |

## Operating Manual
The steps of labeling guidelines are as follows:
1. Get familliar with the coding materials and the Codesbook.
    - Read all the package descriptions in `most_downloaded_package.xlsx`;
    - Read the Codesbook, which describes the codes we define for labelling. In the Codebook table, each line represents a code, `Definition` explains what the code is, and `Code` is the term used for labelling the materials. We also list some labelling rules after the table to help resolve ambiguities and the conflicts encountered in our labelling process.

2.  Conduct coding. For each line in the `most_downloaded_package.xlsx`, read the `description` column, label them with matching codes. Each package is assigned to one code. For packages that you think don't have matching codes, you can label it as unclear. For packages that you think match multiple codes, please refer to the labelling rules in the next section.


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
            <td rowspan=9>Applications</td>
            <td>Natural Language Processing (NLP)</td>
            <td>Packages dealing with text data. It includs various datasets, models, and frameworks for tasks like neural machine translation, sentiment analysis, chatbots, word tokenizer, topic modeling, language modelling. </td>
            <td>abdothebest: GeNN (generative neural networks) is a high-level interface for text applications using PyTorch RNN's.</td>
        </tr>
        <tr>
            <td>Computer Vision (CV)</td>
            <td>Packages dealing with image and video data. It includs various datasets, models, and frameworks for tasks like
                image classification, object detection, semantic segmentation, text to image generation, optical character
                recognition.</td>
            <td>basicsr: BasicSR (Basic Super Restoration) is an open-source image and video restoration toolbox based on
                PyTorch, such as super-resolution, denoise, deblurring, JPEG artifacts removal, etc.</td>
        </tr>
        <tr>
            <td>Audio Processing (Audio)</td>
            <td>Packages dealing with audio data. It includs various datasets, models, and frameworks for tasks like audio
                source separation, speech recognition, speech synthesis.</td>
            <td>asteroid: PyTorch-based audio source separation toolkit.</td>
        </tr>
        <tr>
            <td>Time Series</td>
            <td>Packages dealing with time series data. It includs various datasets, models, and frameworks for tasks like time
                series forecasting, time series data synthesis, survival analysis.</td>
            <td>pytorch-forecasting: PyTorch Forecasting is a PyTorch-based package for forecasting time series with
                state-of-the-art network architectures. It provides a high-level API for training networks on pandas data frames
                and leverages PyTorch Lightning for scalable training on (multiple) GPUs, CPUs and for automatic logging.</td>
        </tr>
        <tr>
            <td>Information Retrieval (IR)</td>
            <td>Packages for recommender systems and ranking problems.</td>
            <td>tensorflow-ranking: TensorFlow Ranking is a framework to define learning-to-rank models.</td>
        </tr>
        <tr>
            <td>Graph</td>
            <td>Packages dealing with graphs and complex networks. It involves graph neural networks. </td>
            <td>ogb: The Open Graph Benchmark (OGB) is a collection of benchmark datasets, data loaders, and evaluators for
                graph machine learning.</td>
        </tr>
        <tr>
            <td>Tabular Data</td>
            <td>Packages dealing with tabular data. It involves packages for learning from tabular data or syntehsizing tabular
                data.</td>
            <td>pytorch-tabnet: This is a pyTorch implementation of Tabnet (Arik, S. O., & Pfister, T. (2019). TabNet: Attentive
                Interpretable Tabular Learning</td>
        </tr>
        <tr>
            <td>Security</td>
            <td>Packages for computer security problems, such as deciphering, encryption, and attack detection.</td>
            <td>ciphey: Fully automated decryption/decoding/cracking tool using natural language processing & artificial
                intelligence, along with some common sense.</td>
        </tr>
        <tr>
            <td>Other Applications</td>
            <td>Packages dealing with other application tasks that do not fit to the above applications, such as graphics,
                autonomous driving, and robotics.</td>
            <td>pysnakegym: Gym for the Snake Game</td>
        </tr>
        <tr>
            <td rowspan=13>Infrastructure</td>
            <td>Model</td>
            <td>Packages that provide model architectures, pretrained models, or layers suitable for various application tasks
                and not dedicated to a specific application.</td>
            <td>sru: SRU is a recurrent unit that can run over 10 times faster than cuDNN LSTM, without loss of accuracy tested
                on many tasks.</td>
        </tr>
        <tr>
            <td>Framework</td>
            <td>General purpose packages that provide workflows and high-level APIs to help developers build and deploy deep
                learning applications and conduct deep learning research.</td>
            <td>keras: Keras is a deep learning API written in Python, running on top of the machine learning
                platform TensorFlow. It was developed with a focus on enabling fast experimentation and providing a delightful
                developer experience.</td>
        </tr>
        <tr>
            <td>MLOps Platform</td>
            <td>Packages provided by MLOps platforms. These packages are tightly integrated with MLOps platforms to strealine
                building, training, and deploying deep learning applications.</td>
            <td>tfx: TensorFlow Extended (TFX) is a Google-production-scale machine learning platform based on TensorFlow. It
                provides a configuration framework to express ML pipelines consisting of TFX components. TFX pipelines can be
                orchestrated using Apache Airflow and Kubeflow Pipelines. Both the components themselves as well as the
                integrations with orchestration systems can be extended.</td>
        </tr>
        <tr>
            <td>Monitoring</td>
            <td>Packages for monitoring the training process of deep learning models, usually in the form of visualization.</td>
            <td>ml-logger: ML-Logger, A Simple and Scalable Logging Utility With a Beautiful Visualization Dashboard That Is
                Super Fast</td>
        </tr>
        <tr>
            <td>Data Processing</td>
            <td>Packages that provide general pipeline to load and preprocess various kinds of data.</td>
            <td>tensorflow-io: TensorFlow I/O is a collection of file systems and file formats that are not available in
                TensorFlow's built-in support.</td>
        </tr>
        <tr>
            <td>Distributed Training</td>
            <td>Packages that facilitate training deep learning models in a distributed way, e.g., multi-GPUs, multiple
                machines.</td>
            <td>elephas: Elephas is an extension of Keras, which allows you to run distributed deep learning models at scale
                with Spark.</td>
        </tr>
        <tr>
            <td>AutoML</td>
            <td>Packages that automatically search model architecture, model hyperparameters given the dataset.</td>
            <td>autokeras: AutoKeras: An AutoML system based on Keras.</td>
        </tr>
        <tr>
            <td>Optimization</td>
            <td>Packages that provide various optimizatipon functions.</td>
            <td>adabelief-pytorch: PyTorch implementation of AdaBelief Optimizer</td>
        </tr>
        <tr>
            <td>Deployment</td>
            <td>Packages that facilitate deploying deep learning models to browser, cloud, or mobile.</td>
            <td>tflite-model-maker: The TFLite Model Maker library simplifies the process of adapting and converting a
                TensorFlow neural-network model to particular input data when deploying this model for on-device ML
                applications.</td>
        </tr>
        <tr>
            <td>Training Simplification</td>
            <td>Packages that simplify the training process by freeing developers from writing biolerplate.</td>
            <td>poutyne: Poutyne is a simplified framework for PyTorch and handles much of the boilerplating code needed to
                train neural networks.</td>
        </tr>
        <tr>
            <td>Evaluation</td>
            <td>Packages that provide various metrics to evaluate deep learning models.</td>
            <td>torchmetrics: TorchMetrics is a collection of 90+ PyTorch metrics implementations and an easy-to-use API to
                create custom metrics.</td>
        </tr>
        <tr>
            <td>Model Compression</td>
            <td>Packages that compress trained deep learning model size or faciliate model compression, e.g., quantization.</td>
            <td>compressai: CompressAI (compress-ay) is a PyTorch library and evaluation platform for end-to-end compression
                research.</td>
        </tr>
        <tr>
            <td>Model Conversion</td>
            <td>Packages that convert deep learning models from one frameworks to another framework.</td>
            <td>keras2onnx: The keras2onnx model converter enables users to convert Keras models into the ONNX model format.
            </td>
        </tr>
        <tr>
            <td rowspan="7">Sciences</td>
            <td>Biology</td>
            <td>Packages that solves biological problems. It includs various datasets, models, and frameworks for tasks like
                cell detection and segmentation, brain image processing, DNA/RNA/protein sequence prediction.</td>
            <td>alphafold2-pytorch: an unofficial Pytorch implementation / replication of Alphafold2</td>
        </tr>
        <tr>
            <td>Medicine</td>
            <td>Packages that deals with medical images and health records.</td>
            <td>ivadomed: ivadomed is an integrated framework for medical image analysis with deep learning.</td>
        </tr>
        <tr>
            <td>Physics</td>
            <td>Packages that solves physics problems, e.g., engines simulating physics environment, astronomical data analysis.
            </td>
            <td>deeptrack: A deep learning oriented microscopy image simulation package. We provide tools to create physical
                simulations of optical systems, to generate and train neural network models, and to analyze experimental data.
            </td>
        </tr>
        <tr>
            <td>Economy</td>
            <td>Packages that apply deep learning to echnomic problems, e.g., trading, quantitative investment, and
                econometrics.</td>
            <td>empyrial: Empyrial is a Python-based open-source quantitative investment library dedicated to financial
                institutions and retail investors.</td>
        </tr>
        <tr>
            <td>Mathematics</td>
            <td>Packages for solving mathematic problem, e.g., differential equations, statistical problems.</td>
            <td>leibniz: Leibniz is a package providing facilities to express learnable differential equations based on PyTorch
            </td>
        </tr>
        <tr>
            <td>Quantum Computing</td>
            <td>Packages that integrate deep learning with quantum computing.</td>
            <td>c3-toolset-nightly: The C3 package is intended to close the loop between open-loop control optimization, control
                pulse calibration, and model-matching based on calibration data. Integrated tool-set for Control, Calibration
                and Characterization of quantum devices applied to superconducting qubits</td>
        </tr>
        <tr>
            <td>Other Disciplines</td>
            <td>Packages that touch disciplines not listed in the above, e.g., geography, climate, and materials.</td>
            <td>lauetoolsnn: LaueNN- neural network training and prediction routine to index single and polycrystalline Laue
                diffraction patterns</td>
        </tr>
        <tr>
            <td colspan=2>Probabilistic Methods</td>
            <td>Packages related to probabilistic methods. Probabilistic methods include Gaussian processes, Bayesian methods, causal inference</td>
            <td>edward: A library for probabilistic modeling, inference, and criticism</td>
        </tr>
        <tr>
            <td colspan=2>Social Aspects</td>
            <td>Packages related to deep learning model's robustness, interpretability, explainability, fairness, and privacy.</td>
            <td>aif360: The AI Fairness 360 toolkit is an open-source library to help detect and mitigate bias in machine learning models.</td>
        </tr>
        <tr>
            <td colspan=2>Reinforcement Learning</td>
            <td>Packages that provide various environments, models, and frameworks for building reinforcement learning models and conduct reinforcement learning research.</td>
            <td>anyrl: It is a general-purpose library for Reinforcement Learning which aims to be as modular as possible</td>
        </tr>
        <tr>
            <td colspan=2>Miscellaneous Tools</td>
            <td>Packages that provide commonly used utilities and wrappers.</td>
            <td>torch-snippets: One line functions for common tasks</td>
        </tr>
        <tr>
            <td colspan=2>Education</td>
            <td>Packages that accompany with deep learning book or courses.</td>
            <td>fastbook: Deep Learning for Coders with fastai and PyTorch: AI Applications Without a PhD - the book and the course</td>
        </tr>
    </tbody>
</table>

### labelling rules
We summarize a set of carefully justified rules for resolving angiguities and conflicts during the labelling process.

- *Applications* and *Sciences* First. Some packages may be related to both an *application* or *Sciences* domain and a domain in the other categories. In these cases, assign these packages to corresponding *Application* or *Sciences* domain. For example, `textattack` is a Python framework for adversarial attacks, data augmentation, and model training in NLP. We assign it to the `NLP` domain instead of `Social Aspects`.

- *Sciences* is over *Applications*. It is natural deep learning technique applied in some *Sciences* domains are similar to *Applications* domains, e.g., cell detection are essentially object detection tasks in CV. Considering the particularity of scientific tasks, in these cases, assign the packages to *Sciences* domains. This also aligns with the topic division of NeurIPS.

- *Infrastructure* packages are not confined to a certain *Application* or *Science* domain, e.g., NLP, but rather provide functionalities applicable to multiple *Application* or *Science* domains. If a package is applicable to multiple *Application* or *Science* domains (e.g., CV, NLP, and Audio), assign it under the *Infrastructure* category.
