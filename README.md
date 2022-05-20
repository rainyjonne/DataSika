# DataSika :deer: 
Have you gotten stuck in data muds and needed to write pile of codes to handle just a tiny data type problems? Or have you bumped into some situations that you have to check out your spaghetti codes :spaghetti: for a long time to see what's wrong when cleaning your data?  Don't worry! :relieved: Here comes `DataSika` :deer:  for you! `DataSika` is a simple python package that allows you to produce your own data pipeline locally by writing some basic **standard yaml syntaxs**. You can do **webscrapping**, **api-requesting** based on our useful functions. Also, we provide some filter availabilities for you if you want to filter out some content by **xpath (for html responses)**, **jsonpath (for json responses)** and **sql (for manipulating dataframes)**. Can't wait to try? Just install it as soon as possible and test it with examples we provided! :satisfied: :sparkles: 

## Compatibility of python
- python version > `3.7`

## Environment SetUp
### Clone this project `(If you wanna run some examples!)`
- Using command: `git clone git@github.com:rainyjonne/DataSika.git`
- Manually download: clicking `Download ZIP file` from the green code button 

### Install Python
- [Install python directly](https://www.python.org/downloads/)
- [Using Pyenv](docs/envs/pyenv.md)
 
### Upgrade your pip if its version not new enough 
- [Install `pip`](https://pip.pypa.io/en/stable/installation/)
  - macOS: `python -m ensurepip --upgrade`
  - WSL, Linux: `python -m ensurepip --upgrade`

### Install our pacakge
- Just execute this command: `pip install DataSika`, then you can happily use this command with your yaml files! :tada: :confetti_ball: 
- Sika Command usage:
```
usage: sika [-h] [--input INPUT] [--output OUTPUT] [--rerun]

Build a simple pipeline by a yaml file

optional arguments:
  -h, --help       show this help message and exit
  --input INPUT    put in an input yaml file path
  --output OUTPUT  put a path for your output db
  --rerun          rerun the whole pipeline again, delete all data tables in your db file
```

## Running examples
- Making this package's command line tool works: `python setup.py install`
- Running our four examples:
  - Using command line tools:
    1. (ETL) Getting Ruby Gem Details Example: `sika --input examples/repominer.yaml`
    2. (ETL) Airbnb UK Hostings + UK Crime Data Example: `sika --input examples/airbnb-uk-crime.yaml`
    3. (EL) Getting Ruby Gem Lists Example: `sika --input examples/repominer-el.yaml`
    4. (EL) Airbnb Japan Hostings Example: `sika --input examples/airbnb-tokyo.yaml`
  - Using python scripts:
    1. (ETL) Getting Ruby Gem Details Example: `python sika/main.py --input examples/repominer.yaml`
    2. (ETL) Airbnb UK Hostings + UK Crime Data Example: `python sika/main.py --input examples/airbnb-uk-crime.yaml`
    3. (EL) Getting Ruby Gem Lists Example: `python sika/main.py --input examples/repominer-el.yaml`
    4. (EL) Airbnb Japan Hostings Example: `python sika/main.py --input examples/airbnb-tokyo.yaml`

