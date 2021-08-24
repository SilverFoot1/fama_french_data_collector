
def remove_values(stock_df):
    # Select all stocks where the name does NOT contain the word 'Smartshares'
    stock_df = stock_df.loc[~stock_df['Name'].str.contains('Smartshares'), :]

    # rows that contain nulls.
    dropped_data = stock_df[stock_df.isnull().any(axis=1)]

    # Drop rows that contain nulls.
    stock_df.dropna(inplace=True)
    print('Final Data Shape ', stock_df.shape)

    return [stock_df, dropped_data]


def create_features(stock_df):

    # Creates column which is the % difference between yesterday and today's price.
    stock_df['pct_change'] = (stock_df['CurrentPrice'] / stock_df['PreviousClose']) - 1

    # todo make it error proof if book value is 0
    # Creates column for the book to market ratio i.e. Stock price / Book price.
    stock_df['B/M'] = stock_df['CurrentPrice'] / stock_df['BookValue']

    # Stocks that had no price change.
    print('Number of 0% Change in Returns: ', stock_df['pct_change'].isin([0]).sum(axis=0))

    return stock_df


def create_final_row(stocks, factors):

    # Creates a dictionary object where the index is the Ticker name, and the value is the pct_change, and stringifies.
    returns_json = str(stocks.set_index('Ticker').to_dict()['pct_change'])

    # Creates new column for this JSON object containing stock returns.
    factors['Returns'] = returns_json

    print(factors.to_string())

    return factors
