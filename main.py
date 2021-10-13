import os
import requests
from requests.exceptions import HTTPError
from urllib.parse import urlparse

from dotenv import load_dotenv


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
    return response.json()['total_clicks']


def is_bitlink(token, url_parsed):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(
        url=f"https://api-ssl.bitly.com/v4/bitlinks/{url_parsed.netloc}{url_parsed.path}",
        headers=headers)
    return response.ok


def main():
    load_dotenv()
    BIT_TOKEN = os.environ.get("BIT_TOKEN")
    url = input()
    url_parsed = urlparse(url)
    try:
        if is_bitlink(BIT_TOKEN, url_parsed):
            clicks = count_clicks(BIT_TOKEN, f"{url_parsed.netloc}{url_parsed.path}")
            print(f"{url} переходов: {clicks}")
        else:
            bitlink = shorten_link(BIT_TOKEN, url)
            print("Битлинк", bitlink)
    except requests.exceptions.HTTPError:
        print(f"HTTPError in: {url}")
    except Exception as e:
        print(e, url)


if __name__ == "__main__":
    main()
