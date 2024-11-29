# PPTX Searcher

Honestly a misnomer at this point but im not changing the name.

A utility script that can load in numerous pptx, and pdf files. Extracts the text and compiles a FST5 (Fast Text Search) sqlite database

Allows for querying over the db finding page and slides that contain the query.

## Installation

*built in python 3.11, but will hopefully work in 3 generally*

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


### Built in
to help out I already have added all the lecture slides into respective databases as well as a full db
1. `-db 201` will search for text found in 201 slides
2. `-db 220` will search for text found in 220 slides
3. `-db 243` will search for text found in 243 slides
4. No db argument will default to `searchable.db` which contains all class material from all classes

So if I wanted to perform a search for the word 'bayes' in 201 I would type `python main.py -s bayes -db 201`

Or over all classes `python main.py -s bayes`



## Tutorial / Example 
1. Download files from canvas or wherever
   <img width="913" alt="image" src="https://github.com/user-attachments/assets/5a109899-caa6-4c9e-92fd-8fe10ac91238">
2. Place in a dir nearby (i have a in_data folder ignored by github but you can put it wherever you want)
<img width="276" alt="Screenshot 2024-11-29 at 11 16 13 AM" src="https://github.com/user-attachments/assets/2713c94f-56e4-4f50-9eb6-525738b903e9">

3. Call with `-r` and `-db` args
<img width="654" alt="image" src="https://github.com/user-attachments/assets/5027aa5b-2165-45b9-92aa-151ef7a4c870">

4. Wait for text parsing to complete (sometimes the pptx files generate a ugly message but its okay i swear)
<img width="789" alt="image" src="https://github.com/user-attachments/assets/2ca9c8e2-4dad-48c9-974a-2299d72f7b53">

5. Query with the `-s` flag and `-db` flag
<img width="571" alt="image" src="https://github.com/user-attachments/assets/504e6229-63e1-4614-9f0f-3a4f5c9b9d2d">

6. Paginate over results with the `j` and `k` keys, using `q` to quit
<img width="772" alt="image" src="https://github.com/user-attachments/assets/07dab725-19dd-4fb7-b5d5-ed92888bf4c5">










