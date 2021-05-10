# Macpaw AWS Bucket Data Pipeline
[![Build Status](https://travis-ci.com/mikharkiv/macpaw-test-de.svg?branch=master)](https://travis-ci.com/mikharkiv/macpaw-test-de)

A test task for MacPaw Data Engineering Summer Intership 2021. 

Using aiohttp, Flake8, Travis CI, and Docker.

## Table of contents
* [Installation](#installation)
  * [Using Docker](#using-docker)
  * [Using Python virtual environment](#using-python-virtual-environment)
* [Command line arguments](#command-line-arguments)
* [Config file description](#config-file-description)
* [Testing](#testing)
* [Project structure description](#project-structure-description)
* [Logic behind the scenes](#logic-behind-the-scenes)
* [Dependencies](#dependencies)

## Installation
> Note: all commands should be executed in the directory where you have cloned this repository  

#### Using Docker:
0. Download and install [Docker](https://www.docker.com/get-started) if you don't have one  
1. Clone the repository to your computer  
`git clone git@github.com:mikharkiv/macpaw-test-de.git`
2. Build an image  
`docker-compose build`  
3. Run a container  
`docker-compose up app`
4. Enjoy!

#### Using Python virtual environment:
0. Download [Python](https://www.python.org/downloads/) if you don't have one  
1. Clone the repository to your computer  
`git clone git@github.com:mikharkiv/macpaw-test-de.git`
2. Make a new virtual environment  
`python -m venv venv`
3. Activate it  
On macOS and Linux:  
`source venv/bin/activate`  
On Windows:  
`.\venv\Scripts\activate`
4. Install dependencies  
`pip install -r requirements.txt`  
5. Run the app  
`cd src && python main.py`
6. Enjoy!

## Command line arguments

Usage: `main.py [-h] [--profile PROFILE] [--force]`

Optional arguments:
* `-h`, `--help` - show help 
* `--profile PROFILE` - specify configuration profile to use (from `config.ini`)
* `--force` - process all files on bucket, even if they were already processed

## Config file description

Config is in following format:
```ini
[profile_name] # Name of the profile

# Name of the database
DATABASE_NAME = db.sqlite3

# Name of the bucket (should be in this URL-like format)
BUCKET_NAME = data-engineering-interns.macpaw.io

# Key of the file with files list
FILES_LIST_KEY = files_list.data

# Encoding of the bucket
BUCKET_ENCODING = utf8

# Date-time format, in which values will be stored
DATE_STORE_FORMAT = %Y-%m-%d %H:%M:%S

# Name of the file where to save already processed files registry
PROCESSED_FILES_FILENAME = processed.json

# Whether to save output to the file
SAVE_LOG = yes
```

## Testing  
Application testing is done automatically thanks to TravisCI.  
But you can also test it by yourself using virtual environment:   
`python -m pytest`

## Project structure description

The project structure is:
*  `src/`
   * `main.py`  
   Our entry point. Here we run the application, setting up the data and running our pipeline;
   * `bucket.py`  
   Methods needed for extracting files from AWS bucket;
   * `data.py`  
   Classes which represent data types and provide processing logic;
   * `db.py`  
   Methods needed for working with database;
   * `registry.py`  
   Methods needed for working with processed files registry;
   * `settings.py`  
   Processing CLI arguments and configuration file;
   * `tests.py`  
   Unit-tests for data classes;
* `config.ini` - **app configuration** file;
* `pytest.ini` - pytest configuration file;
* `requirements.txt` - project requirements list;
* `.travis.yml` - Travis CI configuration file;
* `Dockerfile`, `docker-compose.yml`, `.dockerignore` - Docker configuration files;
* `.editorconfig` - IDE code style configuration;
* `.flake8` - Flake8 configuration file.


## Logic behind the scenes

The data pipeline consists of following stages:
1. **Application initialising**  
Configure logger, init all modules
2. **Extracting names of files to process**  
Here we're checking for connection with bucket and extracting list of files from bucket.
Then we're selecting only those files we haven't processed yet.
3. **Processing data**  
At first we asynchronously run processing for each file, thereby we achieve high processing speed and bypass IO boundaries.  
Each class in `data.py` represents one of the data types and provide own processing and validation logic.
Thereby we achieve code flexibility and good structure.  
I decided to validate data by fields types, because AWS bucket contains a lot of files and entries, and I cannot be sure that every entry is in proper format and contains required fields.
4. **Writing data to the database**  
I decided to commit changes only after all of files have been processed, because this is a time-consuming operation. Thereby we achieve less processing time.  
By using `INSERT OR UPDATE` we delegate a task of removing duplicates to the RDBMS.
5. **Logging and configuration**  
The application configuration is very convenient: `config.ini` can contain multiple configuration profiles, and we can specify which to use in CLI arguments.  
Also, the app has an option to process all of files even if they have been already processed by using `--force` CLI argument.

## Dependencies
* **aiohttp** - for making async queries;
* **pytest** - for running unit-tests;
* **flake8**, **mypy** - for checking codestyle.
  
Regards, _mikharkiv_
