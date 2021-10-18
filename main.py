import argparse
import logging
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError


def shorten_link(token, url):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    options = {
        "long_url": url
    }
    response = requests.post(
        url="https://api-ssl.bitly.com/v4/shorten",
        headers=headers,
        json=options)
    response.raise_for_status()
    return response.json()["link"]


def count_clicks(token, short_url):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    options = {
        "unit": "day",
        "units": -1
    }
    response = requests.get(
        url=f"https://api-ssl.bitly.com/v4/bitlinks/{short_url}/clicks/summary",
        headers=headers,
        params=options)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(token, url):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(
        url=f"https://api-ssl.bitly.com/v4/bitlinks/{url}",
        headers=headers)
    return response.ok


def main():
    load_dotenv()
    bit_token = os.environ.get("BIT_TOKEN")
    parser = argparse.ArgumentParser(description="Transform url to bitly link")
    parser.add_argument(
        "url",
        type=str,
        help="use 'python main.py {url}'"
        )
    args = parser.parse_args()
    url = args.url
    url_components = urlparse(url)
    checked_url = f"{url_components.netloc}{url_components.path}"
    try:
        if is_bitlink(bit_token, checked_url):
            clicks = count_clicks(bit_token, checked_url)
            print(f"{url} переходов: {clicks}")
        else:
            bitlink = shorten_link(bit_token, url)
            print("Битлинк", bitlink)
    except requests.exceptions.HTTPError as error:
        print(f"HTTPError in: {url}: {error}")
        logging.error(f" HTTPError in: {url}: {error}")



if __name__ == "__main__":
    main()
