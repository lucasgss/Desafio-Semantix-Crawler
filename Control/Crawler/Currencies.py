import requests
from Control.Comun import get_page_soup_by_url, clear_text
from Model.Currency import Currency
import re


class Currencies:
    """Navigate to the website https://m.investing.com/currencies/{currency to-currency from} and extract information
        Example: https://m.investing.com/currencies/usd-brl
    """

    def __init__(self, currency_conversion):
        """:param currency_conversion: currency_conversion format example: usd-brl"""
        self.url = "https://m.investing.com/currencies/{0}".format(currency_conversion)

    def get_site_data(self):
        """navigate to the url and extract the information"""
        # url = 'https://m.investing.com/currencies/usd-brl'
        try:
            page_soup = get_page_soup_by_url(self.url)

            formatted_currency = self.__get_currency_conversion(page_soup)

            currency_information = self.__get_currency_information_list(page_soup)

            return Currency(formatted_currency, currency_information[0], currency_information[1],
                            currency_information[2], currency_information[3])

        except requests.exceptions.HTTPError as http_Error:
            # TODO: GENERATE LOG
            return None
        except AttributeError:
            # TODO: GENERATE LOG
            return None

    def __get_currency_information_list(self, page_soup):
        """
        Get currency information's in the page.
        """
        # GET the tags Span and I, if there are classes names that contains "pid-2103".
        currency_information = page_soup.find_all(['span', 'i'], attrs={'class': re.compile('^pid-2103*')})
        # Clear the information removing whitespace, tab, or line break character
        return [text.get_text(strip=True) for text in currency_information]

    def __get_currency_conversion(self, page_soup):
        """
        Get currency conversion information in the page.
        """
        line_currency = page_soup.select(".instrumentH1inlineblock")
        return clear_text(line_currency[0].get_text()).split('-')[0]
