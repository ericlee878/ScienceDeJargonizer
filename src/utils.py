import datetime
import pandas as pd
import arxivscraper
import arxiv
import time 

def get_arxiv_ids(start, end):

    '''
    Get the arXiv IDs of CS papers that were either published or updated in the specified
    time range, and belong to our desired list of categories. Uses external, unofficial 
    arxivscraper to obtain IDs in the date range.

    Returns list of arXiv IDs. 
    '''

    # Desired fields
    desired_fields = [
        'cs.ai', 'cs.cl', 'cs.cv', 'cs.cy', 'cs.hc', 
        'cs.ir', 'cs.lg', 'cs.ni', 'cs.ro', 'cs.si', 
    ]

    # Create scraper to get all article IDs in our desired time range - 
    # Collected articles include submissions and resubmissions
    scraper = arxivscraper.Scraper(
        category='cs', 
        date_from=start,
        date_until=end,
        t=20 # batching for efficiency
    )

    # Call scraper
    scraper_output = scraper.scrape()

    print("Initial bulk of arXiv CS articles in date range discovered - includes publications and updates.\n\n")

    # Filter the outputs to get articles only in desired sub-categories
    arxiv_ids_to_mine = []

    # Iterate and run category check
    for time_range_article in scraper_output:
        
        # List of all categories should be a subset of the desired fields list 
        cat_list = time_range_article['categories'].split(' ')
        
        # All author-assigned categories should be present in our list of desied categories
        if set(cat_list).issubset(set(desired_fields)):
            arxiv_ids_to_mine.append(time_range_article['id'])

    print("Initial bulk of CS articles in date range filtered by categories!")
    print("Articles to mine using arXiv API, post filtering: "+str(len(arxiv_ids_to_mine))+"\n\n")

    return arxiv_ids_to_mine


def is_peer_reviwed(comment):

    '''
    Parameters:
    ----------------
    comment: String, contains any author comments posted along with the arXiv metadata

    Returns:
    ----------------
    peer_reviewed: Boolean, True or False, depending on the comment
    '''

    # Define a regular expression pattern to match strings meeting the criteria for peer review indicators
    pattern = r'(accept.*|publish.*|present.*|2023|2024|2025)'
    
    # Use re.search to find if the pattern matches anywhere in the text
    match = re.search(pattern, comment, re.IGNORECASE)
    
    # If a match is found, return True, otherwise return False
    return bool(match)


