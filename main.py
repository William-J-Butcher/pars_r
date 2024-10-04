import requests
import json
import random
import time
import pandas as pd
import cloudscraper
from bs4 import BeautifulSoup
import lxml


def get_data(url, n):

    # сгенерировано через curl на сайте https://curlconverter.com/
    cookies = {
        'ring': '04e7d6c7b83cf573ff1dcb306df007d6',
        '_ga': 'GA1.1.1205222096.1727782762',
        'sentinel': 'hjSUrwSZjc/NBovOFEC59D92sU0z3K5nb3nv7FVGQrFSFvyw3DTv5OfeERlwZWRCWSuxWqtiLe9AhBPpiIquUENTbT0ux+O7w'
                    'SUfpkyEbOo=:yNWXJ7Z52Z9OnRIxIaA/FC8EUSlGR15Q21UrlWwjbEY=',
        '_ga_98VH35E9J1': 'GS1.1.1727858397.4.1.1727858549.60.0.0',
        'ring_session': '1.4.1727782733.1727858368.1727858533.PYZSmsDtYBwCu4XFjTk4Y6t0oKLQEI1FpKgMHTbJ228%3D',
        '_ga_G0RWKN84TQ': 'GS1.1.1727858397.4.1.1727858561.48.0.0',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'priority': 'u=1, i',
        'referer': 'https://www.farpost.ru/vladivostok/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"129.0.6668.71"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/129.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    response = requests.get(url=url, headers=headers)
    print(f'Статус код страницы: {response.status_code}')  # response.status_code)

    scrap = cloudscraper.create_scraper()
    page = 1
    apartments_data_dict = []
    valid_count = 0  # Счетчик валидных объявлений

    while valid_count < n:
        url = f'https://www.farpost.ru/vladivostok/realty/sell_flats/?page={page}'
        response = scrap.get(url=url, cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        apartments_cards = soup.find_all('div', class_='descriptionCell bull-item__cell bull-item__description-cell')

        for apartment_card in apartments_cards:
            try:
                apartment_description = apartment_card.find('div', class_='bull-item__subject-container').find('a').text
                apartment_description = apartment_description.replace('\"', "'").replace('\n', ' ')
            except Exception:
                apartment_description = 'Description is not found'

            try:
                apartment_price = apartment_card.find('div', class_='price-block__price').text
            except Exception:
                apartment_price = 'Price is not found'

            try:
                apartment_square_price = apartment_card.find('div', class_="bull-item__additional-price").text
            except Exception:
                apartment_square_price = 'Square price is not found'

            try:
                apartment_url = 'https://www.farpost.ru' + apartment_card.find('div', class_='bull-item__subject-container').find('a').get('href')
            except Exception:
                apartment_url = 'URL is not found'

            try:
                apartment_square = apartment_card.find('div', class_='bull-item__annotation').text.strip()
                apartment_square = apartment_square.replace(' ', '')
                apartment_square = apartment_square.split(', ')
                apartment_square = [item for item in apartment_square if 'кв.м.' in item]
                apartment_square = apartment_square[0]
            except Exception:
                apartment_square = 'Square is not found'

            # Условие валидности объявления
            if (
                'not found' not in apartment_description and
                'not found' not in apartment_price and
                'not found' not in apartment_square_price and
                'not found' not in apartment_square and
                'not found' not in apartment_url
            ):
                apartments_data_dict.append({
                    'description': apartment_description,
                    'square': apartment_square,
                    'price': apartment_price,
                    'square price': apartment_square_price,
                    'url': apartment_url
                })
                valid_count += 1  # Увеличиваем счетчик валидных объявлений
                print(f'Валидных объявлений: {valid_count}')

            # Прерывание после достижения n валидных объявлений
            if valid_count == n:
                break
                print(f'Найдено {valid_count} валидных объявлений.')

        time.sleep(random.randrange(2, 15))
        page += 1

        print(f'количество валидных объявлений: {valid_count}')
        print(page)
        print()

    # Сохранение данных в JSON
    with open('/data/apartments_data_dict.json', 'w', encoding='utf-8') as file:
        json.dump(apartments_data_dict, file, indent=4, ensure_ascii=False)

    with open('/data/apartments_data_dict.json', encoding='utf-8') as file:
        data = json.load(file)

    # Создание Excel таблицы
    df = pd.DataFrame.from_dict(data)
    df.to_excel('/data/data.xlsx', index=False, engine='openpyxl')


if __name__ == '__main__':
    # Укажите количество валидных объявлений, после которых нужно прекратить выполнение
    get_data('https://www.farpost.ru/vladivostok/realty/sell_flats/?page=1', n=300)
