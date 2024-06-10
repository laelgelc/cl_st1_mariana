# Corpus Linguistics - Study 1 - Mariana - Dataset preparation - Only Portuguese

## Importing the required libraries

import pandas as pd

## Data wrangling

### Consolidating multiple JSONL files into one JSONL file - code snippets

#Note: You have to download and open this Jupyter Notebook on JupyterLab (provided as part of Anaconda Distribution) to visualise the procedure

#### In an Amazon EC2 instance, create the working directories

#mkdir mari
#mkdir mariout
#cd mari

#### Iterate this line of code from `2016_1` to `2016_12`

#aws s3 cp s3://gelcawsemr/2016_1/filtered_tweets.jsonl/ . --recursive && cat *.json > mari2016_1.jsonl && aws s3 cp mari2016_1.jsonl s3://laelgelcawsemrmariana/ && mv mari2016_1.jsonl ../mariout/ && rm *

#### Change to `mariout`

#cd ../mariout

### Importing the tweet raw data into a dataframe

archive = 'mari2016_1.jsonl'
archive_pt = 'mari2016_1_pt.jsonl'

df_tweets_raw_data = pd.read_json(archive, lines=True)

### Dropping unnecessary columns

### Keeping only the tweets in Portuguese

df_tweets_raw_data = df_tweets_raw_data[df_tweets_raw_data['lang'] == 'pt'].reset_index(drop=True)

### Creating the file `mari2016_pt.jsonl`

df_tweets_raw_data.to_json(archive_pt, orient='records', lines=True)
