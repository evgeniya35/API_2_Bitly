import requests
from requests import exceptions
from requests.exceptions import HTTPError
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()

def shorten_link(token, url):
    headers = {
        "Authorization": "Bearer " + token
    }
    options = {
        "long_url": url
    }
    response = requests.post(url="https://api-ssl.bitly.com/v4/shorten", headers=headers, json=options)
    response.raise_for_status()
    return response.json()


def count_clicks(token, short_url):
    headers = {
        "Authorization": "Bearer " + token
    }
    options = {
        "unit": "day",
        "units": -1
    }
    response = requests.get(url=f"https://api-ssl.bitly.com/v4/bitlinks/{short_url}/clicks/summary", headers=headers, params=options)
    response.raise_for_status()
    return response.json()


def is_url(url):
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
    except ValueError:
        return False


def is_bitlink(url):
    return url == "bit.ly"


def is_bitlink_api(token, parsed):
    headers = {
        "Authorization": "Bearer " + token
    }
    response = requests.get(url=f"https://api-ssl.bitly.com/v4/bitlinks/{parsed.netloc}{parsed.path}", headers=headers)
    response.raise_for_status()
    bit = response.json()
    return bit["id"] == parsed.netloc + parsed.path

    
def main():
    url = "https://proglib.io/p/ne-izobretat-velosiped-ili-obzor-modulya-collections-v-python-2019-12-15"
    token = "cf242e3e8a06d3faadcfcb10650d3726e2a50a57"
    url = "https://bit.ly/3DpixNc"
    parsed = urlparse(url)
    try:
        if is_bitlink(parsed.netloc):
            if is_bitlink_api(token, parsed):
                clicks = count_clicks(token, parsed.netloc + parsed.path)
                print(f"{url} переходов: {clicks['total_clicks']}")
        else:
             bitlink = shorten_link(token, url)
             print("Битлинк", bitlink["link"])
    except requests.exceptions.HTTPError:
        print("HTTPError in: " + url)
    except Exception as e:
        print(e, url)
    else:
        pass

    

    """
    try:
        total_clicks = count_clicks(token, short_url)
    except requests.exceptions.HTTPError:
        print(HTTPError)
    except Exception as e:
        print(e)
    else:
        print("total_clicks", total_clicks["total_clicks"])
    
    try:
        bitlink = shorten_link(token, long_url)["link"]
    except requests.exceptions.HTTPError:
        print("HTTPError")
    except Exception as e:
        print(e)
    else:
        print("Битлинк", bitlink)
    """

if __name__ == "__main__":
    main()