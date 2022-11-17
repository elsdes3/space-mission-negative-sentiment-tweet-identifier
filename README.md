# Machine Learning to Identify Negative Sentiment Tweets about JWST Mission

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/elsdes3/space-mission-negative-sentiment-tweet-identifier)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/elsdes3/space-mission-negative-sentiment-tweet-identifier/master/3_combine_raw_data.ipynb)
![CI](https://github.com/elsdes3/space-mission-negative-sentiment-tweet-identifier/actions/workflows/main.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/mit)
![OpenSource](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
![prs-welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)

## [Table of Contents](#table-of-contents)
1. [About](#about)
2. [Pre-Requisites](#pre-requisites)
3. [Usage](#usage)
4. [Notebooks](#notebooks)
5. [Notes](#notes)
6. [Project Organization](#project-organization)

## [About](#about)
This project trains a binary ML classification model to classify sentiment in tweets regarding the James Webb Space Telescope (JWST) mission, that were posted between December 30, 2021 and January 10, 2022. The model predicts if tweets
- need support
  - this is the minority class
  - corresponds to negative and neutral sentiment tweets
- do not need support
  - this is the majority class
  - corresponds to positive sentiment tweets

from the mission support/communications team.

Tweets were [streamed](https://developer.twitter.com/en/docs/tutorials/stream-tweets-in-real-time) using [AWS Kinesis Firehose](https://aws.amazon.com/kinesis/data-firehose/) and then
- combined by date and hour
- filtered to only capture tweets relating to the mission
- processed text in the tweets using text-processing via [PySpark](https://spark.apache.org/docs/latest/api/python/index.html)
- divided into training, validation and testing splits
- used to [fine-tune](https://huggingface.co/docs/transformers/training#train-in-native-pytorch) a [pre-trained transformers model](https://huggingface.co/docs/transformers/index#transformers) to predict the above-mentioned binary outcome - if tweets needs support or not

The value of using a ML-based approach to flag tweets needing support was estimated by calculating how much time would be
- missed
- wasted

if the fine-tuned transformer model was used to predict if tweets in the test split needed support or not compared to the corresponding predictions made using an alternative naive approach that did not use ML (i.e. randomly guessing if tweets needed support). The ML-based approach was shown deliver value by reducing time missed and time wasted compared to the non-ML (naive, random guessing) approach to predicting if tweets needed support or not.

For full details about the background, motivation and implementation overview, please see the [full project scope](https://github.com/elsdes3/space-mission-negative-sentiment-tweet-identifier/master/).

## [Pre-Requisites](#pre-requisites)
1. The following AWS ([1](https://docs.aws.amazon.com/sdk-for-php/v3/developer-guide/guide_credentials_environment.html), [2](https://docs.aws.amazon.com/sdk-for-php/v3/developer-guide/guide_credentials_profiles.html)) and [Twitter Developer API](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api) credentials
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION`
   - `AWS_S3_BUCKET_NAME`
   - `TWITTER_API_KEY`
   - `TWITTER_API_KEY_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_TOKEN_SECRET`

   must be stored in a [`.env` file](https://help.pythonanywhere.com/pages/environment-variables-for-web-apps/) stored one level up from the root directory of this project.i.e. one level up from the directory containing this `README.md` file.

## [Usage](#usage)
1. Create AWS resources
   ```bash
   make -f Makefile-stream aws-create
   ```
   In this step, if the code in the [section **See EC2 Public IP Address in Ansible Inventory**](https://nbviewer.org/github/elsdes3/machine-learning-with-big-data/blob/main/1_create_aws_resources.ipynb#set-ec2-public-ip-address-in-ansible-inventory) has **not** been manually executed, then edit
   ```bash
   inventories/production/host_vars/ec2host
   ```
   and replace `...` in `ansible_host: ...` by the public IP address of the newly created EC2 instance from the AWS Console in the EC2 section.
2. Provision the EC2 host, excluding Python package installation
   ```bash
   make -f Makefile-stream provision-pre-python
   ```
3. Install Python packages on the EC2 host
   ```bash
   make -f Makefile-stream provision-post-python
   ```
4. Start the Twitter streaming script locally
   ```bash
   make -f Makefile-stream stream-local-start
   ```
5. Stop the Twitter streaming script running locally
   ```bash
   make -f Makefile-stream stream-local-stop
   ```
6. Start the Twitter streaming script on the EC2 instance
   ```bash
   make -f Makefile-stream stream-start
   ```
7. Stop the Twitter streaming script running on the EC2 instance
   ```bash
   make -f Makefile-stream stream-stop
   ```
8. (optional) Run the Twitter streaming script locally, saving to a local CSV file but not to S3
   ```bash
   make -f Makefile-stream stream-check
   ```

   Pre-Requisites
   - the eight environment variables listed above must be manually set, before running this script, using
     ```bash
     export AWS_ACCESS_KEY_ID=...
     export AWS_SECRET_ACCESS_KEY=...
     export AWS_REGION=...
     export AWS_S3_BUCKET_NAME=...
     export TWITTER_API_KEY=...
     export TWITTER_API_KEY_SECRET=...
     export TWITTER_ACCESS_TOKEN=...
     export TWITTER_ACCESS_TOKEN_SECRET=...
     ```
9. Combine data (tweets) by hour
   ```base
   make combine-data combine-data-logs
   ```
10. Combine data (tweets) by hour
    ```base
    make combine-data combine-data-logs
    ```
11. Filter hourly data (tweets) to remove unwanted / irrelevant tweets
    ```base
    make filter-data filter-data-logs
    ```
12. Process text of *all* filtered data (tweets)
    ```base
    make process-data process-data-logs
    ```
13. Split data
    ```base
    make split-data split-data-logs
    ```
14. Fine-tune pre-trained model
    ```base
    make train train-logs
    ```
15. Evaluate prediction probabilities on unseen data
    ```base
    make inference inference-logs
    ```
16. Destroy AWS resources
    ```bash
    make -f Makefile-stream aws-destroy
    ```

## [Notebooks](#notebooks)
1. `1_create_aws_resources.ipynb` ([view](https://nbviewer.org/github/elsdes3/space-mission-negative-sentiment-tweet-identifier/blob/main/1_create_aws_resources.ipynb))
   - use the AWS Python SDK (`boto3` [link](https://pypi.org/project/boto3/)) to create AWS resources
     - [S3 storage bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
     - [CloudWatch Log Group and Log Stream](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatchLogsConcepts.html)
     - [IAM Role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html)
     - [Kinesis Firehose Delivery Stream](https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html)
2. `2_delete_aws_resources.ipynb` ([view](https://nbviewer.org/github/elsdes3/space-mission-negative-sentiment-tweet-identifier/blob/main/2_delete_aws_resources.ipynb))
   - use `boto3` to delete all AWS resources
3. `3_combine_data.ipynb` ([view](https://nbviewer.org/github/elsdes3/space-mission-negative-sentiment-tweet-identifier/blob/main/notebooks/3-combine-data/notebooks/3_combine_data.ipynb))
   - combines raw data (streamed tweets) by hour
   - since each hour of data files were small enough to read into a single data object (DataFrame), in-memory tools were used to combine each hourly folder of streamed data
4. `4_filter_data.ipynb` ([view](https://nbviewer.org/github/elsdes3/space-mission-negative-sentiment-tweet-identifier/blob/main/notebooks/4-filter-data/notebooks/4_filter_data.ipynb))
   - filter hourly tweets to remove tweets unrelated to the JWST mission
   - filters out unwanted tweets based on a list of words that are not relevant to the subject of this project
5. `5_process_data.ipynb` ([view](https://nbviewer.org/github/elsdes3/space-mission-negative-sentiment-tweet-identifier/blob/main/notebooks/5-process-data/notebooks/5_process_data.ipynb))
   - processes text in *all* filtered tweets using PySpark string manipulation methods
6. `6_split_data.ipynb` ([view](https://nbviewer.org/github/elsdes3/space-mission-negative-sentiment-tweet-identifier/blob/main/notebooks/6-split-data/notebooks/6_split_data.ipynb))
   - divide processed data into training, validation and testing splits
7. `7_train.ipynb` ([view](https://nbviewer.org/github/elsdes3/space-mission-negative-sentiment-tweet-identifier/blob/main/notebooks/7-train/notebooks/7_train.ipynb))
   - fine-tune pre-trained transformers model to flag tweets that need and do not need support
   - pre-trained model is trained using training and validation split
   - fine-tuned model is then exported to disk and evaluated using test split
     - model evaluation is performed using ML and business metrics
8. `8_inference.ipynb` ([view](https://nbviewer.org/github/elsdes3/space-mission-negative-sentiment-tweet-identifier/blob/main/notebooks/8-inference/notebooks/8_inference.ipynb))
   - trends in fine-tuned model's probabilistic predictions are examined in order to compare the same after re-training in production
   - this is necessary in order to ensure model performs as expected in production, when making inference predictions

## [Notes](#notes)
1. When running the script locally (step 8. from **Usage** above), there is no functionality to stop the `twitter_s3.py` script. It has to be stopped manually by
   - pressing <kbd>Ctrl</kbd> + <kbd>C</kbd>
   - waiting until the specified number of tweets in `max_num_tweets_wanted` on line 217 of `twitter_s3.py`, have been streamed
2. Running the notebooks to create and destroy AWS resources in a non-interactive approach has not been verified. It is not currently known if this is possible.
3. AWS resources are created and destroyed using the `boto3` AWS Python SDK. The AWS EC2 instance that is used to host the Twitter streaming (Python) code is [provisioned using Ansible playbooks](https://www.ansible.com/use-cases/provisioning).
4. The AWS credentials must be associated to a user group whose users have been granted programmatic access to AWS resources. In order to configure this for the IAM user group from the AWS console, see the documentation [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console). For this project, this was done before creating any AWS resources using the AWS Python SDK.
5. The Twitter credentials must be for a user account with [elevated access](https://developer.twitter.com/en/support/twitter-api/v2) to the Twitter Developer API.
6. Data used for this project was collected between December 30, 2021 and January 10, 2022.

## [Project Organization](#project-organization)

    ├── LICENSE
    ├── .gitignore                          <- files and folders to be ignored by version control system
    ├── .pre-commit-config.yaml             <- configuration file for pre-commit hooks
    ├── .github
    │   ├── workflows
    │       └── main.yml                    <- configuration file for CI build on Github Actions
    ├── Makefile                            <- Makefile with commands like `make lint` or `make build`
    ├── Makefile-stream                     <- Makefile for streaming tweets
    ├── README.md                           <- The top-level README for developers using this project.
    ├── scoping.md                          <- Project scope.
    ├── ansible.cfg                         <- configuration file for Ansible
    ├── environment.yml                     <- configuration file to create environment to run project on Binder
    ├── manage_host.yml                     <- manage provisioning of EC2 host
    ├── read_data.py                        <- Python script to read streamed Twitter data that has been saved locally
    ├── streamer.py                         <- Wrapper script to control local or remote Twitter streaming
    ├── stream_twitter.yml                  <- stream Twitter data on EC2 instance
    ├── twitter_s3.py                       <- Python script to stream Twitter data locally or on EC2 instance
    ├── variables_run.yaml                  <- Ansible playbook variables
    ├── tox.ini                             <- tox file with settings for running tox; see https://tox.readthedocs.io/en/latest/
    ├── utils.sh                            <- shell convenience utilities when caling `make`
    ├── data
    │   ├── raw                             <- The original, immutable data dump.
    |   └── processed                       <- Intermediate (transformed) data and final, canonical data sets for modeling.
    ├── notebooks                           <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                                          the creator's initials, and a short `-` delimited description, e.g.
    │                                          `1.0-jqp-initial-data-exploration`.
    ├── inventories
    │   ├── production
    │       ├── host_vars                   <- variables to inject into Ansible playbooks, per target host
    │           └── ec2_host
    |       └── hosts                       <- Ansible inventory
    ├── v1                                  <- previous version of project - topic modeling using big-data tools only
    ├── src                                 <- Source code for use in this project
    │   └── __init__.py                     <- Makes src a Python module

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
