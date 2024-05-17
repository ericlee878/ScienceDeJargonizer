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
arxiv_ids_to_mine = get_arxiv_ids(start, end)

# dictionary that stores the arXiv metadata
metadatas = {}

# List of ids that raised exceptions
arxiv_ids_exceptions = []

# headers for requests
headers = {
    "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
}
# iterates through all article links
for arxiv_id in arxiv_ids_to_mine:

    ##### Metadata to extract from articles #####
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

    # Create article object
    article = {}

    # Create the link
    link = f"https://arxiv.org/abs/{arxiv_id}"

    # Request the URL
    try:
        # Send HTTP request to the URL
        response = requests.get(link, headers=headers)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        if soup:
            # FINDS TITLE
            title_tag = soup.find('h1', class_='title mathjax')
            # Cleans the tag to only get the title

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

        else:  
            print("'soup' object is NoneType'.")
            arxiv_ids_exceptions.append(arxiv_id)
    
    # except requests.exceptions.Timeout:
    #     # Handle timeout error, log the error
    #     print(f"Timeout error occurred for ArXiv ID: {arxiv_id}")
    #     continue  # Continue with the next iteration of the loop
    # except requests.exceptions.TooManyRedirects:
    #     # Handle too many redirects error
    #     print(f"Too many redirects for ArXiv ID: {arxiv_id}")
    #     continue
    # except requests.exceptions.RequestException as e:
    #     # Handle other request exceptions
    #     print(f"Request exception occurred for ArXiv ID: {arxiv_id}")
    #     print(e)
    #     continue
    except Exception as e:
        # Handle any other unexpected exceptions
        print(f"Unexpected error occurred for ArXiv ID: {arxiv_id}")
        print(e)
        continue
        
    

    # Sleep for the random interval between 0 and 0.1
    time.sleep(random.random() / 10)

############################################################
######################## WRITE DATA ########################
############################################################

# Writing metadata out
arxiv_filepath = home_dir / 'data' / 'arxiv_metadata' / 'all' / (template_filename+'_all_arxiv_metadata.json')
with open(arxiv_filepath, 'w') as json_file:
    json.dump(metadatas, json_file, indent=4)


