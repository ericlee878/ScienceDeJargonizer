## main file for collecting data ##

import datetime
import pandas as pd
##import arxivscraper
import arxiv
import time 
import requests
from bs4 import BeautifulSoup
import json

## link to arxiv/cs
arXiv_url = "https://arxiv.org/list/cs.AI/recent"

# Send HTTP request to the URL
response = requests.get(arXiv_url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Finds all the divs with the metadata
meta_divs = soup.find_all('div', class_='meta')

# Dict that holds all the metadata of all the papers
metadata_list = {}

# Id of papers in database
id = 0

for meta in meta_divs:
    # print(meta)
    # print("--------")
    # Parse the HTML content
    if meta is not None:
        metasoup = BeautifulSoup(meta, 'html.parser')
        # Extgit acting the title
        title = metasoup.find('div', class_='list-title').get_text(strip=True).replace('Title:', '').strip()
        # Extracting the authors
        authors = [a.get_text(strip=True) for a in metasoup.find('div', class_='list-authors').find_all('a')]
        # Extracting the comments
        comments = metasoup.find('div', class_='list-comments').get_text(strip=True).replace('Comments:', '').strip()
        # Extracting the subjects
        subjects = metasoup.find('div', class_='list-subjects').get_text(strip=True).replace('Subjects:', '').strip()

        data = {
            "title": title,
            "authors": authors,
            "comments": comments,
            "subjects": subjects
        }
        metadata_list[id] = data
        id = id + 1

## array that holds all the abstracts of the articles
id_to_texts_map = {}

# Find all <dl> elements
dl = soup.find_all('dl')

# Find all <dt> elements in the <dl> element
dt_list = dl[0].find_all('dt') 

## id of each paper
id = 0
## iterates through each paper
for dt in dt_list:
    first_run = True
    # Find all <a> tags within this <dt> that have an 'href' attribute
    a_tags = dt.find_all('a', href=True)
    # Finds the <a> tag with link to paper
    a_tag = a_tags[0]
    # Find the link to paper from a_tag
    href = a_tag['href']
    ## makes each href into proper link to paper
    paper_url = "https://arxiv.org" + href
    # Send HTTP request to the URL
    paper_response = requests.get(paper_url)
    # Parse the HTML content
    paper_soup = BeautifulSoup(paper_response.text, 'html.parser')
    # Find the <a> element with string 'HTML (experimental)'
    paper_a_tag = paper_soup.find('a', string='HTML (experimental)')
    # Find the link to html_format from paper_a_tag
    if paper_a_tag != None:
        html_href = paper_a_tag['href']
        # Send HTTP request to the URL
        html_response = requests.get(html_href)
        ##print(html_href)
        # Parse the HTML content
        html_soup = BeautifulSoup(html_response.text, 'html.parser')

        # Finds all <div> elements with the class '
        p_list = html_soup.find_all('p', class_='ltx_p')
        for p in p_list:
            if first_run: # If new article
                id_to_texts_map[id] = p.get_text() # Adds a new column in dictionary
            else:
                id_to_texts_map[id] = id_to_texts_map[id] + p.get_text() ## If not new article, keeps adding to same element of dict
            first_run = False
        id = id + 1
    else:
        ## deletes papers without html format from earlier metadata list (to match id numbering)
        del metadata_list[id]
        id = id + 1


# Writing metadata to metadata_raw.json
with open('metadata_raw.json', 'w') as json_file:
    json.dump(metadata_list, json_file, indent=4)


# Writing text data to id_to_text_raw.json
with open("id_to_text_raw.json", "w") as outfile:
    json.dump(id_to_texts_map, outfile, indent=4)

        
            







