# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.boc.cn/sourcedb/whpj/"
page = requests.get(url)
# encoding as chinese simplified chars
page.raise_for_status()
page.encoding = "utf-8"

soup = BeautifulSoup(page.text, 'lxml')

table= soup.select_one('.publish .main+table')
target_currency = "澳大利亚元"
aud_rmb_rate = None
timestamp = None

for row in table.findAll("tr"):
    cells = row.findAll("td")
    if len(cells) >=8:
        currency_name = cells[0].findAll(string=True)
        if len(currency_name) > 0 and currency_name[0] == target_currency:
            aud_rmb_rate = cells[3].findAll(string=True)[0]
            timestamp = cells[6].findAll(string=True)[0]
            break

if aud_rmb_rate is not None:
    print(f'{aud_rmb_rate} - {timestamp}')
else:
    print(f'Australian dollar not found')