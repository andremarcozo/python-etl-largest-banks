import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime
import lxml
import sqlite3
from queries import queries_list
import json

url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"

first_table_attributes =['Name', 'MC_USD_Billion']
final_table_attributes = ['Name', 'MC_USD_Billion', 'MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion']

csv_path = 'Largest_banks_data.csv'
exchange_path = '/home/traive/Documentos/ESTUDOS/python-project-for-data-engeneering/exchange_rate.csv'
queries_result_path = 'Queries_results.csv'


db_name = '	Banks.db'
table_name = 'Largest_banks'

log_path = 'code_log.txt'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def log_message(message, log_path = log_path):

    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_path, 'a') as f:
        f.write(f"{timestamp} - {message}\n")


def extract(url, columns):
    final_table = []

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        
        rows = table.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            if len(cols) >=3:
                name = cols[1].get_text(strip=True)
                market_cap = cols[2].get_text(strip=True)
                final_table.append([name, market_cap])

    except Exception as e:
        print(f'Scrap failed with error: {e}')

    
    df = pd.DataFrame(final_table, columns=columns)    

    return(df)


def transform(df, csv_path = exchange_path):
    df['MC_USD_Billion'] = pd.to_numeric(df['MC_USD_Billion'], errors='coerce')

    exchange_df = pd.read_csv(csv_path)
    exchange_rate = exchange_df.set_index('Currency').to_dict()['Rate']

    df['MC_GBP_Billion'] = (df['MC_USD_Billion'] * float(exchange_rate['GBP'])).round(2)
    df['MC_EUR_Billion'] = (df['MC_USD_Billion'] * float(exchange_rate['EUR'])).round(2)
    df['MC_INR_Billion'] = (df['MC_USD_Billion'] * float(exchange_rate['INR'])).round(2)

    return df

    
def load_to_csv(df, csv_path = csv_path):
     df.to_csv(csv_path, index=False)


def load_to_db(df, db_name, table_name, connection):
    df.to_sql(table_name, connection, if_exists='replace', index=False)




def run_queries(queries, conn):

    
    for query in queries:        
        print(query)
        query_result = pd.read_sql(query, conn)
        print(query_result)
        print("-" * 50)
        



# df = extract(url, first_table_attributes)

# print(df)



log_message('Preliminaries complete. Initiating ETL process')

df = extract(url, first_table_attributes)

log_message('Data extraction complete. Initiating Transformation process')

df = transform(df, exchange_path)

log_message('Data transformation complete. Initiating loading process')

load_to_csv(df)

log_message('Data saved to CSV file')

conn = sqlite3.connect(db_name)

log_message('SQL Connection initiated')


load_to_db(df, db_name, table_name, conn)


log_message('Data loaded to Database as a table, Executing queries')

run_queries(queries_list, conn)

log_message('Process Complete')

conn.close()

log_message('Server Connection closed')



 


  