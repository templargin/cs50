import requests
import socket
import urllib.parse
import os

def get_data_API(isbns):

    # Parsing URL
    url = "https://www.goodreads.com/book/review_counts.json"

    url_parse = urllib.parse.urlsplit(url)

    # Making sure hostname is resolved
    try:
        socket.gethostbyname(url_parse.hostname)
    except socket.error:
        #print("ERROR: Could not resolve the host")
        return None

    # Parameters for HTTP request
    # SAVE GOODREADS_KEY as an environmental variable
    access_key = os.getenv("GOODREADS_KEY")

    # Send a request
    try:
        res = requests.get(url, params={"access_key":access_key, "isbns":isbns})
    except requests.exceptions.ConnectionError as e:
        print("ERROR: API request unsuccessful")
        return None

    # Making sure request is successful
    if res.status_code != 200:
        # raise Exception("ERROR: API request unsuccessful")
        return None

    # Getting JSON data
    data = res.json()

    # return data
    return data
