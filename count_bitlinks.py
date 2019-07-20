import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse


def shorten_link(long_url, token):
    bitlink_create_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    json_payload = {
        'long_url': long_url,
    }

    response = requests.post(bitlink_create_url, headers=headers,
                                 json=json_payload)
    response.raise_for_status()
    return response

def count_bitlink_clicks(bitlink_url, token):
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    payload = {
        'units': -1,
        'unit': 'day'
    }

    parsed_url = urlparse(bitlink_url)
    bitlink_id = parsed_url.netloc + parsed_url.path
    bitlink_count_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks'\
        .format(bitlink_id)
    response = requests.get(bitlink_count_url, headers=headers, params=payload)
    response.raise_for_status()
    return response


def get_bitlink_info(bitlink_url, token):
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }

    parsed_url = urlparse(bitlink_url)
    bitlink_id = parsed_url.netloc + parsed_url.path
    bitlink_info_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}' \
        .format(bitlink_id)

    response = requests.get(bitlink_info_url, headers=headers)
    response.raise_for_status()
    return requests

def show_clicks_for_bitlink(response):
    link_clicks = response.json()['link_clicks']
    for click in link_clicks:
        print('Дата: {}, кликов: {}'.format(click['date'], click['clicks']))


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(
        description='Программа сокращает ссылки или выводит кол-во переходов по уже сокращенным.'
    )
    parser.add_argument('url', help='Адрес ссылки (URL)')
    args = parser.parse_args()

    api_token = os.getenv('BITLY_API_TOKEN')
    api_url = 'https://api-ssl.bitly.com/v4/user'

    url = args.url
    try:
        response = get_bitlink_info(url, token=api_token)
    except requests.exceptions.HTTPError:
        try:
            response = shorten_link(long_url=url, token=api_token)
            shortened_link = response.json()['link']
            print('Сокращенная ссылка: {}'.format(shortened_link))
            exit()
        except requests.exceptions.HTTPError as error:
            print(error)
            exit(2)

    try:
        response = count_bitlink_clicks(bitlink_url=url, token=api_token)
    except requests.exceptions.HTTPError as error:
        print(error)
        exit(2)
    show_clicks_for_bitlink(response)

