# Corpus Linguistics - Study 1 - Mariana

## Prerequisites

#Make sure the prerequisites in [CL_LMDA_prerequisites](https://github.com/laelgelc/laelgelc/blob/main/CL_LMDA_prerequisites.ipynb) are satisfied.

## Dataset

#Please download the following dataset (Right-click on the link and choose `Save link as` to download the corresponding file):
#- [mari2016_2022_pt.jsonl](https://laelgelcawsemrmariana.s3.sa-east-1.amazonaws.com/mari2016_2022_pt.jsonl)

## Importing the required libraries

import pandas as pd
import demoji
import re
import os
from collections import Counter

## Data wrangling

### Importing the tweet raw data into a dataframe

df_tweets_raw_data = pd.read_json('mari2016_2022_pt.jsonl', lines=True)

df_tweets_raw_data.head(5)

df_tweets_raw_data.shape

#### Inspecting a few tweets

inspected_row = 1
print('username:' + df_tweets_raw_data.loc[inspected_row, 'username'])
print('text:' + df_tweets_raw_data.loc[inspected_row, 'text'])
print('tweet_url:' + df_tweets_raw_data.loc[inspected_row, 'tweet_url'])

### Inspecting the dataset and eliminating malformed data

#### Checking if data types are consistent

df_tweets_raw_data.dtypes

#### Identifying rows that are empty in column `text`

print(df_tweets_raw_data['text'].isnull().sum())

df_tweets_raw_data[df_tweets_raw_data['text'].isnull()]

#### Dropping the rows that are empty in the column `text`

# Drop the rows whose column 'text' is NaN
df_tweets_raw_data = df_tweets_raw_data.dropna(subset=['text'])

# Reset the index
df_tweets_raw_data = df_tweets_raw_data.reset_index(drop=True)

print(df_tweets_raw_data['text'].isnull().sum())

#### Removing specific Unicode characters

#The dataset may need to be cleaned of invisible Unicode characters.

##### Detecting `U+2066` and `U+2069` characters

#- [U+2066](https://www.compart.com/en/unicode/U+2066)
#- [U+2069](https://www.compart.com/en/unicode/U+2069)

#Please refer to:
#- [Python RegEx](https://www.w3schools.com/python/python_regex.asp)
#- [regex101](https://regex101.com/)
#- [RegExr](https://regexr.com/)

# Defining a function to detect specific Unicode characters
def extract_unicode_characters(df, column_name):
    unicode_chars = Counter()  # Initialize a Counter to store Unicode character counts

    for value in df[column_name]:
        if isinstance(value, str):
            # Use RegEx to find non-ASCII characters (Unicode)
#            non_ascii_chars = re.findall(r'[^\x00-\x7F]+', value)
            # Use RegEx to find specific Unicode characters - adjust the expression accordingly
            specific_unicode_chars = re.findall(r'[\u2066\u2069]', value)
            unicode_chars.update(specific_unicode_chars)

    return unicode_chars

# Inspect the dataframe for specific Unicode characters
unicode_counts = extract_unicode_characters(df_tweets_raw_data, 'text')

# Print the results
for char, count in unicode_counts.items():
    print(f'Character {char}: Count = {count}')

##### Removing `U+2066` and `U+2069` characters

# Defining a function to remove specific Unicode characters
def remove_specific_unicode(input_line):
    # Using RegEx to replace specific Unicode characters - adjust the expression accordingly
    cleaned_line = re.sub(r'[\u2066\u2069]', '', input_line)
    return cleaned_line

# Removing specific Unicode characters
df_tweets_raw_data['text'] = df_tweets_raw_data['text'].apply(remove_specific_unicode)

#### Replacing the `LF` character by a space

#Some tweets, especially the retweeted ones, contain multiple lines of text.

# Defining a function to replace the `LF` character by a space
def remove_cr_lf(input_line):
    # Using RegEx to replace LF by a space
    cleaned_line = re.sub(r'\n', ' ', input_line)
    return cleaned_line

# Applying the function to the 'text' column in your DataFrame
df_tweets_raw_data['text'] = df_tweets_raw_data['text'].apply(remove_cr_lf)

df_tweets_raw_data

### Dropping duplicates

#### Retweets

#Retweets bear the RegEx pattern `'\bRT @\w+\s*:'gm` or `'\bRT @\w+\s':"gm` at the beginning of the column `text`. They should be often dropped because they are duplicates of the original tweets. In the case of this study, though, the dataset may not include the original tweets because it is a 1% random sample. Therefore, only the first occurrence of the retweet is being kept.

# Create a new column 'no_retweet' containing the contents of the column 'text' without any preceding 'RT @mentions:'
df_tweets_raw_data['no_retweet'] = df_tweets_raw_data['text'].str.replace(r'\bRT @\w+\s*:|\brt @\w+\s*:', '', regex=True)

# Drop duplicate rows except the first occurrence based on 'no_mention'
df_tweets_raw_data.drop_duplicates(subset='no_retweet', keep='first', inplace=True)
df_tweets_raw_data = df_tweets_raw_data.reset_index(drop=True)
df_tweets_raw_data.shape

#### Duplicate tweets

#The dataset was build in a way that if a certain tweet had more than one photo, one copy of the tweet was included per unique photo. Since we are concerned with analysing just the text, those duplicates should be removed. Tweets that bear the same 'tweet_url' are duplicates - we are going to keep only the first.

df_tweets_raw_data.drop_duplicates(subset='tweet_url', keep='first', inplace=True)
df_tweets_raw_data = df_tweets_raw_data.reset_index(drop=True)
df_tweets_raw_data.shape

#### @mentioned tweets

#A few users @mention copies of tweets towards other specific users creating multiple copies of the same tweet - those duplicates should be removed.

# Create a new column 'no_mention' containing the contents of the column 'text' without any preceding @mentions
df_tweets_raw_data['no_mention'] = df_tweets_raw_data['text'].str.replace(r'@\w+\s*', '', regex=True)

# Drop duplicate rows except the first occurrence based on 'no_mention'
df_tweets_raw_data.drop_duplicates(subset='no_mention', keep='first', inplace=True)
df_tweets_raw_data = df_tweets_raw_data.reset_index(drop=True)
df_tweets_raw_data.shape

## Sampling the raw data according to filtering expressions

# Defining the filtering expressions
#filter_words = ['venezuelano', 'venezuelana', 'aporofobia', 'crise', 'discriminação', 'estigma', 'xenofobia', 'roraizuela', 'preconceito']
filter_words = ['venezuelano', 'venezuelana', 'aporofobia', 'discriminação', 'estigma', 'xenofobia', 'roraizuela']

# Creating a boolean mask for filtering
mask = df_tweets_raw_data['text'].str.contains('|'.join(filter_words), case=False)

# Applying the mask to create 'df_tweets_filtered'
df_tweets_filtered = df_tweets_raw_data[mask]
df_tweets_filtered = df_tweets_filtered.reset_index(drop=True)

df_tweets_filtered

### Exporting the filtered data into a file for inspection

df_tweets_filtered.to_csv('tweets_emojified.tsv', sep='\t', index=False)

#The original set of filter words resulted in 496,811 tweets. According to Professor Tony, the recommended number of texts should fall between 20 and 50 thousand tweets. Inspecting the file `tweets_emojified.tsv` as follows, it has been determined that the words 'crise' and 'preconceito' are responsible for the majority of the selected tweets. Therefore, it has been decided to remove them.

#Note: You have to download and open this Jupyter Notebook on JupyterLab (provided as part of Anaconda Distribution) to visualise the procedure

#eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads/cl_st1_mariana$ ll
#total 1769052
#drwxrwxrwx 1 eyamrog eyamrog        512 Jul  8 16:44 ./
#drwxrwxrwx 1 eyamrog eyamrog        512 Jul  8 16:38 ../
#drwxrwxrwx 1 eyamrog eyamrog        512 Jul  8 16:24 .ipynb_checkpoints/
#-rwxrwxrwx 1 eyamrog eyamrog      66359 Jul  8 16:44 CL_St1_Mariana.ipynb*
#-rwxrwxrwx 1 eyamrog eyamrog 1609093422 Jul  8 16:21 mari2016_2022_pt.jsonl*
#-rwxrwxrwx 1 eyamrog eyamrog  202338605 Jul  8 16:43 tweets_emojified.tsv*
#eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads/cl_st1_mariana$ grep -ic "venezuelano" tweets_emojified.tsv
#14661
#eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads/cl_st1_mariana$ grep -ic "venezuelana" tweets_emojified.tsv
#5327
#eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads/cl_st1_mariana$ grep -ic "aporofobia" tweets_emojified.tsv
#150
#eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads/cl_st1_mariana$ grep -ic "crise" tweets_emojified.tsv
#338401
#eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads/cl_st1_mariana$ grep -ic "discriminação" tweets_emojified.tsv
#7490
#eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads/cl_st1_mariana$ grep -ic "estigma" tweets_emojified.tsv
#6017
#eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads/cl_st1_mariana$ grep -ic "xenofobia" tweets_emojified.tsv
#16018
#eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads/cl_st1_mariana$ grep -ic "roraizuela" tweets_emojified.tsv
#6
#eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads/cl_st1_mariana$ grep -ic "preconceito" tweets_emojified.tsv
#110800
#eyamrog@Rog-ASUS:/mnt/c/Users/eyamr/Downloads/cl_st1_mariana$

## Replacing emojis

### Demojifying the column `text`

# Defining a function to demojify a string
def demojify_line(input_line):
    demojified_line = demoji.replace_with_desc(input_line, sep='<em>')
    return demojified_line

df_tweets_filtered['text'] = df_tweets_filtered['text'].apply(demojify_line)

#### Exporting the filtered data into a file for inspection

df_tweets_filtered.to_csv('tweets_demojified1.tsv', sep='\t', index=False)

### Separating the demojified strings with spaces

# Defining a function to separate the demojified strings with spaces
def preprocess_line(input_line):
    # Add a space before the first delimiter '<em>', if it is not already preceded by one
    preprocessed_line = re.sub(r'(?<! )<em>', ' <em>', input_line)
    # Add a space after the first delimiter '<em>', if it is not already followed by one
    preprocessed_line = re.sub(r'<em>(?! )', '<em> ', preprocessed_line)
    return preprocessed_line

# Separating the demojified strings with spaces
df_tweets_filtered['text'] = df_tweets_filtered['text'].apply(preprocess_line)

#### Exporting the filtered data into a file for inspection

df_tweets_filtered.to_csv('tweets_demojified2.tsv', sep='\t', index=False)

### Formatting the demojified strings

# Defining a function to format the demojified string
def format_demojified_string(input_line):
    # Defining a function to format the demojified string using RegEx
    def process_demojified_string(s):
            # Lowercase the string
            s = s.lower()
            # Replace spaces and colons followed by a space with underscores
            s = re.sub(r'(: )| ', '_', s)
            # Add the appropriate prefixes and suffixes
            s = f'EMOJI{s}e'
            return s

    # Use RegEx to find and process each demojified string
    processed_line = re.sub(r'<em>(.*?)<em>', lambda match: process_demojified_string(match.group(1)), input_line)
    return processed_line

# Formatting the demojified strings
df_tweets_filtered['text'] = df_tweets_filtered['text'].apply(format_demojified_string)

### Replacing the `pipe` character by the `-` character in the `text` column

#Further on, a few columns of the dataframe are going to be exported into the file `tweets.txt` whose columns need to be delimited by the `pipe` character. Therefore, it is recommended that any occurrences of the `pipe` character in the `text` column are replaced by another character.

# Defining a function to replace the 'pipe' character by the '-' character
def replace_pipe_with_hyphen(input_string):
    modified_string = re.sub(r'\|', '-', input_string)
    return modified_string

# Replacing the 'pipe' character by the '-' character
df_tweets_filtered['text'] = df_tweets_filtered['text'].apply(replace_pipe_with_hyphen)


#### Exporting the filtered data into a file for inspection

df_tweets_filtered.to_csv('tweets_demojified3.tsv', sep='\t', index=False)

## Tokenising

#Please refer to [What is tokenization in NLP?](https://www.analyticsvidhya.com/blog/2020/05/what-is-tokenization-nlp/).

# Defining a function to tokenise a string
def tokenise_string(input_line):
    # Replace URLs with placeholders
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\b'
    placeholder = '<URL>'  # Choose a unique placeholder
    urls = re.findall(url_pattern, input_line)
    tokenised_line = re.sub(url_pattern, placeholder, input_line)  # Replace URLs with placeholders
    
    # Replace curly quotes with straight ones
    tokenised_line = tokenised_line.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")
    # Separate common punctuation marks with spaces
    tokenised_line = re.sub(r'([.\!?,"\'/()])', r' \1 ', tokenised_line)
    # Add a space before '#'
    tokenised_line = re.sub(r'(?<!\s)#', r' #', tokenised_line)  # Add a space before '#' if it is not already preceded by one
    # Reduce extra spaces by a single space
    tokenised_line = re.sub(r'\s+', ' ', tokenised_line)
    
    # Replace the placeholders with the respective URLs
    for url in urls:
        tokenised_line = tokenised_line.replace(placeholder, url, 1)
    
    return tokenised_line

# Tokenising the strings
df_tweets_filtered['text'] = df_tweets_filtered['text'].apply(tokenise_string)

## Creating the files `file_index.txt` and `tweets.txt`

### Creating column `text_id`

df_tweets_filtered['text_id'] = 't' + df_tweets_filtered.index.astype(str).str.zfill(6)

### Creating column `conversation`

df_tweets_filtered['author_id'] = df_tweets_filtered['author_id'].astype(str)

df_tweets_filtered['conversation'] = 'v:' + df_tweets_filtered['author_id'].str.replace('id_', '')

### Creating column `date`

# Convert 'created_at' to datetime format
df_tweets_filtered['created_at'] = pd.to_datetime(df_tweets_filtered['created_at'])

# Extract the date part (without time) into a new column 'date'
df_tweets_filtered['date'] = df_tweets_filtered['created_at'].dt.date

# Add the prefix 'd:' to the 'date' values
df_tweets_filtered['date'] = 'd:' + df_tweets_filtered['date'].astype(str)

### Creating column `text_url`

df_tweets_filtered['text_url'] = 'url:' + df_tweets_filtered['tweet_url']

### Creating column `user`

df_tweets_filtered['user'] = 'u:' + df_tweets_filtered['username']

### Creating column `content`

df_tweets_filtered['content'] = 'c:' + df_tweets_filtered['text']

### Reordering the created columns

#Please refer to:
#- [Python - List Comprehension 1](https://www.w3schools.com/python/python_lists_comprehension.asp)
#- [Python - List Comprehension 2](https://treyhunner.com/2015/12/python-list-comprehensions-now-in-color/)

# Reorder the columns (we use list comprehension to create a list of all columns except 'text_id', 'variable', 'date' and 'text_url')
df_tweets_filtered = df_tweets_filtered[['text_id', 'conversation', 'date', 'text_url', 'user', 'content'] + [col for col in df_tweets_filtered.columns if col not in ['text_id', 'conversation', 'date', 'text_url', 'user', 'content']]]

df_tweets_filtered

### Creating the file `file_index.txt`

df_tweets_filtered[['text_id', 'conversation', 'date', 'text_url']].to_csv('file_index.txt', sep=' ', index=False, header=False, encoding='utf-8', lineterminator='\n')

### Creating the file `tweets.txt`

folder = 'tweets'
try:
    os.mkdir(folder)
    print(f'Folder {folder} created!')
except FileExistsError:
    print(f'Folder {folder} already exists')

#Note: The parameters `doublequote=False` and `escapechar=' '` are required to avoid that the column content is doublequoted with '"' in sentences that use characters that need to be escaped such as double quote '"' itself - this causes a malformed response from TreeTagger.

df_tweets_filtered[['text_id', 'conversation', 'date', 'user', 'content']].to_csv(f'{folder}/tweets.txt', sep='|', index=False, header=False, encoding='utf-8', lineterminator='\n', doublequote=False, escapechar=' ')
