import datetime
import pandas as pd
import arxivscraper
import arxiv
import pdfx
from pyaltmetric import Altmetric
import time 


def mine_arxiv_metadata(arxiv_ids_to_mine, start=0, end=0):

    '''
    Uses the arXiv API to get the full paper metadata (excluding fulltext). 
    Returns DataFrame.

    Input:
    arxiv_ids_to_mine: List, all arXiv IDs to get metadata for
    '''

    # Mine from arXiv API in Chunks (to get max metadata possible)

    # How many elements each chunk should have  
    n = 300
    
    # Using list comprehension to create ID batches
    arxiv_ids_to_mine = [arxiv_ids_to_mine[i:i + n] for i in range(0, len(arxiv_ids_to_mine), n)]
    print("Number of calls to be made to arXiv API: " + str(len(arxiv_ids_to_mine)) + "\n\n")

    # Maintain list of non-null article objects
    list_article_dicts = []

    # Iterate and mine using official API
    for desired_id_list in arxiv_ids_to_mine:
        
        # Generate arXiv query
        query = arxiv.Search(id_list=desired_id_list)
        
        # Iterate over results and check each for None, then save
        for article_object in query.results():
        
            # Check if the dict exists i.e. article was retrieved successfully
            if article_object:

                # Clean
                article_dict = clean_article_object(article_object)
                list_article_dicts.append(article_dict)

    # Convert to DF
    arxiv_metadata = pd.DataFrame(list_article_dicts)

    # Time stamp format conversions
    start_date = pd.Timestamp(start, tz='US/Pacific')
    end_date = pd.Timestamp(end, tz='US/Pacific')
    print(arxiv_metadata.dtypes)

    # Get df with desired articles only - using the 'published' column from the official API
    arxiv_metadata = arxiv_metadata[arxiv_metadata['published'].between(start_date, end_date)]

    print("Date Filtered Number of arXiv articles: "+ str(arxiv_metadata.shape[0]))

    return arxiv_metadata


def mine_arxiv_fulltext(arxiv_ids_to_mine):

    '''
    Takes as input a list of arXiv IDs, and uses them to obtain the fulltext. 
    '''

    # Mine fulltext
    arxiv_fulltexts = {}

    # Iterate and mine
    for arxiv_id in arxiv_ids_to_mine:

        # Generate link
        pdf_link = "https://arxiv.org/pdf/" + arxiv_id[:-2] + ".pdf"

        try:
            # Use pdfx to get the object
            pdf = pdfx.PDFx(pdf_link)

            # Extract text from the object
            pdf_text = pdf.get_text()

            # Add to dictionary
            arxiv_fulltexts[arxiv_id] = pdf_text

        except Exception as e: 
            print(e)
            print(f"No PDF found for {arxiv_id}")

    return arxiv_fulltexts



def mine_altmetric_metadata(arxiv_ids_to_mine, api_key=None):

    '''
    Use a list of arXiv IDs to get their Altmetric statistics for 
    mainstream news coverage.
    '''

    print(f"Collecting Altmetric Data for {len(arxiv_ids_to_mine)} arXiv articles.")

    # Instantiate API
    api = Altmetric()
    if api_key:
        api = Altmetric(api_key)

    # Empty list
    altmetric_metadata = []

    # Unretrieved IDs
    altmetric_not_found = []

    # Iterate and retrieve Altmetric data
    for arxiv_id in arxiv_ids_to_mine:
        
        time.sleep(2)
            
        # Retrieve entry
        arxiv_entry = api.arxiv(arxiv_id[:-2])
        
        if arxiv_entry: # if not None, this exists
            altmetric_metadata.append(arxiv_entry)
        else:
            altmetric_not_found.append(arxiv_id)


    print("Abstracts found on Altmetric: ", len(altmetric_metadata))
    print("Abstracts not found on Altmetric: ", len(altmetric_not_found))

    # Convert to DataFrame
    altmetric_metadata = pd.DataFrame(altmetric_metadata)

    return altmetric_metadata

def text_proc(text_field):
    
    '''Removes surrounding whitespaces from text + Removes newlines.'''
    
    if text_field:
    
        # Remove surrounding whitespaces
        text_field = text_field.strip()

        # Replace new line with space and then remove doublespaces
        text_field = ' '.join(text_field.replace("\n", " ").split())
    
    return text_field

# def time_proc(time_field):
    
#     ''' 
#     Process the time format from ISO into a Python datetime object.
#     '''
    
#     if time_field:
#         time_field = datetime.datetime.strptime(time_field, '%Y-%m-%dT%H:%M:%SZ').date()
        
#     return time_field

def clean_article_object(article_object):
    
    '''
    Used to clean the mined arXiv data. 
    Retains only required keys + Does necessary text/timestamp processing/key title modification 
    wherever needed.
    
    '''
    
    # Create a filtered version of only the relevant keys
    article_dict = {}
    
    # Add keys
    article_dict['arxiv_id'] = article_object.entry_id.split('/')[-1]
    article_dict['arxiv_url'] = article_object.entry_id
    # article_dict['arxiv_pdf_url'] = article_object.entry_id.replace('arxiv.org/abs', 'arxiv.org/pdf')+'.pdf'
    
    article_dict['arxiv_primary_category'] = article_object.primary_category.lower()
    article_dict['arxiv_all_categories'] = [cat.lower() for cat in article_object.categories if cat[:3]=='cs.'] # arXiv occassionally returns the ACM format too, ignore it
    
    article_dict['title'] = text_proc(article_object.title)
    article_dict['summary'] = text_proc(article_object.summary)
    article_dict['doi'] = article_object.doi
    article_dict['authors'] = [auth_object.name for auth_object in article_object.authors]
    
    article_dict['published'] = article_object.published
    article_dict['updated'] = article_object.updated
    
    return article_dict


def check_time_period(time_field, start_datetime, end_datetime):

    '''
    Checks if the publication data (not "update" date) is within our desired time range.
    '''
    
    return start_datetime <= time_field <= end_datetime