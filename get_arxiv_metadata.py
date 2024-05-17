### arXiv Metadata Collection ###

# Imports
import time 
import random
import requests
import json
from src.utils import get_arxiv_ids, get_arxiv_metadata
from pathlib import Path
import argparse
import re
import logging
from datetime import datetime

# Get basic directory
home_dir = Path.cwd()

############################################################
###################### SETUP LOGGING #######################
############################################################

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = home_dir / "logs" / f"get_arxiv_metadata_logfile_{timestamp}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

############################################################
###################### ACCEPT INPUTS #######################
############################################################

# Define a custom argument type for a list of strings -- useful for primary category argument
def list_of_strings(argument):
    return argument.split(',')

# Create parser 
parser = argparse.ArgumentParser(
    description="Mine article metadata from arXiv CS.")

parser.add_argument(
    "start",
    type=str, 
    help="Start Date for arXiv publications: YYYY-MM-DD format.")
parser.add_argument(
    "end", 
    type=str, 
    help="End Date for arXiv publications: YYYY-MM-DD format.")
parser.add_argument(
    "--primary-cats", 
    type=list_of_strings, 
    help="Comma-separated list of primary categories (e.g., 'cs.hc,cs.ai,cs.cy'). Defaults to an empty list if not provided, i.e., any primary categories. There is no error-checking on what is a valid category, so please check yourself before your wreck yourself.", 
    default=[]
)
args = parser.parse_args()

# Extract args
start = args.start
end = args.end
primary_cats = args.primary_cats

# Double check the date
assert start<end, "Re-enter dates such that start date is before the end date."

# Generate a filename for all metadata files from start and end date
filename_date = "".join(start[2:].split('-')) + '_' + "".join(end[2:].split('-'))
filename_cats = "filtered_cats" if primary_cats else "all_cats"

print(filename_cats)

# Log the chosen categories and the generated filename
logging.info(f"Logfile created: {log_filename}")
logging.info(f"Collecting arXiv metadata in time range: {start} to {end}")
logging.info(f"Collecting arXiv metadata with primary categories: {primary_cats}")

############################################################
######################## GET DATA ##########################
############################################################

# Gets the arXiv IDs based on date, time, primary categories
arxiv_ids_to_mine = get_arxiv_ids(start, end, primary_cats=primary_cats)
arxiv_metadatas = get_arxiv_metadata(arxiv_ids_to_mine[:5])

# ############################################################
# ######################## WRITE DATA ########################
# ############################################################

# Writing metadata out
arxiv_filepath = home_dir / 'data' / 'arxiv_metadata' / (template_filename+filename_cats+'_arxiv_metadata.json')

print(f"Saving dataset at: {arxiv_filepath}")

with open(arxiv_filepath, 'w') as json_file:
    json.dump(arxiv_metadatas, json_file, indent=4)

# Log the filename of the saved dataset
logging.info(f"Saved dataset!")

