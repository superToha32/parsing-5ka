import datetime
import requests
import json
import csv
import decoder
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
def collect_data(city_code='12122', city='Москва'):
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    ua = UserAgent()
    cookies = {
        'location_id': f'{city_code}'
    }
    with open(f'{city}_5k.csv', 'w', encoding='UTF-8')as file:
        writer = csv.writer(file)
        writer.writerow(('Продукты','Старая цена','Новая цена','Скидка','Время акции'))
    n=1
    while True:
        try:
            response = requests.get(url=f'https://5ka.ru/api/v2/special_offers/?records_per_page=15&page={n}&store=&ordering=&price_promo__gte=&price_promo__lte=&categories=&search=', cookies=cookies)
        except AttributeError:
            break
        str = response.text
        i = str.find('[')
        arr = str[i+2:-3:].split('},{')
        for y in arr:
            dic = json.loads('{'+y+'}')
            try:
                name = dic['name']
            except:
                break
            old_price =dic['current_prices']['price_reg__min']
            cur_price =dic['current_prices']['price_promo__min']
            discount =100 - cur_price*100//old_price
            sell_date = dic['promo']['date_end']
            with open(f'{city}_5k.csv', 'a', encoding='UTF-8') as file:
                writer = csv.writer(file)
                writer.writerow((name, old_price, cur_price, discount, sell_date))
        n = n+1
def main():
    #collect_data(city_code='12207')
    collect_data(city_code='12122')

if __name__=='__main__':
    main()