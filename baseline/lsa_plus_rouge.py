import pandas as pd
import numpy as np
import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
import nltk
from numpy.linalg import LinAlgError
from rouge_score import rouge_scorer


df1 = pd.read_csv('movie_database1.csv')
df2 = pd.read_csv('movie_database2.csv')
df3 = pd.read_csv('movie_database3.csv')

df = pd.concat([df1, df2])
df = pd.concat([df, df3])

# Converting years from float to int value
df['year_rotten'] = df['year_rotten'].fillna(0)
df['year_rotten'] = df['year_rotten'].astype(int)
df['year_meta'] = df['year_meta'].fillna(0)
df['year_meta'] = df['year_meta'].astype(int)

# sometimes movies have same name, but were filmed in different years, we have to drop rows that contain conflicting information

mask = (df['year_rotten'] != 0) & (df['year_meta'] != 0) & (np.abs(df['year_rotten'] - df['year_meta']) > 2)
df = df[~mask]

# remove scripts for which we don't have any summary

df.dropna(subset=['summary_rotten', 'summary_meta', 'summary_sublikescript'], how='all', inplace=True)
df = df.reset_index(drop=True)

#%% Generate summaries


# Initialize the LexRank summarizer
summarizer = LsaSummarizer()

# Generate a summary for each script
for i, row in df.iterrows():
    print(i)
    # Split the script into scenes
    script = row['script']
    #scenes = re.split(r'\n(?=[A-Z ]+ - [A-Z ]+)', script.strip())
    scenes = re.split(r'\n(?=[A-Z ]+(?:\/[A-Z]+)? - [A-Z ]+)', script.strip())
    
    full_summary = ""
    
    if len(scenes) == 1:
        twenty_perc = int(0.2 * len(scenes[0]))
        scene = scenes[0][:twenty_perc]
        # Preprocess the scene text
        scene = scene.lower()  # convert to lowercase
        scene = re.sub(r"[^a-z0-9.,\s]", "", scene)  # remove non-alphanumeric characters except dots and commas
        scene = re.sub(r"\s+", " ", scene)  # remove extra whitespace
        # Initialize the parser and tokenizer for the scene
        parser = PlaintextParser.from_string(scene, Tokenizer("english"))
        
        try:
            summary = summarizer(parser.document, sentences_count=2)
            summary_text = " ".join(str(sentence) for sentence in summary).replace("<Sentence: ", "").replace(">", "")
            full_summary += "{}\n".format(summary_text)
        except LinAlgError:
            print(f"Skipping script {i} due to SVD convergence error.")
            continue
    else:
    # Generate a summary for each scene
        for j, scene in enumerate(scenes):
            if j == 0:
                continue
            
            # Preprocess the scene text
            scene = scene.lower()  # convert to lowercase
            scene = re.sub(r"[^a-z0-9.,\s]", "", scene)  # remove non-alphanumeric characters except dots and commas
            scene = re.sub(r"\s+", " ", scene)  # remove extra whitespace
            # Initialize the parser and tokenizer for the scene
            parser = PlaintextParser.from_string(scene, Tokenizer("english"))
            
            try:
                summary = summarizer(parser.document, sentences_count=2)
                summary_text = " ".join(str(sentence) for sentence in summary).replace("<Sentence: ", "").replace(">", "")
                if j < 3:
                    full_summary += "{}\n".format(summary_text)
                else:
                    break
            except LinAlgError:
                print(f"Skipping script {i} due to SVD convergence error.")
                break
        
    # Save the full summary in a new column
    df.loc[i, 'generated_summary'] = full_summary

#%% Evaluation of generated summaries


# Initialize the ROUGE scorer
scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

# Calculate the ROUGE scores for each row in the DataFrame
for i, row in df.iterrows():
    try:
        # Tokenize the summaries into sentences
        ref_summary_rot = nltk.sent_tokenize(row['summary_rotten'].lower())
        gen_summary = nltk.sent_tokenize(row['generated_summary'])

        # Calculate the ROUGE scores
        scores = scorer.score(' '.join(gen_summary), ' '.join(ref_summary_rot))

        # Store the scores in the DataFrame
        df.loc[i, 'rouge-1-rot'] = scores['rouge1'].fmeasure
        df.loc[i, 'rouge-2-rot'] = scores['rouge2'].fmeasure
        df.loc[i, 'rouge-l-rot'] = scores['rougeL'].fmeasure

    except ValueError:
        print(f"Skipping script {i} due to ValueError.")
    except Exception as e:
        print(f"Skipping script {i} due to error: {e}")
        
    
    try:
        # Tokenize the summaries into sentences
        ref_summary_meta = nltk.sent_tokenize(row['summary_meta'].lower())
        gen_summary = nltk.sent_tokenize(row['generated_summary'])

        # Calculate the ROUGE scores
        scores = scorer.score(' '.join(gen_summary), ' '.join(ref_summary_meta))

        # Store the scores in the DataFrame
        df.loc[i, 'rouge-1-meta'] = scores['rouge1'].fmeasure
        df.loc[i, 'rouge-2-meta'] = scores['rouge2'].fmeasure
        df.loc[i, 'rouge-l-meta'] = scores['rougeL'].fmeasure

    except ValueError:
        print(f"Skipping script {i} due to ValueError.")
    except Exception as e:
        print(f"Skipping script {i} due to error: {e}")
        
        
    try:
        # Tokenize the summaries into sentences
        ref_summary_sub = nltk.sent_tokenize(row['summary_sublikescript'].lower())
        gen_summary = nltk.sent_tokenize(row['generated_summary'])

        # Calculate the ROUGE scores
        scores = scorer.score(' '.join(gen_summary), ' '.join(ref_summary_sub))

        # Store the scores in the DataFrame
        df.loc[i, 'rouge-1-sub'] = scores['rouge1'].fmeasure
        df.loc[i, 'rouge-2-sub'] = scores['rouge2'].fmeasure
        df.loc[i, 'rouge-l-sub'] = scores['rougeL'].fmeasure

    except ValueError:
        print(f"Skipping script {i} due to ValueError.")
    except Exception as e:
        print(f"Skipping script {i} due to error: {e}")
    
#%% Visualisation

import matplotlib.pyplot as plt

# Define the reference summaries and corresponding columns in the DataFrame
ref_summaries = ['rot', 'meta', 'sub']
ref_labels = ['roten tomatoes', 'metacritics', 'subslikescript']
rouge_cols = ['rouge-1', 'rouge-2', 'rouge-l']

# Calculate the average ROUGE scores for each reference summary
avg_scores = []
for ref_summary in ref_summaries:
    ref_cols = [f'{rouge}-{ref_summary}' for rouge in rouge_cols]
    ref_scores = df[ref_cols].mean().values.tolist()
    avg_scores.append(ref_scores)

# Create a bar plot to show the average ROUGE scores for each reference summary
fig, ax = plt.subplots(figsize=(8, 6))
x = range(len(ref_summaries))
width = 0.2
colors = ['r', 'g', 'b']

for i in range(len(rouge_cols)):
    ax.bar([xi + (i * width) for xi in x], [s[i] for s in avg_scores], width, color=colors[i], label=rouge_cols[i])

#ax.set_xticks(x)
plt.xticks([r + width for r in x])

ax.set_xticklabels(ref_labels)
ax.set_xlabel('Reference Summary')
ax.set_ylabel('Average F-measure')
ax.legend()

plt.show()











  