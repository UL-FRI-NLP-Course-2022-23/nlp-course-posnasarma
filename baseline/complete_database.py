# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 02:30:22 2023

@author: astanisic
"""

# All scripts to table

import os
import pandas as pd

directory_path = '../scripts/new_names/scripts'

filenames = []
contents = []

for filename in os.listdir(directory_path):
    if filename.endswith('.txt'):
        filenames.append(filename)
        with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as file:
            contents.append(file.read())

table1 = pd.DataFrame({'title': filenames, 'script': contents})
table1['title'] = table1['title'].str[:-4]

#%% Summary from metacritics

import pandas as pd
import json

# Load JSON data from file
with open('../metacritic/metacritic_data2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(data)

# Select columns 'title' and 'summary'
table2 = df[['title', 'genre', 'year', 'summary']]

# apply string operations to the 'title' column
table2['title'] = table2['title'].str.lower()
table2['title'] = table2['title'].str.replace('.', '')
table2['title'] = table2['title'].str.replace(',', '')
table2['title'] = table2['title'].str.replace("'", "")
table2['title'] = table2['title'].str.replace(':', '')
table2['title'] = table2['title'].str.replace(' ', '-')

table2 = table2.rename(columns={'year': 'year_meta'})
table2 = table2.rename(columns={'summary': 'summary_meta'})
table2 = table2.rename(columns={'genre': 'genre_meta'})

# Print table
print(table2)
#%% Summary from rotten tomatos

import pandas as pd
import json

# Load JSON data from file
with open('../rottentomatoes/movie_data_rotten.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(data)

# Select columns 'title' and 'summary'
table3 = df[['link', 'genre', 'year', 'summary']]

#df['title'] = df['link'].apply(lambda x: x.split("/")[-1])
table3['title'] = table3['link'].astype(str).str.split('/').str[-1]
table3['title'] = table3['title'].str.replace('_', '-')

table3 = table3.drop(['link'], axis=1)

table3 = table3.rename(columns={'year': 'year_rotten'})
table3 = table3.rename(columns={'summary': 'summary_rotten'})
table3 = table3.rename(columns={'genre': 'genre_rotten'})

table3['title'] = table3['title'].replace('godfather-part-ii', 'the-godfather-part-ii', regex=False)
table3['title'] = table3['title'].replace('godfather-part-iii', 'the-godfather-part-iii', regex=False)

# Print table
print(table3)
#%% Merging
database = pd.merge(table1, table3, on='title', how='left')
database = pd.merge(database, table2, on='title', how='left')
#%% Adding summary and subtitles from SUBSLIKESCRIPT

import os

# create a new column for the script content
database['subtitle'] = ''
database['summary_sublikescript'] = ''

# loop through each row of the table
for i, row in database.iterrows():
    # get the title of the movie
    title = row['title']
    # load the script file into the 'script' column of the table
    sub_path = os.path.join('../subslikescript/subtitles', f"{title}.txt")
    try:
        with open(sub_path, 'r', encoding='utf-8') as f:
            sub_content = f.read()
            database.at[i, 'subtitle'] = sub_content
    except FileNotFoundError:
        pass
        
    sum_path = os.path.join('../subslikescript/summary', f"{title}.txt")
    try:
        with open(sum_path, 'r', encoding='utf-8') as f:
            sum_content = f.read()
            database.at[i, 'summary_sublikescript'] = sum_content
    except FileNotFoundError:
        pass
    
#%%
database.to_csv('movie_database.csv', index=False)







