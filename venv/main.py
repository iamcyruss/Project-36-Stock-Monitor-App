import os
import requests
import datetime
from datetime import datetime, timedelta
from twilio.rest import Client

WEEKDAY = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
TICKER_DATA_API = os.environ.get("TICKER_DATA_API")
TICKER_ENDPOINT = "https://www.alphavantage.co/query"
TICKER_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "datatype": "json",
    "apikey": TICKER_DATA_API,
}

sms_list = 'Incoming Data: \n'
# get yesterday and day after from datetime
current_date = datetime.now()
#print(current_date.strftime("%A"))
#print(current_date.today())
yesterday = current_date - timedelta(1)
day_after = current_date - timedelta(2)
yesterday_name = yesterday.strftime("%A")
#print(yesterday_name)
day_after_name = day_after.strftime("%A")
#print(day_after_name)
if day_after_name == "Sunday":
    # yesterday is monday day after that is sunday this will change day after to last friday
    yesterday_list = str(yesterday).split()
    day_after = current_date - timedelta(4)
    day_after_name = day_after.strftime("%A")
    day_after_list = str(day_after).split()
elif day_after_name == "Saturday":
    yesterday = current_date - timedelta(2)
    yesterday_name = yesterday.strftime("%A")
    yesterday_list = str(yesterday).split()
    day_after = current_date - timedelta(3)
    day_after_name = day_after.strftime("%A")
    day_after_list = str(day_after).split()
else:
    yesterday_list = str(yesterday).split()
    day_after_list = str(day_after).split()

#print(yesterday)
#print(day_after)
#print(day_after_list)

# get ticker data by date
ticker_response = requests.get(TICKER_ENDPOINT, params=TICKER_PARAMS)
ticker_response.raise_for_status()
ticker_data = ticker_response.json()["Time Series (Daily)"]
#print(ticker_data)
#print(ticker_data[yesterday_list[0]])
#print(ticker_data[day_after_list[0]])
try:
    yesterdays_ticker_data = ticker_data[yesterday_list[0]]
    day_after_ticker_data = ticker_data[day_after_list[0]]
except KeyError:
    print(f"One of these two days ({yesterday_list[0]} and {day_after_list[0]}) must be a holiday because there's no ticker data")
except TypeError:
    print("hi")
#print(ticker_data)
#print(TICKER_PARAMS)
#print(f"ACCOUNT: {SMS_ACCOUNT_SID} and AUTH: {SMS_AUTH_TOKEN}")

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
if yesterdays_ticker_data and day_after_ticker_data:
    #print(yesterdays_ticker_data)
    #print(day_after_ticker_data)
    #print(day_after_ticker_data["1. open"])
    #print(yesterdays_ticker_data['1. open'])
    #check to see if the day_after open is 5% higher or lower to the yesterdays open
    day_after_five = (float(day_after_ticker_data['1. open']) * 2.0) * .01
    print(str(day_after_five))
    day_after_ticker_data_open = float(day_after_ticker_data['1. open'])
    yesterdays_ticker_data_open = float(yesterdays_ticker_data['1. open'])
    print(day_after_ticker_data_open - day_after_five)
    print(day_after_ticker_data_open + day_after_five)
    if day_after_ticker_data_open < yesterdays_ticker_data_open:
        print("Price went up.")
        percent_change = (abs(yesterdays_ticker_data_open - day_after_ticker_data_open) /
                          day_after_ticker_data_open) * 100.0
        print(str(percent_change))
        if day_after_ticker_data_open < yesterdays_ticker_data_open - day_after_five:
            print(f'it went up more than 5%. Day_after open: {str(day_after_ticker_data_open)}. '
                  f'Yesterday open: {str(yesterdays_ticker_data_open)}. Which is a {str(percent_change)}% change.')
            five_percent = True
            sms_list = sms_list + (f"{STOCK}: 🔺{str(percent_change)[0:4]}%\nComparing Date: {day_after_list[0]} Open: "
                            f"{str(day_after_ticker_data_open)} to Date: {yesterday_list[0]} "
                            f"Open: {str(yesterdays_ticker_data_open)}\n")
        else:
            print("The change was within 5%.")
    elif day_after_ticker_data_open > yesterdays_ticker_data_open + day_after_five:
        print("Price went down.")
        percent_change = (abs(yesterdays_ticker_data_open - day_after_ticker_data_open) /
                          day_after_ticker_data_open) * 100.0
        print(str(percent_change))
        if day_after_ticker_data_open + day_after_five < yesterdays_ticker_data_open:
            print(f'it went down more than 5%. Day_after open: {str(day_after_ticker_data_open)}. '
                  f'Yesterday open: {str(yesterdays_ticker_data_open)}. Which is a {str(percent_change)}% change.')
            five_percent = True
            sms_list = sms_list + (f"{STOCK}: 🔻{str(percent_change)[0:4]}%\nComparing Date: {day_after_list[0]} Open: "
                                   f"{str(day_after_ticker_data_open)} to Date: {yesterday_list[0]} "
                                   f"Open: {str(yesterdays_ticker_data_open)}\n")
        else:
            print("The change was within 5%.")
    else:
        print("The change was within 5%.")


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
NEWS_SEARCH = "\"Tesla -Inc\" AND \"TSLA\""
NEW_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_DATA_API = os.environ.get("NEWS_DATA_API")
NEWS_PARAMS = {
    "apiKey": NEWS_DATA_API,
    "q": NEWS_SEARCH,
    "sortBy": "relevancy",
    "from": day_after_list[0],
    "to": yesterday_list[0],
}

news_response = requests.get(NEW_ENDPOINT, params=NEWS_PARAMS)
news_response.raise_for_status()
news_data = news_response.json()
#print(news_data['articles'])
#print(news_data['articles'][0]['title'])
if len(news_data['articles']) >= 3:
    for article in range(2):
        #print(news_data['articles'][article])
        #print(news_data['articles'][article]['publishedAt'])
        #print(news_data['articles'][article]['title'])
        #print(news_data['articles'][article]['description'])
        #print(news_data['articles'][article]['url'])
        sms_list = sms_list + (f"Article Date: {news_data['articles'][article]['publishedAt'].split('T')[0]}\n"
                               f"Headline: {news_data['articles'][article]['title']}\n"
                               f"Brief: {news_data['articles'][article]['description']}\n"
                               f"Link: {news_data['articles'][article]['url']}\n")
else:
    for article in range(len(news_data['articles'])):
        #print(news_data['articles'][article])
        #print(news_data['articles'][article]['publishedAt'])
        #print(news_data['articles'][article]['title'])
        #print(news_data['articles'][article]['description'])
        #print(news_data['articles'][article]['url'])
        sms_list = sms_list + (f"Article Date: {news_data['articles'][article]['publishedAt'].split('T')[0]}\n"
                               f"Headline: {news_data['articles'][article]['title']}\n"
                               f"Brief: {news_data['articles'][article]['description']}\n"
                               f"Link: {news_data['articles'][article]['url']}\n")

print(sms_list)
## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

SMS_ACCOUNT_SID = os.environ.get("SMS_ACCOUNT_SID")
SMS_AUTH_TOKEN = os.environ.get("SMS_AUTH_TOKEN")
FROM_ = +19474652240
client = Client(SMS_ACCOUNT_SID, SMS_AUTH_TOKEN)
if five_percent:
    message = client.messages.create(body=sms_list, from_=FROM_, to='+14253810699')
    print(message.sid)
#todays_list =
#message = client.messages.create(body=todays_list, from_=from_, to='+14253810699')
#print(message.sid)

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

