import os
import requests
import datetime
from datetime import datetime, timedelta

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
TICKER_DATA_API = os.environ.get("TICKER_DATA_API")
TICKER_ENDPOINT = "https://www.alphavantage.co/query"
SMS_ACCOUNT_SID = os.environ.get("SMS_ACCOUNT_SID")
SMS_AUTH_TOKEN = os.environ.get("SMS_AUTH_TOKEN")
FROM_ = +19474652240
TICKER_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "datatype": "json",
    "apikey": TICKER_DATA_API,
}


# get yesterday and day after from datetime
current_date = datetime.now()
print(current_date.today())
yesterday = str(current_date - timedelta(1)).split()
day_after = str(current_date - timedelta(2)).split()
print(yesterday)
print(day_after)

# get ticker data by date
ticker_response = requests.get(TICKER_ENDPOINT, params=TICKER_PARAMS)
ticker_response.raise_for_status()
ticker_data = ticker_response.json()["Time Series (Daily)"]
yesterdays_ticker_data = ticker_data[yesterday[0]]
day_after_ticker_data = ticker_data[day_after[0]]
print(ticker_data)
print(TICKER_PARAMS)
print(f"ACCOUNT: {SMS_ACCOUNT_SID} and AUTH: {SMS_AUTH_TOKEN}")

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def get_stock_data():
    if yesterdays_ticker_data and day_after_ticker_data:
        print(yesterdays_ticker_data)
        print(day_after_ticker_data)
        print(day_after_ticker_data["1. open"])
        print(yesterdays_ticker_data['1. open'])
        day_after_five = (float(day_after_ticker_data['1. open']) * 5.0) * .01
        print(float(day_after_ticker_data['1. open']) - day_after_five)
        print(float(day_after_ticker_data['1. open']) + day_after_five)
        if day_after_ticker_data['1. open'] < yesterdays_ticker_data['1. open']:
            if float(day_after_ticker_data['1. open']) - day_after_five < float(yesterdays_ticker_data['1. open']):
                print('it went down more than 5%')
        elif day_after_ticker_data['1. open'] < yesterdays_ticker_data['1. open']:
            if float(day_after_ticker_data['1. open']) + day_after_five < float(yesterdays_ticker_data['1. open']):
                print('it went up more than 5%')


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
NEWS_SEARCH = "\"Tesla -Inc\" AND \"TSLA\""
NEW_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_DATA_API = os.environ.get("NEWS_DATA_API")
NEWS_PARAMS = {
    "apiKey": NEWS_DATA_API,
    "q": NEWS_SEARCH,
    "sortBy": "relevancy",
    "from": day_after[0],
    "to": yesterday[0],
}

news_response = requests.get(NEW_ENDPOINT, params=NEWS_PARAMS)
news_response.raise_for_status()
news_data = news_response.json()
#print(len(news_data['articles']))
#print(news_data['articles'][0]['title'])
if len(news_data['articles']) >= 3:
    for article in range(2):
        print(news_data['articles'][article]['title'])
        print(news_data['articles'][article]['description'])
else:
    for article in news_data['articles']:
        print(news_data['articles'][article]['title'])
        print(news_data['articles'][article]['description'])

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

