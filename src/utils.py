import pandas as pd
import arxivscraper
import re 
import urllib, urllib.request
import requests
import xml.etree.ElementTree as ET
import arxiv

def get_arxiv_ids(start, end, primary_cats=[]):

    '''
    Parameters:
    ----------------
    start: String, the start date for papers desired
    end: String, the end date for papers desired
    primary_cats: List, optional, primary categories for desired papers. E.g., ['cs.ai', 'cs.cl', 'cs.cv', 'cs.cy',]

    Uses arxivscraper to obtain IDs in the date range.

    Returns:
    ----------------
    arxiv_ids_to_mine: arXiv IDs of CS papers that were either published or updated in the specified
    time range, and belong to a desired list of primary categories. 
    '''

    # Create scraper object to get all article IDs in desired time range - 
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

    # Cannot use this output as is because it does not collect comments + makes a bunch of lower-casing and formatting decisions that I would avoid. 
    # Just that it preconfigures the search and the date stuff very well.

    # Filter the outputs to get articles only in desired sub-categories
    arxiv_ids_to_mine = []
    for article in scraper_output:
        if not primary_cats or article['categories'].split(' ')[0] in primary_cats:
            arxiv_ids_to_mine.append(article['id'])

    # print("Initial bulk of CS articles in date range filtered by categories!")
    print("Articles to mine using arXiv API, post filtering on CS category and dates: "+str(len(arxiv_ids_to_mine))+"\n\n")

    return arxiv_ids_to_mine

# def get_arxiv_metadata(arxiv_ids_to_mine):

#     '''
#     Parameters:
#     ----------------
#     arxiv_ids_to_mine: List, arXiv ids that need to be mined

#     Uses arXiv API to access metadata of arXiv articles.

#     Returns:
#     ----------------
#     arxiv_metadatas: Dict, contains sub-dicts that list off articles and their metadata.
#     '''


def get_arxiv_metadata(arxiv_ids_to_mine):

    '''
    Parameters:
    ----------------
    arxiv_ids_to_mine: List, arXiv ids that need to be mined

    Uses arXiv API to access metadata of arXiv articles.

    Returns:
    ----------------
    arxiv_metadatas: Dict, contains sub-dicts that list off articles and their metadata.
    '''

    # Split arxiv_ids into more managable chunks (size=10, removes need for pagination), and turn into strings
    arxiv_id_chunks = []
    curr_list = []
    for i in range(len(arxiv_ids_to_mine)):
        if i % 10 == 0 and i != 0:
            # turn arxiv_id into string 
            comma_delimited_list = ",".join(curr_list)
            arxiv_id_chunks.append(comma_delimited_list)
            curr_list = []
            curr_list.append(arxiv_ids_to_mine[i])
        else:
            curr_list.append(arxiv_ids_to_mine[i])

    # turn last arxiv_id list into string and add
    comma_delimited_list = ",".join(curr_list)
    arxiv_id_chunks.append(comma_delimited_list)

    # Dictionary to store metadata
    arxiv_metadatas = {}

    # Iterate over the chunks
    for id_list in arxiv_id_chunks:

        url = 'http://export.arxiv.org/api/query?start=0&sortBy=lastUpdatedDate'
        url = url + "&id_list=" + id_list

        data = urllib.request.urlopen(url)
        ## print(data.read().decode('utf-8'))
        response = requests.get(url)
        # root = ET.fromstring(data)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content of the response
            data = response.content  # This gets the bytes content
            # or, if the content is text and not bytes:
            # data = response.text

            # Parse the XML data
            root = ET.fromstring(data)

        else:
            print(response.content)

        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            
            article_dict = {}
            article_id = entry.find('{http://www.w3.org/2005/Atom}id').text.split('/abs/')[-1]
            article_dict['url'] = entry.find('{http://www.w3.org/2005/Atom}id').text
            article_dict['title'] = entry.find('{http://www.w3.org/2005/Atom}title').text
            article_dict['summary'] = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
            article_dict['updated'] = entry.find('{http://www.w3.org/2005/Atom}updated').text
            article_dict['published'] = entry.find('{http://www.w3.org/2005/Atom}published').text

            # Authors
            authors = []
            for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
                authors.append(author.find('{http://www.w3.org/2005/Atom}name').text)
            article_dict['authors'] = authors

            # Comments
            comment = entry.find('{http://arxiv.org/schemas/atom}comment')
            if comment is not None:
                article_dict['comments'] = comment.text

            # Categories
            categories = []
            for category in entry.findall('{http://www.w3.org/2005/Atom}category'):
                categories.append(category.attrib['term'])
            article_dict['categories'] = categories

            # Primary category
            primary_category = entry.find('{http://arxiv.org/schemas/atom}primary_category')
            if primary_category is not None:
                article_dict['primary_category'] = primary_category.attrib['term']

            # DOI and Journal references
            doi = entry.find('{http://arxiv.org/schemas/atom}doi')
            if doi is not None:
                article_dict['doi'] = doi.text

            journal_ref = entry.find('{http://arxiv.org/schemas/atom}journal_ref')
            if journal_ref is not None:
                article_dict['journal_ref'] = journal_ref.text

            arxiv_metadatas[article_id] = article_dict

    return arxiv_metadatas


def is_peer_reviewed(comments):

    '''
    Parameters:
    ----------------
    comments: String, contains any author comments posted along with the arXiv metadata

    Returns:
    ----------------
    peer_reviewed: Boolean, True or False, depending on the comment
    '''

    # Define a regular expression pattern to match strings meeting the criteria for peer review indicators
    pattern = r'(accept.*|publish.*|present.*|2023|2024|2025)'
    
    # Use re.search to find if the pattern matches anywhere in the text
    match = re.search(pattern, comments, re.IGNORECASE)
    
    # If a match is found, return True, otherwise return False
    return bool(match)


def download_pdf(arxiv_id, output_folder):

    '''
    Parameters:
    ----------------
    arxiv_id: String, arXiv ID of the article
    output_folder: Path, the folder where the PDFs will be saved

    Downloads the PDFs of the arXiv articles.

    Returns:
    ----------------
    None
    '''

    # Use the arXiv wrapper to get the paper
    paper = next(arxiv.Client().results(arxiv.Search(id_list=[arxiv_id])))

    # Download the PDF to a specified directory with a custom filename
    try:
        paper.download_pdf(
            dirpath=output_folder, 
            filename=f"{arxiv_id}.pdf"
        )
    
    except Exception as e:
        print(f"Error downloading PDF for arXiv ID: {arxiv_id}. Error: {e}")


    # Old code -- used requests, switching to arXiv wrapper
    # # Construct the URL for the PDF + where it will be saved
    # pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    # pdf_filepath = output_folder / f"{arxiv_id}.pdf"
    # try:
    #     # Open the URL
    #     with urllib.request.urlopen(pdf_url) as response:
    #         # Open a file to write the PDF contents
    #         with open(pdf_filepath, 'wb') as f:
    #             # Read the response content and write it to the file
    #             f.write(response.read())
    #         # Print a success message if the PDF is downloaded successfully
    #         print(f"PDF downloaded for arXiv ID: {arxiv_id}")
    # except Exception as e:
    #     # Print an error message if there is any exception during the download process
    #     print(f"Error downloading PDF for arXiv ID: {arxiv_id}. Error: {e}")
