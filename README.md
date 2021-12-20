# aws-project-name

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/edesz/aws-project-name)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/edesz/aws-project-name/master/0_get_data.ipynb)
![CI](https://github.com/edesz/aws-project-name/workflows/CI/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/mit)
![OpenSource](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
![prs-welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)
![pyup](https://pyup.io/repos/github/edesz/aws-project-name/shield.svg)

## [Table of Contents](#table-of-contents)
1. [About](#about)
2. [Project Organization](#project-organization)
3. [Usage](#usage)
4. [Notes](#notes)

## [About](#about)

A short description of the project.

## [Usage](#usage)
1. Provision the EC2 host
   ```bash
   make provision
   ```
2. Start the Twitter streaming script on the EC2 instance
   ```bash
   make stream-start
   ```
3. Stop the Twitter streaming script on the EC2 instance
   ```bash
   make stream-stop
   ```
4. Start the Twitter streaming script locally
   ```bash
   make stream_local
   ```

## [Notes](#notes)
1. Running the Twitter streaming script locally is a manual process done using
   ```bash
   make stream_local
   ```

   This will run the Python streaming script in a background process. It will be up to the user to manually
   - find the appropriate background process ID
   - stop the process

   if the script is to be stopped before it reaches the preset limit for maximum number of tweets to be streamed.
2. Running the streaming script remotely is done using the Ansible playbook `stream_twitter.yml` and tags `start` and `stop` via
   ```bash
   make stream-start
   ```
   and

   ```bash
   make stream-stop
   ```
   can be used to start and stop the execution of the script as a background process with no manual input required.

## [Project Organization](#project-organization)

    ├── LICENSE
    ├── .gitignore                          <- files and folders to be ignored by version control system
    ├── .pre-commit-config.yaml             <- configuration file for pre-commit hooks
    ├── .github
    │   ├── workflows
    │       └── main.yml                    <- configuration file for CI build on Github Actions
    ├── Makefile                            <- Makefile with commands like `make lint` or `make build`
    ├── README.md                           <- The top-level README for developers using this project.
    ├── ansible.cfg                         <- configuration file for Ansible
    ├── environment.yml                     <- configuration file to create environment to run project on Binder
    ├── manage_host.yml                     <- manage provisioning of EC2 host
    ├── read_data.py                        <- Python script to read streamed Twitter data that has been saved locally
    ├── stream_twitter.yml                  <- stream Twitter data on EC2 instance
    ├── twitter_s3.py                       <- Python script to stream Twitter data locally or on EC2 instance
    ├── executed_notebooks
    |   └── *.ipynb                         <- executed notebooks, with output and execution datetime suffix in filename
    ├── data
    │   ├── raw                             <- The original, immutable data dump.
    |   └── processed                       <- Intermediate (transformed) data and final, canonical data sets for modeling.
    ├── *.ipynb                             <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                                          and a short `-` delimited description, e.g. `1.0-jqp-initial-data-exploration`.
    ├── requirements.txt                    <- base packages required to execute all Jupyter notebooks (incl. jupyter)
    ├── inventories
    │   ├── production
    │       ├── host_vars                   <- variables to inject into Ansible playbooks, per target host
    │           └── ec2_host
    |       └── hosts                       <- Ansible inventory
    ├── src                                 <- Source code for use in this project.
    │   ├── __init__.py                     <- Makes src a Python module
    │   │
    │   ├── cw                              <- Scripts to manage AWS CloudWatch Log Groups and Streams
    │       └── cloudwatch_logs.py
    │   │
    │   ├── ec2                             <- Scripts to manage AWS EC2 instances and security groups
    │       └── ec2_instances_sec_groups.py
    │   │
    │   ├── firehose                        <- Scripts to manage AWS Kinesis firehose data streams
    │       └── kinesis_firehose.py
    │   │
    │   ├── iam                             <- Scripts to manage AWS IAM
    │       └── iam_roles.py
    │   │
    │   ├── keypairs                        <- Scripts to manage AWS EC2 SSH key pairs
    │       └── ssh_keypairs.py
    │   │
    │   └── s3                              <- Scripts to manage AWS S3 buckets
    │       └── buckets.py
    │
    ├── papermill_runner.py                 <- Python functions that execute system shell commands.
    └── tox.ini                             <- tox file with settings for running tox; see https://tox.readthedocs.io/en/latest/

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
