import datetime
import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def collect_data(city_code='12122', city='Москва'):
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    ua = UserAgent()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User.Agent': ua.random
    }

    cookies ={
        'location_id': f'{city_code}'
    }


    response = requests.get(url='https://5ka.ru/special_offers', headers=headers, cookies=cookies)
    with open(f'index.html', 'w', encoding='UTF-8') as file:
        file.write(response.text)


    with open('index.html', 'rb')as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    list = soup.find('div',class_='items-list')
    print(list)
    cards = soup.find_all('div', class_='product-card item')

    with open(f'{city}_{cur_time}.csv', 'w', encoding='UTF-8')as file:
        writer = csv.writer(file)
        writer.writerow(('Продукты','Старая цена','Новая цена','Скидка','Время акции'))

    for card in cards:
        card_title = card.find('div', class_='item-name').text.strip()
        try:
            card_discount = card.find('div', class_='discount-hint hint').text.strip()
        except AttributeError:
            continue
        card_price_old_i = card.find('div', class_='price-right').find('span', class_='price-regular').text.strip()
        card_price_old_d = card.find('div', class_='price-right').find('sup').text.strip()

        card_old_price = f'  {card_price_old_i}'.strip()#{card_price_old_d}'

        card_price_now_i = card.find('div', class_='price-discount').find('span').text.strip()
        card_price_now_d = card.find('div', class_='price-right').find('span', class_='price-discount_cents').text.strip()

        card_price_now = f'  {card_price_now_i}.{card_price_now_d}'[4::]

        sell_date = card.find('div', class_='item-date').text.strip()
        with open(f'{city}_{cur_time}.csv', 'a', encoding='UTF-8') as file:
            writer = csv.writer(file)
            writer.writerow((card_title, card_old_price,card_price_now,card_discount,sell_date))



    print(f'Файл {city} {cur_time} успешно записан!')
def main():
    collect_data(city_code='12122')

if __name__=='__main__':
    main()

#location_id=12207 Брянск
#location_id=12122 Москва