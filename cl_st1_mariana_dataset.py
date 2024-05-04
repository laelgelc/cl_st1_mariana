# Corpus Linguistics - Study 1 - Mariana - Dataset preparation

## Tweet Object documentation

#Please refer to [Tweet Object](https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet)

## Importing the required libraries

import pandas as pd

## Data wrangling

### Importing the tweet raw data into a dataframe

df_tweets_raw_data = pd.read_json('mari20192020.jsonl', lines=True)

#df_tweets_raw_data.head(5)

#df_tweets_raw_data.shape

### Checking if data types are consistent

#df_tweets_raw_data.dtypes

#### Converting `id` column's data type to `str` for future use

#Note: For some unknown reason, pandas has imported the attribute `id_str` incorrectly in some cases. Therefore, `id` is  being used instead.

df_tweets_raw_data['id'] = df_tweets_raw_data['id'].astype(str)

### Dropping unnecessary columns

#### Listing the columns

#df_tweets_raw_data.columns.values.tolist()

#### Selecting the columns that are being dropped

df_tweets_raw_data = df_tweets_raw_data.drop(columns=[
#    'created_at',
    'entities',
    'favorite_count',
    'favorited',
    'filter_level',
#    'id',
    'id_str',
    'is_quote_status',
#    'lang',
    'quote_count',
    'reply_count',
    'retweet_count',
    'retweeted',
    'retweeted_status',
    'source',
#    'text',
    'timestamp_ms',
    'truncated',
#    'user',
    'quoted_status',
    'quoted_status_id',
    'quoted_status_id_str',
    'quoted_status_permalink',
    'extended_tweet',
    'display_text_range',
    'extended_entities',
    'possibly_sensitive',
    'in_reply_to_screen_name',
    'in_reply_to_user_id',
    'in_reply_to_user_id_str',
    'in_reply_to_status_id',
    'in_reply_to_status_id_str',
    'coordinates',
    'geo',
    'place',
#    'withheld_in_countries'
])

#df_tweets_raw_data.columns.values.tolist()

### Listing the values of the parameter `lang`

#df_tweets_raw_data['lang'].unique()

### Keeping only the tweets in Portuguese

df_tweets_raw_data = df_tweets_raw_data[df_tweets_raw_data['lang'] == 'pt'].reset_index(drop=True)

### Extracting the column `username`

# Flatten the nested JSON 'user' attribute
df_tweets_raw_data_flattened_user = pd.json_normalize(df_tweets_raw_data['user'])

# Extract the 'screen_name' attribute
username = df_tweets_raw_data_flattened_user['screen_name']

# Create a new column 'username'
df_tweets_raw_data['username'] = username

### Extracting the column `author_id`

# Extract the 'id_str' attribute
author_id = df_tweets_raw_data_flattened_user['id_str']

# Create a new column 'username'
df_tweets_raw_data['author_id'] = author_id

### Extracting the column `tweet_url`

# Construct the tweet URL using the tweet ID and user's screen name
df_tweets_raw_data['tweet_url'] = (
    'https://twitter.com/' + 
    df_tweets_raw_data['username'] + 
    '/status/' + 
    df_tweets_raw_data['id']
)

#df_tweets_raw_data

### Inspecting the data

#inspected_row = 450
#print('username:' + df_tweets_raw_data.loc[inspected_row, 'username'])
#print('text:' + df_tweets_raw_data.loc[inspected_row, 'text'])
#print('tweet_url:' + df_tweets_raw_data.loc[inspected_row, 'tweet_url'])

### Creating the file `mari20192020.tsv`

df_tweets_raw_data[['created_at', 'author_id', 'username', 'tweet_url', 'text']].to_csv('mari20192020.tsv', sep='\t', index=False, encoding='utf-8', lineterminator='\n')
