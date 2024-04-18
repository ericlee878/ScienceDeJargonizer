## main file for collecting data ##

import time 
import random
import requests
from bs4 import BeautifulSoup
import json
from old_utils import *

# dictionary that stores the metadata
metadatas = {}

# gets the ids of the articles in specific dateframe
arxiv_ids = get_arxiv_ids("2024-03-01", "2024-03-01")

# iterates through all article links
for id in arxiv_ids:
    ##### Metadata to get out of articles #####
    title = " "
    authors = []
    comments = " "
    subjects = " "
    abstract = " "
    ###########################################

    article = {}

    link = "https://arxiv.org/abs/" + str(id)

    # Send HTTP request to the URL
    response = requests.get(link)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # FINDS TITLE
    title_tag = soup.find('h1', class_='title mathjax')
    # Cleans the tag to only get the title
    title = title_tag.get_text(strip=True).replace("Title:", "", 1)

    # FINDS AUTHOR
    authors_div = soup.find('div', class_='authors')
    if authors_div:
        # Find all 'a' tags within the div with class 'authors'
        author_tags = authors_div.find_all('a')
        # Extract the text from each 'a' tag
        authors = [tag.text for tag in author_tags]

    # FINDS COMMENTS
    comment_tag = soup.find('td', class_='tablecell comments mathjax')
    if comment_tag is not None:
        # Extract the text from each 'td' tag
        comments = comment_tag.text

    # FINDS SUBJECTS
    subject_span = soup.find('span', class_='primary-subject')
    subjects = subject_span.text

    # FINDS ABSTRACT
    abstract_blockquote = soup.find('blockquote', class_='abstract mathjax')
    abstract = abstract_blockquote.text.replace("\nAbstract:", "")

    # ADD TO DICTIONARY
    if title is not None and len(authors) > 0: ## if there is a title and author
        ### Could also add if comments say paper has been published here ###
        article['title'] = title
        article['authors'] = authors
        article['comments'] = comments
        article['subjects'] = subjects
        article['abstract'] = abstract

    metadatas[id] = article

    # Sleep for the random interval between 0 and 0.1
    time.sleep(random.random() / 10)

# Writing metadata to metadata_raw.json
with open('raw_metadata.json', 'w') as json_file:
    json.dump(metadatas, json_file, indent=4)
    

        
            







