from bs4 import BeautifulSoup
import requests
import pandas as pd
import yfinance as yf
from yahoofinancials import YahooFinancials


def extract_stock_tickers():

    # Url containing all the NZ stock tickers
    wiki_url = 'https://en.wikipedia.org/wiki/List_of_companies_listed_on_the_New_Zealand_Exchange'

    # Requesting the webpage, and turning to a soup object.
    response = requests.get(wiki_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Selecting the table element from the soup, that has the tickers
    table = soup.select_one('table.wikitable')

    # Iterating over the table to get ticker values.
    tickers = []
    for item in table.select('.external.text'):

        # all NZ tickers are 3 chars in length
        if len(item.text) == 3:

            # Specific cases for abnormal stocks
            if item.text == 'AKL':
                tickers.append(item.text+'.AX')
                continue

            # not actually listed stocks: DOW too small, FNZ is index, MOA not listed, TLS is ASX
            if item.text in ['DOW', 'FNZ', 'MOA', 'TLS']:
                continue

            # majority of normal public stocks
            else:
                tickers.append(item.text + '.NZ')

    return tickers


def extract_stock_data(tickers):
    stock_data = {
        'Ticker': [],
        'Name': [],
        'CurrentPrice': [],
        'PreviousClose': [],
        'Beta': [],
        'BookValue': [],
        'MarketCap': []
    }

    # to capture invalid values that don't have a book value key pair.
    no_book_value = []

    for stock in tickers:
        print('up to: ' + stock)

        # dictionary with all the stock information
        data = (yf.Ticker(stock)).info

        # Most common reason to cause an error is not having a book value, and it is easiest to do a check here.
        # This doesn't mean book value was null, rather that there is no key value for book value in the returned object
        if 'bookValue' not in data.keys():
            no_book_value.append(stock)
            continue

        # appending all the data to the appropriate list in the dictionary object
        stock_data['Ticker'].append(stock)
        stock_data['Name'].append(data['shortName'])
        stock_data['Beta'].append(data['beta'])
        stock_data['BookValue'].append(data['bookValue'])
        stock_data['MarketCap'].append(data['marketCap'])
        stock_data['CurrentPrice'].append(data['currentPrice'])
        stock_data['PreviousClose'].append(data['previousClose'])

    # The stocks that were removed due to having no book value.
    print('No Book Values: ', no_book_value)

    return pd.DataFrame(stock_data)


def extract_market_return():

    # Get data for the NZX50 index.
    nzx_50 = yf.Ticker('^NZ50').info

    # 'Return of Market' (rm), the % change in price from yesterday to today of the index.
    rm = (nzx_50['regularMarketPrice'] / nzx_50['previousClose']) - 1

    return rm


