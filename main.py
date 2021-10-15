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


def is_bitlink(token, url_components):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(
        url=f"https://api-ssl.bitly.com/v4/bitlinks/{url_components.netloc}{url_components.path}",
        headers=headers)
    return response.ok


def main():
    load_dotenv()
    bit_token = os.environ.get("BIT_TOKEN")
    url = input()
    url_components = urlparse(url)
    try:
        if is_bitlink(bit_token, url_components):
            clicks = count_clicks(bit_token, f"{url_components.netloc}{url_components.path}")
            print(f"{url} переходов: {clicks}")
        else:
            bitlink = shorten_link(bit_token, url)
            print("Битлинк", bitlink)
    except requests.exceptions.HTTPError:
        print(f"HTTPError in: {url}")
    except Exception as e:
        print(e, url)


if __name__ == "__main__":
    main()
