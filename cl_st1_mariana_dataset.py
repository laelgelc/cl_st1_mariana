import argparse
import re
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument(
    '--input_file', help='The S3 URI of the input file.')
args = parser.parse_args()

input_filename = args.input_file
suffix = '_pt'

def add_suffix(filename):
    # Extract the base filename without the extension
    base_filename = re.match(r'^([A-Za-z0-9-_,\s]+)\.[A-Za-z]{1,5}$', filename).group(1)
    
    # Append suffix to the base filename
    new_filename = f'{base_filename}{suffix}'
    
    # Add the original file extension back
    new_filename += re.search(r'\.[A-Za-z]{1,5}$', filename).group()
    
    return new_filename

output_filename = add_suffix(input_filename)

df_tweets_raw_data = pd.read_json(input_filename, lines=True)

df_tweets_raw_data['id'] = df_tweets_raw_data['id'].astype(str)

df_tweets_raw_data = df_tweets_raw_data[df_tweets_raw_data['lang'] == 'pt'].reset_index(drop=True)

# Flatten the nested JSON 'user' attribute
df_tweets_raw_data_flattened_user = pd.json_normalize(df_tweets_raw_data['user'])

# Extract the 'screen_name' attribute
username = df_tweets_raw_data_flattened_user['screen_name']

# Create a new column 'username'
df_tweets_raw_data['username'] = username

# Extract the 'id_str' attribute
author_id = df_tweets_raw_data_flattened_user['id_str']

# Create a new column 'username'
df_tweets_raw_data['author_id'] = author_id

# Construct the tweet URL using the tweet ID and user's screen name
df_tweets_raw_data['tweet_url'] = (
    'https://twitter.com/' + 
    df_tweets_raw_data['username'] + 
    '/status/' + 
    df_tweets_raw_data['id']
)

df_tweets_raw_data[['created_at', 'author_id', 'username', 'tweet_url', 'text']].to_json(output_filename, orient='records', lines=True)