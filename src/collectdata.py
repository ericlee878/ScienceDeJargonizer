## main file for collecting data ##

import datetime
import pandas as pd
##import arxivscraper
import arxiv
import time 
import requests
from bs4 import BeautifulSoup

## array that holds all the abstracts of the articles
abstracts = []



## link to arxiv/cs
arXiv_url = "https://arxiv.org/list/cs.AI/recent"

# Send HTTP request to the URL
response = requests.get(arXiv_url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all <dl> elements
dl = soup.find_all('dl')

# Find all <dt> elements in the <dl> element
dt_list = dl[0].find_all('dt') 
# dt = dt_list[0]
for dt in dt_list:
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
        print(html_href)
        # Parse the HTML content
        html_soup = BeautifulSoup(html_response.text, 'html.parser')

        # Finds all <div> elements with the class '
        p_list = html_soup.find_all('p', class_='ltx_p')
        for p in p_list:
            print(p.get_text())
            abstracts.append(p.get_text())
            print("----------------------------------")
    
print(abstracts[0])

        # # Find the <p> tag by its class (if needed)
        # p_tags = html_soup.findAll('p', class_='ltx_p')
        # print(len(p_tags))
        # for p_tag in p_tags:
        #     text = p_tag.string
        #     print(text)

        ##abstract = p_tags.get_text()
        ##abstracts.append(abstract)

        # Finds all <div> elements with the class '
        ##div_elements = soup.find_all('div', class_='ltx_page_content')
        ##print(len(div_elements))

## how articles have paragraphs organized:
## - ltx_p
## - ltx_p
        
            







