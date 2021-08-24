
from extract_stock_data import extract_stock_tickers, extract_stock_data, extract_market_return
from clean_transform_data import remove_values, create_features, create_final_row
from get_factors import get_factors
from load_data import load_data


if __name__ == '__main__':

    # returns a list of stock tickers
    tickers = extract_stock_tickers()

    # returns a dataframe of all relevant stock data
    raw_data = extract_stock_data(tickers)

    # Exports raw data to excel file
    raw_data.to_excel('excel_files/Raw_Stock_Data.xlsx')

#     remove nulls and unwanted stocks. Returns [DF, DF]
    clean_data, dropped_data = remove_values(raw_data)

    # Store preliminary data in excel
    clean_data.to_excel('excel_files/Clean_Stock_Data.xlsx')
    print('Length of Cleaned Data: ', len(clean_data))

    # Adds columns for book/market ratio, and the percentage change in returns. Returns DF.
    feature_data = create_features(clean_data)

    # Extracts NZX50 index data, and calculates it percentage return from the prior closing price. Returns float.
    market_return = extract_market_return()

    # Creates the portfolios and calculates the factor values used by the Fama-French model. Returns DF.
    factors = get_factors(feature_data, market_return)

    # adds a column to factor DF containing a JSON object, that holds all the % stock returns. Returns DF
    final_row = create_final_row(feature_data, factors)

    # Updates the DB and excel file with the newly created final row.
    load_data(final_row)

