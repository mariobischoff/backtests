import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import pytz
from dotenv import load_dotenv
import os
load_dotenv()

account = int(os.environ['LOGIN'])
password = os.environ['PASS']
server = os.environ['SERVER']

if not mt5.initialize(login=account, server=server, password=password):
    print("initialize() failed, error code =",mt5.last_error())
    quit()

authorized=mt5.login(account, password, server)
authorized
mt5.last_error()
print(mt5.account_info())

timezone = pytz.timezone("America/Sao_Paulo")
utc_from = datetime(2023, 1, 1, tzinfo=timezone)
utc_to = datetime(2023, 9, 14, tzinfo=timezone)

rates = mt5.copy_rates_range("WIN$", mt5.TIMEFRAME_M5, utc_from, utc_to)

df = pd.DataFrame(rates)

df['time'] = pd.to_datetime(df['time'], unit='s')
df.set_index('time', inplace=True)
df.drop(columns=['tick_volume', 'spread', 'real_volume'], inplace=True)
df.to_csv('data/win.csv')