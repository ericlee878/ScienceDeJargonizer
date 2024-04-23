### ArXiv Fulltext Collection ###

# Imports
import json
from pathlib import Path
import argparse
from utils import is_peer_reviewed

# Get basic directory
home_dir = Path.cwd()

############################################################
###################### ACCEPT INPUTS #######################
############################################################

# Read in the IDs w/ the metadata -- change filename to the relevant one
with open('../data/raw/240302_240303_arxiv_metadata.json') as json_data:
    metadata = json.load(json_data)
    json_data.close()

# Convert JSON to DataFrame
metadata_df = pd.DataFrame.from_dict(metadata, orient='index')

# Filter for the scrape of fulltext
metadata_df['peer_reviewed'] = metadata_df['comments'].apply(is_peer_reviwed)
metadata_df = metadata_df.loc[metadata_df['peer_reviewed']].reset_index(drop=True)


############################################################
##################### GET PDFS OF TEXT #####################
############################################################

# Sachita will fill this out at 5pm CT