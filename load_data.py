import pandas as pd
import sqlite3


def load_data(new_row):

    # Create DB connection and cursor
    conn = sqlite3.connect('factor_db.sqlite')
    cursor = conn.cursor()

    # Selecting the first row from the single row DF passed in.
    row = new_row.iloc[0, :].values

    # Insert statement using parameters.
    cursor.execute('''
        INSERT INTO factors (date_stamp, mkt_rf, smb, hml, rfr, nz_returns)
        VALUES (?, ?, ?, ?, ?, ?);
    ''', (row[0], row[1], row[2], row[3], row[4], row[5]))

    # Commit and close DB
    print('Loaded to Database')
    conn.commit()
    conn.close()

    # Reading the excel doc.
    excel_data = pd.read_excel('excel_files/factor_data.xlsx')

    # Needed for the first data entry. If excel file is empty it creates a column.
    if 'Unnamed: 0' in excel_data.columns:
        excel_data.drop('Unnamed: 0', axis=1, inplace=True)

    # Adding row to DF, and overwriting it to the excel doc.
    updated = pd.concat([excel_data, new_row], ignore_index=True)
    updated.to_excel('excel_files/factor_data.xlsx')
    print('Loaded to Excel')
