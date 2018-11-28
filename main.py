import requests
import os
import argparse
from dotenv import load_dotenv


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("link")
    return parser.parse_args()


def is_bitlink(link, headers=dict()):
    api_url = "https://api-ssl.bitly.com/v4/bitlinks/{}".format(link)
    response = requests.get(api_url, headers=headers)
    return response.ok


def get_shortlink(long_url, headers=dict()):
    data = {"long_url": long_url, "units": -1}
    api_url = "https://api-ssl.bitly.com/v4/bitlinks"
    response = requests.post(api_url, json=data, headers=headers)
    return response.json()["link"] if response.ok else None


def get_bit_clicks(link, headers=dict()):
    api_url = "{}{}{}".format(
        "https://api-ssl.bitly.com/v4/bitlinks/",
        link,
        "/clicks/summary",
    )
    response = requests.get(api_url, headers=headers)
    return response.json()["total_clicks"] if response.ok else None


def main():
    load_dotenv()
    token = os.getenv("token")
    link = get_args().link
    headers = {"Authorization": "Bearer {}".format(token)}
    if link and token:
        if is_bitlink(link, headers):
            result = get_bit_clicks(link, headers)
            result_description = "Переходов по ссылке: "
        else:
            result = get_shortlink(link, headers)
            result_description = "Ваша ссылка: "
        if result is None:
            print("Incorrect url")
        else:
            print("{}{}".format(result_description, result))
    else:
        print("Wrong Args")


if __name__ == "__main__":
    main()
