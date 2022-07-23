from requests import get as requests
from app.models import Other
from random import randint as rand
from time import time

btc_reload = None
eth_reload = None

def eth(count):
    global eth_reload
    if int(time()) - int(eth_reload) >= 0:
        etherium = float(requests("https://api.etherscan.io/api?module=stats&action=ethprice&apikey=ABOBA").json()['result']['ethusd'])
        Other.objects.filter(id=1).update(etherium = etherium)
        eth_reload = time() + 36000
    kurs = int(Other.objects.get(id = 1).etherium) * count
    return kurs

def btc(count):
    global btc_reload
    if int(time()) - int(btc_reload) >= 0:
        bitcoin = requests('https://blockchain.info/ticker').json()
        Other.objects.filter(id=1).update(bitcoins = bitcoin['USD']['buy'])
        btc_reload = time() + 36000
    kurs = int(Other.objects.get(id=1).bitcoins) * count
    return kurs

def rating(user):
    if user.rating > 1000000000:
        user.rating = Decimal(1000000000)
        user.save()
    return user.digit_number(user.rating)

if __name__ != '__main__':
    btc_reload = time() + 36000
    eth_reload = time() + 36000
