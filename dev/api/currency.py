import requests
import socket
import urllib.parse

def main():

    # Parsing URL
    url = "http://data.fixer.io/api/latest"

    url_parse = urllib.parse.urlsplit(url)

    # Making sure hostname is resolved
    try:
        socket.gethostbyname(url_parse.hostname)
    except socket.error:
        print("ERROR: API request unsuccessful")

    # Parameters for HTTP request
    access_key = "2e3ee8f5320fb9ca89d63387caf8fcdd"
    symb = "CAD"

    # Send a request
    res = requests.get(url, params={"access_key":access_key, "symbols":symb})

    # Making sure request is successful
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful")

    # Getting JSON data
    data = res.json()

    # Working with data
    print(data)




if __name__ == "__main__":
    main()
