import pandas as pd
import os
import json
from tqdm.auto import tqdm
import networkx as nx
import semanticscholar as sch
import urllib
import json
import requests
import glob
import itertools
import numpy as np
from pandarallel import pandarallel
from fuzzywuzzy import fuzz, process
import string

# Path to ICLR data
filepath = "/nethome/dkartchner3/school/epi/citation-networks-idea-propogation/data/mag_papers/iclr.json"
papers = json.load(open(filepath, 'r'))

# Table to remove punctuation
table = str.maketrans('', '', string.punctuation)
counter = 0

# Keep track of relevant fields
paper_titles = []
paper_authors = []
paper_ids = []
paper_aff_names = []
paper_aff_ids = []

# Look at all papers
for p in papers['entities']:
    # We only want papers from 2018
    if p['Y'] == 2018:
        counter += 1
        # Grab relevant fields
        paper_titles.append(p['Ti'].translate(table).lower())
        paper_authors.append(' '.join([a['AuN'] for a in p['AA']]))
        paper_ids.append(p['Id'])
        paper_aff_ids.append([a['AfId'] for a in p['AA'] if a['AfId'] is not None])
        paper_aff_names.append([a['AfN'] for a in p['AA'] if a['AfId'] is not None])

print("ICLR papers in MAG:", counter)

# Count papers
iters = 0

# Collect data on accepted papers and their ratings
accepted_titles = []
accepted_authors = []
reviews = []

with open("../../data/paper_quality/iclr2018_metadata.jsonl", 'r') as f:
    for line in f:
        # Load paper
        paper = json.loads(line)
        
        # Get info on accepted/invited to workshop papers
        if paper['decision'].lower() != 'reject':
            accepted_titles.append(paper['submission_content']['title'].translate(table).lower())
            accepted_authors.append(' '.join([a.translate(table).lower() for a in paper['submission_content']['authors']]))
            reviews.append(paper['review_ratings'])
            iters += 1
        
print("Non-rejected submissions to ICLR main conference:", iters)

### Find best match between datasets with fuzzy string matching
paper_scores = {}
for paper, author, review in tqdm(zip(accepted_titles, accepted_authors, reviews)):
    
    # Get closest matched title
    winning_paper = process.extractOne(paper, paper_titles, scorer=fuzz.ratio)
    paper_index = paper_titles.index(winning_paper[0])
    
    # Get closest author match
    winning_author = process.extractOne(author, paper_authors, scorer=fuzz.token_sort_ratio)
    author_index = paper_authors.index(winning_author[0])
    
    # Get average review score
    review_score = np.mean([int(r[0]) for r in review])
    
    # Create dict of scores
    paper_scores[paper] = {'title_match': winning_paper[0],
                           'title_score': winning_paper[1],
                           'title_match_id': paper_ids[paper_index],
                           'authors': author,
                           'author_match': winning_author[0],
                           'author_score': winning_author[1],
                           'author_match_id': paper_ids[author_index],
                           'review_score': review_score, 
                           'matched_aff_ids':paper_aff_ids[paper_index], 
                           'matched_aff_names':paper_aff_names[paper_index]}


# Make results into a dataframe 
matches = pd.DataFrame([(p['title_match_id'], 
                         name, 
                         p['review_score'], 
                         p['matched_aff_ids'], 
                         p['matched_aff_names']) 
                        for name, p in paper_scores.items() 
                        if p['title_score'] > .9 ], columns=['mag_id',
                                                             'title',
                                                             'avg_review_score', 
                                                             'afids', 
                                                             'afns'])

# Throw away papers with no affiliated author and save results
matches = matches[matches.afids.map(lambda x: len(x)) > 0].reset_index(drop=True)
matches.to_pickle('../../data/paper_quality/iclr_matched_papers.pkl')
