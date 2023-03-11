# google-takeout
## Overview
Scripts for aiding in Google Takeout

When trying to extract your data from Google Photos, you are often left with a miriad of .zip files of photos. Once you have extracted them, the takeout.py file can scan all files for dates and metadata, ready to upload to another photo storage cloud service (such as iCloud).

To run, simply:

python takeout.py <INPUT FOLDER> <OUTPUT FOLDER>

The script will scan files in the <INPUT FOLDER> for files with a date and output them to the <OUTPUT FOLDER> under either "files_with_dates" or "files_without_dates" folders.

This will help you decide whether you would like to upload them or not.

## Setup
run `pip install -r requirements.txt` and then run the script: `python takeout.py`
