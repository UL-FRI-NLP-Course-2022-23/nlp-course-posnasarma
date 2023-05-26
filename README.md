# Natural language processing course 2022/23: `An Automatic Movie Summary Generator`

Team members:
 * `Luka Pavićević`, `63220489`, `lp83866@student.uni-lj.si`
 * `Andrija Stanišić`, `63220491`, `as86041@student.uni-lj.si`
 * `Stefanela Stevanović`, `63220492`, `ss51676@student.uni-lj.si`
 
Group public acronym/name: `PosnaSarma`
 > This value will be used for publishing marks/scores. It will be known only to you and not you colleagues.

# Project Overview

The goal of this project is to create a summary generator for the movies without any human interaction in the process. We plan to achieve this goal by applying different natural language processing methods. For the base line we have implemented Latent Semantic Analysis (LSA) and for the final implementation we have used a transformer based model which has shown promising results. The transformer-based model used is T5-small, which was imported from the Hugging Face and fine-tuned on our dataset.  

# Usage Guide

We have collected our dataset from different sources and we have pushed it completely on the github, so you don't have to performe any web scraping yourself. If you wish to download the dataset yourself that can be done in four steps. To download the movie scripts, you should run the **Jupyter Notebook** in the *scripts* repository. The second step is downloading the subtitles, this can be done by running the provided **Jupyter Notebook** from the directory *subslikescript*. This method will download subtitles and summaries. Since not all the summaries were available on the first site we have downloaded more summaries from **Rottent Tomatoes** and **MetaCritic**, these summaries can be obtained by running provied **Jupyter Notebook** in the repositories *metacritic* and *rottentomatoes* respectivly. 

To performe the natural language processing you should look at the directories *baseline* and *main*. In the *baseline* you will find our Latent Semantic Analysis (LSA). This analysis can be done by running the provided *lsa_plus_rouge.py* script. As for the *main*, there you will find our fine tunned **T5-small** model that was imported from the Hugging Face. We have fine tunned our model on **Google Colab**, since the model parameters are 5 GB in size we were not able to provide the model. But if you wish you can do the fine tunning on **Google Colab**, and the whole proces of training and validation should take about two hours. 

# Installation Instructions

The following python libraries are required in order to run our code. The requirements are split based on what part of the code you want to run.
	1. Scrip acquisition:
	   - Requests
	   - BeautifulSoup 4
	   - tqdm
	2. Subtitle acquisition:
	   - Requests
	   - BeautifulSoup 4
	   - tqdm
	   - Pandas
	3. MetaCritic/RottenTomatoes summary acquisition:
	   - Matplotlib
	   - Numpy
	   - Selenium
	4. Baseline model:
	   - Pandas 
	   - Sumy
	   - Numpy
	   - NLTK
	   - Rouge_score
	5. Main model:
	   - Transformers 
	   - Datasets 
	   - Evaluate 
	   - Rouge_score
	   - Accelerate
	   - Sentencepiece
	   - Bert_score
	   - Pandas

# Contact Information

If you have any questions and/or suggestions reggarding our imeplementation you can contact any of the contributors, and we would be more than happy to help you. 