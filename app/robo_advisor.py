# this is the "app/robo_advisor.py" file
import csv
import json
import os
from dotenv import load_dotenv
import requests
from pandas import DataFrame
import plotly.express as px
from pprint import pprint
from datetime import datetime
import statistics

load_dotenv

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)
data_choice = str.strip(input("Please choose between stocks or crypto:"))
if data_choice == "stocks" or data_choice == "crypto":
    print(f"REQUESTING {data_choice} DATA...")
else:
    print("INVALID CHOICE. Please selected either stocks or crypto data")
    data_choice = str.strip(input("Please choose between stocks or crypto:"))
# ask for user input 
if data_choice == "stocks":
    symbol = str.strip(input("Please choose a stock ticker to search (e.g. MSFT):"))
    # symbol1, symbol2 = str.strip(input("Please choose a stock ticker to search (i.e. MSFT):")).split()

    # Validate a user input

    print("-------------------------")
    print(f"SELECTED SYMBOL: {symbol}")
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")

    api_key = os.environ.get("ALPHAVANTAGE_API_KEY") 
    # try except source: https://www.w3schools.com/python/python_try_except.asp
    try:
        stock_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}"
        response = requests.get(stock_url)
        parsed_response = json.loads(response.text)

        last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

        tsd = parsed_response["Time Series (Daily)"]
    except:
        print("INVALID ticker. Please run the program again with a valid ticker symbol")
        exit()
    records = []
    for date, daily_data in tsd.items():
         record = {
             "date": date,
             "open": daily_data["1. open"],
             "high": daily_data["2. high"],
             "low": daily_data["3. low"],
             "close": daily_data["5. adjusted close"],
             "volume": int(daily_data["6. volume"]),
         }
         records.append(record)
    
    df = DataFrame(records)
    
    #
    # INFO INPUTS
    #
    # EXPORT TO CSV

    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"{symbol}_prices.csv")
    df.to_csv(csv_file_path)

    # code for datetime = https://www.geeksforgeeks.org/get-current-date-using-python/

    print(f"REQUEST AT: {datetime.now()}")
    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed}")
    print("LATEST CLOSE: ", to_usd(float(records[0]["close"])))
    print("RECENT HIGH: ", to_usd(float(df["high"].max())))
    print("RECENT LOW: ", to_usd(float(df["low"].min())))
    print("-------------------------")
    ten_day_average = (float(records[1]["close"]) + float(records[2]["close"]) + float(records[3]["close"]) + float(records[4]["close"]) + float(records[5]["close"]) + float(records[6]["close"]) + float(records[7]["close"]) + float(records[8]["close"]) + float(records[9]["close"]) + float(records[10]["close"]))/10
    if float(records[0]["close"]) > float(ten_day_average): 
        print("RECOMMENDATION: BUY")
    else: 
         print("RECOMMENDATION: SELL")
    print("RECOMMENDATION REASON:The most recent closing price of", to_usd(float(records[0]["close"])), "is compared to the ten day average price of", to_usd(float(ten_day_average)))
    print("-------------------------")
    print(f"WRITING DATA TO CSV: {csv_file_path}...")
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")

    # CHART PRICES OVER TIME

    fig = px.line(df, y="close", x="date", title=f"Closing Prices for {symbol.upper()}") # see: https://plotly.com/python-api-reference/generated/plotly.express.line
    fig.update_yaxes(autorange="reversed")
    fig.show()
else:
    symbol = str.strip(input("Please choose a crypto currency to search (e.g.BTC):"))
    # symbol1, symbol2 = str.strip(input("Please choose a stock ticker to search (i.e. MSFT):")).split()

    # Validate a user input

    print("-------------------------")
    print(f"SELECTED SYMBOL: {symbol}")
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")

    api_key = os.environ.get("ALPHAVANTAGE_API_KEY") 
    # try except source: https://www.w3schools.com/python/python_try_except.asp
    try:
        crypto_url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey={api_key}"
        response = requests.get(crypto_url)
        parsed_response = json.loads(response.text)

        last_refreshed = parsed_response["Meta Data"]["6. Last Refreshed"]

        tsd = parsed_response["Time Series (Digital Currency Daily)"]
    except:
        print("INVALID crypto currency. Please run the program again with a valid crypto currency")
        exit()
    records = []
    for date, daily_data in tsd.items():
         record = {
             "date": date,
             "open": daily_data["1a. open (USD)"],
             "high": daily_data["2a. high (USD)"],
             "low": daily_data["3a. low (USD)"],
             "close": daily_data["4a. close (USD)"],
             "volume": int(daily_data["5. volume"]),
         }
         records.append(record)
    
    df = DataFrame(records)
    
    #
    # INFO INPUTS
    #
    # EXPORT TO CSV

    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"{symbol}_prices.csv")
    df.to_csv(csv_file_path)

    # code for datetime = https://www.geeksforgeeks.org/get-current-date-using-python/

    print(f"REQUEST AT: {datetime.now()}")
    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed}")
    print("LATEST CLOSE: ", to_usd(float(records[0]["close"])))
    print("RECENT HIGH: ", to_usd(float(df["high"].max())))
    print("RECENT LOW: ", to_usd(float(df["low"].min())))
    print("-------------------------")
    ten_day_average = (float(records[1]["close"]) + float(records[2]["close"]) + float(records[3]["close"]) + float(records[4]["close"]) + float(records[5]["close"]) + float(records[6]["close"]) + float(records[7]["close"]) + float(records[8]["close"]) + float(records[9]["close"]) + float(records[10]["close"]))/10
    if float(records[0]["close"]) > float(ten_day_average): 
        print("RECOMMENDATION: BUY")
    else: 
         print("RECOMMENDATION: SELL")
    print("RECOMMENDATION REASON:The most recent closing price of", to_usd(float(records[0]["close"])), "is compared to the ten day average price of", to_usd(float(ten_day_average)))
    print("-------------------------")
    print(f"WRITING DATA TO CSV: {csv_file_path}...")
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")

    # CHART PRICES OVER TIME

    fig = px.line(df, y="close", x="date", title=f"Closing Prices for {symbol.upper()}") # see: https://plotly.com/python-api-reference/generated/plotly.express.line
    fig.update_yaxes(autorange="reversed")
    fig.show()