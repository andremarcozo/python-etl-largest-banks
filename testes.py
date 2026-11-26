import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
import lxml
from io import StringIO


url = "https://en.wikipedia.org/wiki/List_of_largest_banks"

first_table_attributes =['Name', 'MC_USD_Billion']
final_table_attributes = ['Name', 'MC_USD_Billion', 'MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion']

csv_path = 'Largest_banks_data.csv'

db_name = '	Banks.db'
table_name = 'Largest_banks'

log_path = 'code_log.txt'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}


html=requests.get(url, headers=headers).text
tabelas = pd.read_html(StringIO(html), match="Market cap")
df = tabelas[0]
df = df.drop(df.columns[1], axis=1)

df.columns = ['Name', 'MC_USD_Billion']


print(df)


