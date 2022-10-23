from bs4 import BeautifulSoup
import requests
from requests.models import parse_url

URL_RABOTA = 'https://rabota.by/search/vacancy?area=1002&fromSearchLine=true&text=python'
HEADERS_RABOTA = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

def get_html_rabota(url):
    r = requests.get(url, headers=HEADERS_RABOTA)
    return r

def get_content_rabota(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='vacancy-serp-item')
    jobs = []
    for item in items:
        jobs.append({
            f'Должность:{item.find("a", class_="bloko-link").get_text()}': f"Компания: {item.find('a', class_='bloko-link bloko-link_secondary').get_text()}",
            "Cсылка": item.find('a', class_='bloko-link').get('href')
        })
    return jobs

def parser_rabota():
    page = 0
    text = []
    while True:     
        html = get_html_rabota(URL_RABOTA+'&page='+str(page))
        print('Parsing' ,URL_RABOTA+'&page='+str(page))
        if html.status_code == 200:
            text += get_content_rabota(html.text)
            if len(get_content_rabota(html.text)) < 1: break
            page += 1
        else:
            break

    with open('my_file.csv', 'w', encoding='utf-8') as file:
        for i in range(len(text)):
            [file.write('{0},{1}\n'.format(key, value)) for key, value in text[i].items()]
    return text

if __name__ == '__main__':
    print(parser_rabota())