import requests
from bs4 import BeautifulSoup
import time
import json
import signal


URL = 'https://ru.investing.com/crypto/'

def get_html(url, params=None):
    r = requests.get(url,headers = {'User-agent': 'your bot 0.1'} ,params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    prices = soup.find_all('td', class_='price js-currency-price')
    names = soup.find_all('td', class_='left bold elp name cryptoName first js-currency-name')   

    crypto_names = []
    crypto_price = []              
    
    for name in names:
        crypto_names.append(name.find().get_text())

    for price in prices:
        crypto_price.append(price.find().get_text())



    crypto_dict = dict(zip(crypto_names, crypto_price))

    with open('ready.json', 'w', encoding='utf-8') as file:
        json.dump(crypto_dict, file,indent=4 ,ensure_ascii=False)


    return crypto_dict

run = True
def signal_handler(signal, frame):
    global run
    print("exiting")
    run = False

signal.signal(signal.SIGINT, signal_handler)


def parse():
    html = get_html(URL)
    while run:
        if html.status_code == 200:
            print(get_content(html.text))
            time.sleep(10)
            parse()
        else:
            print("Error")


if __name__ == '__main__':
    print(parse())