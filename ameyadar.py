# coding: UTF-8
import json, os, time, math, urllib.request
from requests_oauthlib import OAuth1Session
import datetime as dt
from scipy.stats import norm

# Twitter API
twitter = OAuth1Session(os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"], os.environ["ACCESS_TOKEN"], os.environ["ACCESS_TOKEN_SECRET"])

# Yahoo API
YAHOO_APP_ID = os.environ["YAHOO_APP_ID"]

COORDINATES = '135.7849,35.02799' # longitude and latitude
rainEmoji = ['🌂', '🌦', '☂️', '🌧', '☔', '⛈', '🌀']

rain_url = 'https://map.yahooapis.jp/weather/V1/place?coordinates=%s&appid=%s&output=json&interval=10'%(COORDINATES,YAHOO_APP_ID)
response = urllib.request.urlopen(rain_url)
content = json.loads(response.read().decode('utf-8'))
rainfall = 0
emoji = ''
for var in range(7):
    x = norm.pdf(var, 0, 5)/norm.pdf(0, 0, 5)
    y = content['Feature'][0]['Property']['WeatherList']['Weather'][var]['Rainfall']
    rainfall += x*y
if rainfall != 0:
    cubed = min(math.ceil(math.log(math.ceil(rainfall),3)), 6)
    emoji = rainEmoji[cubed]
req0 = twitter.get('https://api.twitter.com/1.1/account/verify_credentials.json')
oldName = json.loads(req0.text)['name']
for num in range(7):
    oldName = oldName.replace(rainEmoji[num],"")
newName = oldName.replace(defaultEmoji,"") + emoji
reqPost1 = twitter.post('https://api.twitter.com/1.1/account/update_profile.json?name=%s'%newName)
print("new name: "+newName)
