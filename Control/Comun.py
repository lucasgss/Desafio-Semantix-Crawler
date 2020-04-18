import requests
from bs4 import BeautifulSoup as Soup
import re


def get_page_soup_by_url(url):
    """
    Request the url, parse the result and return the object BeautifulSoup
    :param url: String
    :return: bs4.BeautifulSoup
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.163 Safari/537.36'}
    page_html = requests.get(url, headers=headers)
    page_html.raise_for_status()

    return Soup(page_html.content, "html.parser")


def clear_text(text):
    """use Regex to remove characters from string"""
    return re.sub(r'([\s\r\n]+|\s*\Z)|(\s*\Z|\s*[\r\n]+ )', '', text, flags=re.MULTILINE)
