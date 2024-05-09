### ArXiv Metadata Collection ###

# Imports
import time 
import random
import requests
from bs4 import BeautifulSoup
import json
from src.utils import get_arxiv_ids
from pathlib import Path
import argparse
import re

# Get basic directory
home_dir = Path.cwd()

############################################################
###################### ACCEPT INPUTS #######################
############################################################

# Create parser for time range
parser = argparse.ArgumentParser(
    description="Mine article metadata from arXiv CS.")
parser.add_argument("start", type=str, help="Start Date for arXiv publications: YYYY-MM-DD format.")
parser.add_argument("end", type=str, help="End Date for arXiv publications: YYYY-MM-DD format.")
args = parser.parse_args()

# Desired time range
start = args.start
end = args.end

# Double check the date
assert start<end, "Re-enter dates such that start date is before the end date."

# Generate a filename for all metadata files from start and end date
template_filename = "".join(start[2:].split('-')) + '_' + "".join(end[2:].split('-'))

############################################################
######################## GET DATA ##########################
############################################################

# gets the ids of the articles in specific dateframe
arxiv_ids = get_arxiv_ids(start, end)

# dictionary that stores the arXiv metadata
metadatas = {}

# iterates through all article links
for id in arxiv_ids:
    ##### Metadata to get out of articles #####
    title = " "
    authors = []
    comments = " "
    subjects = " "
    abstract = " "
    primary_category = " "
    categories = []
    submitted_date = " "
    last_revised_date = " "
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

    # FINDS DATE
    date_div = soup.find('div', class_="dateline")
    date_div_text = date_div.text
    # Extracts the submitted date
    submitted_match = re.search(r"Submitted on (\d+ \w+ \d+)", date_div_text)
    if submitted_match:
        submitted_date = submitted_match.group(1)
    # Extracts the last revised date
    last_revised_match = re.search(r"last revised (\d+ \w+ \d+)", date_div_text)
    if last_revised_match:
        revised_date = last_revised_match.group(1)
    else:
        revised_date = submitted_date

    # FINDS PRIMARY CATEGORY
    primary_category_span = soup.find('span', class_='primary-subject')
    primary_category_text = primary_category_span.text
    # Extracts the short-hand version of primary category
    primary_category = re.findall(r'\(([^()]*)\)', primary_category_text)[-1]

    # FINDS CATEGORIES
    categories_td = soup.find('td', class_ = 'tablecell subjects')
    # Takes out the span element that contains primary category
    span_element = categories_td.find('span')
    if span_element:
        span_element.extract() 
    categories_text = categories_td.text
    # Seperates the categories into a list
    categories_list = [item.strip() for item in categories_text.split(';') if item.strip()]

    # Extracts the short-hand version of categories from each category and appends it to list
    for c in categories_list:
        c_text = re.findall(r'\(([^()]*)\)', c)[-1]
        categories.append(c_text)

    # ADD TO DICTIONARY
    if title is not None and len(authors) > 0: ## if there is a title and author
        ## Could also add if comments say paper has been published here ###
        article['title'] = title
        article['authors'] = authors
        article['comments'] = comments
        article['subjects'] = subjects
        article['abstract'] = abstract
        article['primary_category'] = primary_category
        article['categories'] = categories
        article['submitted_date'] = submitted_date
        article['last_revised_date'] = last_revised_date

    metadatas[id] = article

    # Sleep for the random interval between 0 and 0.1
    time.sleep(random.random() / 10)

############################################################
######################## WRITE DATA ########################
############################################################

# Writing metadata out
arxiv_filepath = home_dir / 'data' / 'arxiv_metadata' / 'all' / (template_filename+'_all_arxiv_metadata.json')
with open(arxiv_filepath, 'w') as json_file:
    json.dump(metadatas, json_file, indent=4)


