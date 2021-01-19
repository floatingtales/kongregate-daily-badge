import schedule
import time
import webbrowser
import ssl
import re
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

kongpanionurl = 'https://www.kongregate.com/badges'

def badge():

    print('retreiving:', kongpanionurl)

    html = urllib.request.urlopen(kongpanionurl, context = ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    dayblob = str(soup('a', class_='btn btn_action phl imgExt'))

    gameurl = re.findall('www.kongregate.com/[^\"]+', dayblob)

    print("opening:", gameurl)

    webbrowser.open(gameurl[0],2)

#scheduler
schedule.every().day.at("17:00").do(badge)

while True:
    schedule.run_pending()
    time.sleep(1)
