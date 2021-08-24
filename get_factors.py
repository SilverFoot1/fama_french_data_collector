import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import date, datetime


def get_factors(data, market_return):
    """
    SIZE:
    B = Big (High market cap)
    S = Small (Low market cap)

    VALUE:
    N = Neutral
    G = Growth (low B/M)
    V = Value (high B/M)
    """

    # returns 6 portfolios for each of the categories needed to calculate factors. Returns 6 DFs.
    BG, BN, BV, SG, SN, SV = get_portfolios(data)

    # Risk Free Rate: Returns Float.
    rfr = get_risk_free_rate()

    # Calculates the 'Small minus Big' factor. Returns float.
    SMB = calculate_SMB(BG, BN, BV, SG, SN, SV)

    # Calculates the 'High minus Low' factor. Returns float
    HML = calculate_HML(BV, SV, BG, SG)

    # Calculates 'Market Premium' or 'Excess Market Return' i.e. market return minus the risk free rate.
    MKT_RF = market_return - rfr

    # Creates a string from today's date in a day/month/year format
    date_string = (date.today()).strftime(" %d/%m/%Y")

    row = {
        'Date': [],
        'MKT_RF': [],
        'SMB': [],
        'HML': [],
        'RFR': []
    }

    # Appending all the data to lists within a dictionary.
    row['Date'].append(date_string)
    row['MKT_RF'].append(MKT_RF)
    row['SMB'].append(SMB)
    row['HML'].append(HML)
    row['RFR'].append(rfr)
    print('reached end of get_factors')

    return pd.DataFrame(row)


def get_portfolios(data):

    # The median Market cap
    median = data['MarketCap'].median()
    cols = data.columns

    large_rows = []
    small_rows = []

    # Resetting the indexes to 0,1,2, etc..
    data.reset_index(drop=True, inplace=True)

    print('get portfolio code')
    print(len(data))
    print(data.to_string())

    #   Iterates over the stock DF via index, and splits in half, using the median as the middle point. It nesting lists
    #   inside lists.
    for i in data.index:
        print('up to ', i)
        if data['MarketCap'][i] > median:
            large_rows.append(list(data.iloc[i]))
        else:
            small_rows.append(list(data.iloc[i]))

    # Creating dataframes from the nested lists.
    large = pd.DataFrame(large_rows, columns=cols)
    small = pd.DataFrame(small_rows, columns=cols)

    # Sorting the small and large DFs according to the B/M ratios of the stocks.
    large.sort_values('B/M', inplace=True)
    small.sort_values('B/M', inplace=True)

    # The number that corresponds to 30% of the DFs length.
    split_index = round(len(large) * 0.3)

    # Splitting the sorted big and small DFs according to the index value.
    big_growth = large[0: split_index]
    big_neutral = large[: -split_index]
    big_value = large[-split_index:]

    small_growth = small[0: split_index]
    small_neutral = small[split_index: -split_index]
    small_value = small[-split_index:]

    return big_growth, big_neutral, big_value, small_growth, small_neutral, small_value


def get_risk_free_rate():

    # Site that lists the risk free rate
    rf_rate_resp = requests.get('https://www.nzfma.org/')
    rate_soup = BeautifulSoup(rf_rate_resp.text, 'html.parser')
    rfr_part = rate_soup.select('#data > div > div:nth-child(6) > div:nth-child(2) > div.MoSTFormLayoutCell2')
    rfr = (float(rfr_part[0].text[6:12]) * 4) / 365

    return rfr


def calculate_SMB(BG, BN, BV, SG, SN, SV):

    # Mean return of the small stocks minus the mean return of the large stocks.
    avg_small = pd.concat([SG['pct_change'], SN['pct_change'], SV['pct_change']]).mean()
    avg_large = pd.concat([BG['pct_change'], BN['pct_change'], BV['pct_change']]).mean()

    return avg_small - avg_large


def calculate_HML(BV, SV, BG, SG):

    # The mean return of the value stocks, minus the mean return of the growth stocks.
    avg_value = pd.concat([BV['pct_change'], SV['pct_change']]).mean()
    avg_growth = pd.concat([BG['pct_change'], SG['pct_change']]).mean()

    return avg_value - avg_growth
