# Import libraries
import requests
import psycopg2
from bs4 import BeautifulSoup
import pandas as pd
from database import Database
from notification import Notification
from config import config

notif_config = config(section="notification")
notif = Notification(notif_config)

db = Database(config())
db.connect()

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
            aud_rmb_rate = float(cells[3].findAll(string=True)[0])
            timestamp = cells[6].findAll(string=True)[0]
            break

if aud_rmb_rate is not None:
    print(f'{aud_rmb_rate} - {timestamp}')
    try:
        cursor = db.conn.cursor()
        # select lastest data from db
        select_latest_query = "select cr.time, cr.rate from currencyRecord cr order by cr.time DESC limit 1"
        cursor.execute(select_latest_query)
        latest_record = cursor.fetchone()
            
        if latest_record is not None and len(latest_record) >= 2:
            if aud_rmb_rate - latest_record[1] < 0:
                notif.send_msg(f"Latest rate: {aud_rmb_rate} @ {timestamp}\nDropped {aud_rmb_rate - latest_record[1]}")
        
        frequency = 30
        if notif_config["frequency"] is not None:
            frequency = notif_config["frequency"]        
        select_lowest_value_query = f"""SELECT cr.time, cr.rate
                                FROM currencyRecord cr
                                WHERE  date_trunc('day', cr.time) <= date_trunc('day', current_timestamp) AND
                                date_trunc('day', cr.time) > date_trunc('day', current_timestamp - interval '{frequency} days')
                                order by cr.rate limit 1;
                               """
        cursor.execute(select_lowest_value_query)
        lowest_record = cursor.fetchone()
        if lowest_record is not None and len(lowest_record) >= 2:
            print(f"Lowest rate: {lowest_record[1]} @ {lowest_record[0]} for last {frequency} days")
            if lowest_record[1] >= aud_rmb_rate:
                notif.send_msg(f"Lowest rate now!!! {aud_rmb_rate} @ {timestamp} for last {frequency} days\nLast lowest rate: {lowest_record[1]} @ {lowest_record[0]}\nDropped by {lowest_record[1] - aud_rmb_rate}")
                                 
        # insert latest data into database
        cursor.execute("insert into currencyrecord(rate, time) values(%s, %s)", (aud_rmb_rate, timestamp))
        db.conn.commit()
    except psycopg2.errors.UniqueViolation as uniqueError:
        print(uniqueError)
    except (Exception, psycopg2.Error) as error :
        raise Exception(f"DB connection error: ", error)
    finally:
        db.disconnect(cursor)
else:
    print(f'Australian dollar not found')
    db.disconnect()