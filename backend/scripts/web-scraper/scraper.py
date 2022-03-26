from email import header
from tkinter.tix import MAX
from typing import Counter
from requests import exceptions
import argparse
import requests
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()

# Image Search Query (Ex: Medium Rare Steak)
ap.add_argument("-q", "--query", required=True,
    help="search query to search Bing Image API for")

# Output directory for images
ap.add_argument("-o", "--output", required=True,
    help="path to output directory of images")
args = vars(ap.parse_args())

API_KEY = "dd789163a74e4d50915967b30ae5dd15"
MAX_RESULTS = 1000 # Max results per search
GROUP_SIZE = 200 # Max of 50 results per request

# Endpoint API URL
URL = "https://api.bing.microsoft.com/v7.0/images/search"

EXCEPTIONS = set([IOError, FileNotFoundError,
	exceptions.RequestException, exceptions.HTTPError,
	exceptions.ConnectionError, exceptions.Timeout])


term = args["query"]
headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
params = {"q": term, "offset": 0, "count": GROUP_SIZE}

# make the search
print("[INFO] searching Bing API for '{}'".format(term))
search = requests.get(URL, headers=headers, params=params)
search.raise_for_status()

# grab the results from the search, including the total number
# of estimated results returned by the Bing API
results = search.json()
estNumResults = min(results['totalEstimatedMatches'], MAX_RESULTS)
print("[INFO] {} total results for '{}'".format(estNumResults,
    term))

# initialize the total number of images downloaded thus far
total = 0

# loop over the estimated number of results in 'GROUP_SIZE' groups
for offset in range(0, estNumResults, GROUP_SIZE):
	# update the search parameters using the current offset, then
	# make the request to fetch the results
	print("[INFO] making request for group {}-{} of {}...".format(
		offset, offset + GROUP_SIZE, estNumResults))
	params["offset"] = offset
	search = requests.get(URL, headers=headers, params=params)
	search.raise_for_status()
	results = search.json()
	print("[INFO] saving images for group {}-{} of {}...".format(
		offset, offset + GROUP_SIZE, estNumResults))

# loop over the results
for v in results["value"]:
    # try to download the image
    try:
        # make a request to download the image
        print("[INFO] fetching: {}".format(v["contentUrl"]))
        r = requests.get(v["contentUrl"], timeout=30)
        # build the path to the output image
        ext = v["contentUrl"][v["contentUrl"].rfind("."):]
        p = os.path.sep.join([args["output"], "{}{}".format(
            str(total).zfill(8), ext)])
        # write the image to disk
        f = open(p, "wb")
        f.write(r.content)
        f.close()
    
    # catch errors
    except Exception as e:
        # checks if exception is in list of exceptions to check for
        if type(e) in EXCEPTIONS:
            print("[INFO] skipping: {}".format(v['contentUrl']))
            continue

    # try to load the image from disk
    image = cv2.imread(p)
    # if the image is `None` then we could not properly load the
    # image from disk (so it should be ignored)
    if image is None:
        print("[INFO] deleting: {}".format(p))
        os.remove(p)
        continue
    # update the counter
    total += 1