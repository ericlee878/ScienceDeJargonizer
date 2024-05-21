### ArXiv Fulltext Collection ###

# Imports
import json
from pathlib import Path
import argparse
from src.utils import is_peer_reviewed, download_pdf
import pandas as pd
import re
import arxiv
import urllib.request
import concurrent.futures
import time
import random
import logging
from datetime import datetime

# Get basic directory
home_dir = Path.cwd()

############################################################
###################### SETUP LOGGING #######################
############################################################

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = home_dir / "logs" / f"get_arxiv_texts_logfile_{timestamp}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

############################################################
###################### ACCEPT INPUTS #######################
############################################################

# Ask for the filepath to the arXiv metadata for which to download fulltexts

# Create parser 
parser = argparse.ArgumentParser(
    description="Mine fulltexts from arXiv CS.")
parser.add_argument(
    "arxiv_metadata_filepath",
    type=str, 
    help="Absolute filepath to the arXiv metadata JSON file.")
args = parser.parse_args()

# Extract args
arxiv_metadata_filepath = Path(args.arxiv_metadata_filepath)

# Check that the file exists
assert arxiv_metadata_filepath.exists(), "File does not exist. Please enter a valid filepath."

# Create a folder for the output PDFs
output_folder = home_dir / 'data' / 'arxiv_pdfs' / arxiv_metadata_filepath.stem
output_folder.mkdir(parents=True, exist_ok=True)

# Log the logfile and the arXiv metadata filepath
logging.info(f"Logfile created: {log_filename}")
logging.info(f"ArXiv metadata filepath: {arxiv_metadata_filepath}")

############################################################
######################## GET DATA ##########################
############################################################

# Read in arXiv metadata
with open(arxiv_metadata_filepath) as json_data:
    metadata = json.load(json_data)
    json_data.close()

# Convert JSON to DataFrame
metadata_df = pd.DataFrame.from_dict(metadata, orient='index')
logging.info(f"Count of papers in dataset: {metadata_df.shape[0]}")

print(metadata_df.head())

# Use ThreadPoolExecutor to create a pool of threads for parallel execution
with concurrent.futures.ThreadPoolExecutor() as executor:

    # A list to store futures representing the status of each download task
    futures = []
    # Iterate over the arxiv_id values in your DataFrame
    for arxiv_id in metadata_df['arxiv_id']:
        # Submit each download task to the executor and store the future object
        futures.append(executor.submit(download_pdf, arxiv_id, output_folder))

        # Sleep for the random interval between 0 and 1s
        time.sleep(random.random())

    # Wait for all tasks to complete and gather the results
    for future in concurrent.futures.as_completed(futures):
        try:
            # Retrieve the result of the download task, which may raise an exception
            future.result()
        except Exception as e:
            # Print information about any exceptions that occurred during the download process
            print(f"Exception occurred: {e}")
        
# Log the completion of the download process
logging.info(f"Download process completed for {metadata_df.shape[0]} papers.")
# Log the directory where they are saved
logging.info(f"PDFs saved to: {output_folder}")