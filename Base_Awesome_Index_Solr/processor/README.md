# Overview

This script processes records from staging\_pre to staging\_post.

# Requirements

Requirements are defined in requirements.txt.  Simply run `pip install -r requirements.txt` 

# Usage

After installing the needed requirements, the script can be run from anywhere that has access to the pre/post collections. 

The script maintains state of processed records in a local sqlite db, to initialize that database, first run:

`python init.py`

After the database is initialized, you can process items by running the following:

`python processor.py`

If items are removed in drupal, they will be removed from the post index the next time the script is run.
