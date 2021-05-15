import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from dotenv import dotenv_values

config = dotenv_values(".env")
api_key = config.get('OWM_API_KEY')
account_sid = config.get("ACCOUNT_SID")
auth_token = config.get("AUTH_TOKEN")
current_lat = 12.114993
current_lon = -86.236176

parameters = {
   "lat": current_lat,
   "lon": current_lon,
   "appid": api_key,
   "exclude": "current,minutely,daily"
}
print(api_key)
print(account_sid)
print(auth_token)

response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()
data = response.json()
data_slices = data["hourly"][:12]


def send_message(forecast_message):
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=forecast_message,
        from_=config.get("SENDER"),
        to='Your recipient number'
    )

    print(message.sid)


for hour_data in data_slices:
    if int(hour_data["weather"][0]["id"]) < 300:
        send_message("The forecast for today is an storm, stay safe")
        break
    elif int(hour_data["weather"][0]["id"]) < 400:
        send_message("Today will be cloudy with patchy drizzle")
        break
    elif int(hour_data["weather"][0]["id"]) < 600:
        send_message("It's going to rain today, bring an ☂️")
        break
    elif int(hour_data["weather"][0]["id"]) < 700:
        send_message("It's going to snow today ⛄️️")
        break
    elif int(hour_data["weather"][0]["id"]) < 800:
        send_message("Today will be atmospheric phenomena")
        break
    elif int(hour_data["weather"][0]["id"]) == 800:
        send_message("Today will be sunshine day ☀️ enjoy it!")
        break
    else:
        send_message("It's going to be cloudy in the next hours ☁️")
        break
