### ArXiv Fulltext Collection ###

# Imports
import json
from pathlib import Path
import argparse
from src.utils import is_peer_reviewed, is_in_HC_CY, download_pdf
import pandas as pd
import re
import arxiv
import urllib.request
import concurrent.futures
import time
import random

# Get basic directory
home_dir = Path.cwd()

# Setup the right dates for input
arxiv_daterange = "240301_240305"
arxiv_metadata_filepath = home_dir / 'data' / 'arxiv_metadata' / 'all' / (arxiv_daterange + '_all_arxiv_metadata.json')

# Mkdir for pdf output
output_folder = home_dir / 'data' / 'arxiv_metadata' / 'arxiv_pdfs' / arxiv_daterange 
output_folder.mkdir(parents=True, exist_ok=True) 

############################################################
###################### ACCEPT INPUTS #######################
############################################################

# Read in arXiv metadata
with open(arxiv_metadata_filepath) as json_data:
    metadata = json.load(json_data)
    json_data.close()

# Convert JSON to DataFrame
metadata_df = pd.DataFrame.from_dict(metadata, orient='index')
metadata_df.index.name = 'arxiv_id'
metadata_df = metadata_df.reset_index()
print(f"Papers in dataset filtered by date range (of publication/update): {metadata_df.shape[0]}")

# Filter by peer-review for the scrape of fulltext
metadata_df['peer_reviewed'] = metadata_df['comments'].apply(is_peer_reviewed)
metadata_df = metadata_df.loc[metadata_df['peer_reviewed']].reset_index(drop=True)
print(f"Papers in dataset filtered by date range + have been peer-reviewed: {metadata_df.shape[0]}")

# Filter by sub-categories: cs.CY or cs.HC
metadata_df["in_HC_CY"] = metadata_df["primary_category"].apply(is_in_HC_CY)
metadata_df = metadata_df.loc[metadata_df["in_HC_CY"]].reset_index(drop=True)
print(f"Papers in dataset filtered by date range + have been peer-reviewed + in desired primary categories: {metadata_df.shape[0]}")

# Use ThreadPoolExecutor to create a pool of threads for parallel execution
with concurrent.futures.ThreadPoolExecutor() as executor:

    # A list to store futures representing the status of each download task
    futures = []
    # Iterate over the arxiv_id values in your DataFrame
    for arxiv_id in metadata_df['arxiv_id']:
        # Submit each download task to the executor and store the future object
        futures.append(executor.submit(download_pdf, arxiv_id, output_folder))

        # Sleep for the random interval between 0 and 0.2s
        time.sleep(random.random() / 5)

    # Wait for all tasks to complete and gather the results
    for future in concurrent.futures.as_completed(futures):
        try:
            # Retrieve the result of the download task, which may raise an exception
            future.result()
        except Exception as e:
            # Print information about any exceptions that occurred during the download process
            print(f"Exception occurred: {e}")
        
        

# Implement logging for this

# Save this df in an output folder as well
metadata_df.set_index("arxiv_id", inplace=True)
metadata_df.to_json(
    home_dir / 'data' / 'arxiv_metadata' / 'filtered' / (arxiv_daterange + '_arxiv_metadata_for_pdfs.json'), 
    orient="index", 
    indent=4
)