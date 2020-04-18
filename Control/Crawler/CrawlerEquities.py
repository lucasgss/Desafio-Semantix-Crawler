import requests
import pandas as pd
from Control.Comun import get_page_soup_by_url
from Model.IBovespa import Investing


def get_data_frame_from_site_data(crawler_result, need_convert_from_dollar):
    data = get_investing_structure(need_convert_from_dollar)
    for equity in crawler_result:
        data["name"].append(equity.name)

        if not need_convert_from_dollar:
            data["last_rs"].append(equity.last)
            data["high_rs"].append(equity.high)
            data["low_rs"].append(equity.low)
        else:
            data["last_usd"].append(equity.last)
            data["high_usd"].append(equity.high)
            data["low_usd"].append(equity.low)

        data["chg"].append(equity.chg)
        data["chg_percent"].append(equity.chg_percent)
        data["vol"].append(equity.vol)
        data["time"].append(equity.time)

    return pd.DataFrame(data)


def get_investing_structure(need_convert_from_dollar):
    data = {"name": []}

    if need_convert_from_dollar:
        data["last_usd"] = []
        data["high_usd"] = []
        data["low_usd"] = []
    else:
        data["high_rs"] = []
        data["low_rs"] = []
        data["last_rs"] = []

    data["chg"] = []
    data["chg_percent"] = []
    data["vol"] = []
    data["time"] = []
    return data


class CrawlerEquities:
    """Navigate to the website https://www.investing.com/equities/StocksFilter?index_id={<FILTER ID>}
        and extract information"""

    def __init__(self, index_id):
        self.url = "https://www.investing.com/equities/StocksFilter?index_id={0}".format(index_id)

    def get_site_data(self):
        """navigate to the url and extract the information"""
        # url = 'https://www.investing.com/equities/StocksFilter?index_id=17920'
        # url = 'https://www.investing.com/equities/StocksFilter?index_id=20'
        try:
            page_soup = get_page_soup_by_url(self.url)

            return self.__get_equities(page_soup)

        except requests.exceptions.HTTPError:
            # TODO: GENERATE LOG
            return None
        except AttributeError:
            # TODO: GENERATE LOG
            return None

    def __get_equities(self, page_soup):
        """
        Get the Equity list in the page.
        :param page_soup: bs4.BeautifulSoup
        :return: List of Investing
        """
        equities_list = page_soup.select("#cross_rate_markets_stocks_1 tbody tr")

        investing_list = []
        for equity_information in equities_list:
            equity_information = [text.get_text(strip=True) for text in equity_information]

            investing_list.append(
                Investing(equity_information[1],
                          str(equity_information[2]).replace(",", ""),
                          str(equity_information[3]).replace(",", ""),
                          str(equity_information[4]).replace(",", ""),
                          equity_information[5], equity_information[6],
                          equity_information[7], equity_information[8]))
        return investing_list
