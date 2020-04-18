import threading
import time
from queue import Queue

from Control.Crawler.CrawlerEquities import CrawlerEquities, get_data_frame_from_site_data
from Control.Crawler.Currencies import Currencies
from config import list_currency_crawlers, list_investing_crawlers, SLEEP_TIME
from instance.db import CrawlerDb

# SLEEP_TIME = 1

queue_investing = Queue()
queue_currency = Queue()


def crawler_investing(filter_id, need_convert_from_dollar):
    crawler = CrawlerEquities(filter_id)
    results = crawler.get_site_data()

    data_frame = get_data_frame_from_site_data(results, need_convert_from_dollar)
    data_frame.to_csv(str(filter_id) + '-' + str(time.time()) + ".csv", sep=",", index=False)

    queue_investing.put(
        {
            "need_convert_from_dollar": need_convert_from_dollar,
            "filter_id": filter_id,
            "crawled_data": data_frame
        }
    )


def crawler_currencies(currency_conversion):
    crawler = Currencies(currency_conversion)
    result = crawler.get_site_data()

    queue_currency.put(
        {
            "type": "currency",
            "filter_id": currency_conversion,
            "crawled_data": result
        }
    )


def get_threads():
    crawler_threads = []
    for crawler in list_investing_crawlers:
        crawler_threads.append(threading.Thread(target=crawler_investing,
                                                args=[crawler["filter_id"],
                                                      crawler["currency"] != "brl"]))

    for crawler in list_currency_crawlers:
        crawler_threads.append(
            threading.Thread(target=crawler_currencies,
                             args=[crawler["currency_conversion"]])
        )

    return crawler_threads


def convert_dollar_to_brl(data_frame, currency_dollar_to_brl):
    """
    Use the Currency information to convert values and generate columns with value in brl.
    :param data_frame: pandas.DataFrame
    :param currency_dollar_to_brl: Model.Currency
    :return:
    """
    brl = currency_dollar_to_brl.value
    # TO DO: Treat values with a comma
    # data_frame["last_rs"] = data_frame["last_usd"] * brl
    data_frame["last_rs"] = ""
    # data_frame["high_rs"] = data_frame["high_usd"] * brl
    data_frame["high_rs"] = ""
    # data_frame["low_rs"] = data_frame["low_usd"] * brl
    data_frame["low_rs"] = ""
    return data_frame


if __name__ == '__main__':
    crawler_bd = CrawlerDb()
    crawler_bd.create_schema()

    while 1:
        threads = get_threads()
        # Init the process
        for thread in threads:
            thread.start()

        while threads:
            # the crawl is still active
            for thread in threads:
                if not thread.is_alive():
                    # remove the stopped threads
                    threads.remove(thread)

            time.sleep(1)

        currency_dollar = {}
        # after craw process ends start the currency conversion
        if not queue_currency.empty():
            currency = queue_currency.get()
            currency_data = currency["crawled_data"]
            # insert currency into database
            crawler_bd.insert_currency(currency_data)
            if currency_data.currency == "USD/BRL":
                currency_dollar = currency_data

        while not queue_investing.empty():
            investing = queue_investing.get()
            # process dollar conversion
            if investing["need_convert_from_dollar"]:
                if currency_dollar:
                    equity_nasdaq_data_frame = convert_dollar_to_brl(investing["crawled_data"], currency_dollar)

                    equity_nasdaq_data_frame.to_csv(str(currency_data.currency).replace("/", "-") + '-' +
                                                    str(time.time()) + ".csv", sep=",", index=False)
                    crawler_bd.insert_nasdaq_list(equity_nasdaq_data_frame)

            else:
                crawler_bd.insert_ibovespa_list(investing["crawled_data"])

        time.sleep(SLEEP_TIME)
