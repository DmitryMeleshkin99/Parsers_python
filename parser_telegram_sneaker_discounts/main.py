from bs4.builder import HTMLTreeBuilder
import requests
from bs4 import BeautifulSoup
import json
import urllib


URL_SNEAKERHEAD = 'https://sneaker-head.by/muzhskie/'
HEADERS_SNEAKERHEAD = {'accept': '*/*',
           'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
        
        }
HOST_MULTISPORT = 'https://multisports.by'
URL_MULTISPORT = 'https://multisports.by/catalog/_sale/obuv/'
HEADERS_MULTISPORT = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}


def get_html_multisport(url, params=None):
    r = requests.get(url,headers = HEADERS_MULTISPORT ,params=params)  #MULTISPORT SHOP
    return r


def get_html_sneakerhead(url, params=None):
    r = requests.get(url,headers = HEADERS_SNEAKERHEAD ,params=params)      #SNEAKERHEAD 
    return r

def get_content_sneakerhead(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='product rounded', href=True)
    sneakerhead_discount = []
    for item in items:
        sneakerhead_discount.append({
            'title': item.find('h2').get_text(),
            'link':  item['href'],
            #'sale': item.find('div', class_='sale-price').get_text(),
            'price': item.find('span', class_='currency').get_text(),
            'image': item.find("img")["src"]
        })


    

    with open('ready.json', 'w', encoding='utf-8') as file:
        json.dump(sneakerhead_discount, file,indent=4 ,ensure_ascii=False)

    return sneakerhead_discount


def get_content_multisport(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='product-card product-not-available element-shadow-hover')
    multisport_discoun = []
    for item in items:
        old_price = item.find('span', class_='old-price text-small text-gray')
        if old_price:
            old_price = old_price.get_text().strip()
        else:
            old_price = 'Старую цену уточняйте!'
        multisport_discoun.append({
            'title': item.find('a', class_='product-name text-fw-bold').get_text(),
            'link': HOST_MULTISPORT + item.find('a', class_='wrap-img product-img').get('href'),
            'price': item.find('span', class_='cur-price text-fw-bold').get_text().strip(),
            'old_price': old_price,
        })




    with open('ready_multisport.json', 'w', encoding='utf-8') as file:
        json.dump(multisport_discoun,file,indent=4, ensure_ascii=False)

    return multisport_discoun




def parser_sneakerhead():
    html_sneakerhead = get_html_sneakerhead(URL_SNEAKERHEAD)

    if html_sneakerhead.status_code == 200:
        return get_content_sneakerhead(html_sneakerhead.text)
    else:
        print('Oops Sneakerhead No connection')

def parser_multisport():
    html_multisport = get_html_multisport(URL_MULTISPORT)

    if html_multisport.status_code == 200:
        return get_content_multisport(html_multisport.text)
    else:
        print('Oops Multisport No Connectionn')



if __name__ == "__main__":
    print(parser_sneakerhead())
    #print(parser_multisport())


