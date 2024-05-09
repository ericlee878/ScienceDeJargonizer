import datetime
import pandas as pd
import arxivscraper
import arxiv
import time 
import re 
import urllib.request

def get_arxiv_ids(start, end):

    '''
    Get the arXiv IDs of CS papers that were either published or updated in the specified
    time range, and belong to our desired list of categories. Uses external, unofficial 
    arxivscraper to obtain IDs in the date range.

    Returns list of arXiv IDs. 
    '''

    # # Desired fields
    # desired_fields = [
    #     'cs.ai', 'cs.cl', 'cs.cv', 'cs.cy', 'cs.hc', 
    #     'cs.ir', 'cs.lg', 'cs.ni', 'cs.ro', 'cs.si', 
    # ]

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

    # Cannot use this as is because it does not collect comments + makes a bunch of lower-casing and formatting decisions

    # Filter the outputs to get articles only in desired sub-categories
    arxiv_ids_to_mine = []

    # Iterate over outputs and append the ids to a list -- initially we were filtering out categories here but now we've decided to do it later.
    for time_range_article in scraper_output:

        # Just append
        arxiv_ids_to_mine.append(time_range_article['id'])
        
        # # List of all categories should be a subset of the desired fields list 
        # cat_list = time_range_article['categories'].split(' ')
        
        # # All author-assigned categories should be present in our list of desied categories
        # if set(cat_list).issubset(set(desired_fields)):
        #     arxiv_ids_to_mine.append(time_range_article['id'])

    # print("Initial bulk of CS articles in date range filtered by categories!")
    print("Articles to mine using arXiv API, post filtering on CS category and dates: "+str(len(arxiv_ids_to_mine))+"\n\n")

    return arxiv_ids_to_mine

def is_peer_reviewed(comment):

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

def is_in_HC_CY(primary_category):
    '''
    Parameters:
    ----------------
    primary_category: String, names the primary category of the work

    Returns:
    ----------------
    in_HC_CY: Boolean, True or False, depending on the primary_category
    '''

    return primary_category in ["cs.CY", "cs.HC"]


def download_pdf(arxiv_id, output_folder):
    # Construct the URL for the PDF + where it will be saved
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    pdf_filepath = output_folder / f"{arxiv_id}.pdf"
    try:
        # Open the URL
        with urllib.request.urlopen(pdf_url) as response:
            # Open a file to write the PDF contents
            with open(pdf_filepath, 'wb') as f:
                # Read the response content and write it to the file
                f.write(response.read())
            # Print a success message if the PDF is downloaded successfully
            print(f"PDF downloaded for arXiv ID: {arxiv_id}")
    except Exception as e:
        # Print an error message if there is any exception during the download process
        print(f"Error downloading PDF for arXiv ID: {arxiv_id}. Error: {e}")
