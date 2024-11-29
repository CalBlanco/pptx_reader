# PPTX Searcher

Honestly a misnomer at this point but im not changing the name.

A utility script that can load in numerous pptx, and pdf files. Extracts the text and compiles a FST5 (Fast Text Search) sqlite database

Allows for querying over the db finding page and slides that contain the query.

## Installation

*built in python 3.13, but will hopefully work in 3 generally*

To properly set up create a venv: `python -m venv venv`

Activate it: `source ./venv/bin/activate`

install dependencies: `pip install -r requirements.txt`

## Usage 

### Command line args:

`-r` or `--dir`: Select a directory (relative to main.py) to load in files from 

`-db` or `--database`: Name the database, will create a db file in the `./dbs/` directory if one doesnt exist, otherwise will load the database from this location

`-s` or `--search`: the search you would like to perform

### How to utilize
1. Load in data with using the `-r` and `-db` arguments. `python main.py -r <location of files> -db <desired name>` if no name is provided it will default to `searchable.db`
2. Query over db with `-s`. `python main.py -s "bayes"` (will query `searchable.db`) specify the db to search with the `-db` arg
- `python main.py -db <db name> -s <search term>`






