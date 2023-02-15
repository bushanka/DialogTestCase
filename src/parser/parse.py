import aiohttp
import aiofiles
import asyncio
import numpy as np
import csv
import datetime
from bs4 import BeautifulSoup
from aiocsv import AsyncDictWriter


async def save_to_csv(file_name, data):
    """
    Сохраняет данные в csv файл.
    :param data: Данные, которые нужно сохранить
    :param file_name: имя файла
    :return: None
    """
    async with aiofiles.open(file_name, mode="w", encoding="utf-8", newline="") as afp:
        writer = AsyncDictWriter(afp, [
            'Product', 'Discount', 'OldPrice', 'NewPrice', 'PromotionTime'
        ], restval="NULL", quoting=csv.QUOTE_ALL)
        await writer.writeheader()
        await writer.writerows(data)


async def parse_magnit(city):
    """
    Функция парсит данные с сайта магнита.
    :param city: город, в котором функция парсит промо-товары
    :return: имя файла, в который записались данные по товарам
    """

    cookies_data = {'mg_geo_id': '2398'} if city == 'Москва' else {'mg_geo_id': '2425'}

    async with aiohttp.ClientSession(cookies=cookies_data) as session:
        async with session.get('https://magnit.ru/promo/', timeout=10) as response:
            html_code = await response.text()

        soup = BeautifulSoup(html_code, 'html.parser')
        all_promo_products = soup.find_all(class_='card-sale card-sale_catalogue')

        promo_info = np.empty(len(all_promo_products), dtype=dict)

        for i, promo_product in enumerate(all_promo_products):
            title = promo_product.find(class_='card-sale__title').text

            promo_time = " ".join(t.text for t in promo_product.find(class_='card-sale__date').find_all('p'))

            new_price = ".".join(
                t.text for t in promo_product.find(class_='label__price label__price_new').find_all('span'))

            old_price = ".".join(
                t.text for t in promo_product.find(class_='label__price label__price_old').find_all('span'))

            try:
                discount = promo_product.find('div', {'class': 'card-sale__discount'}).text
            except AttributeError:
                discount = '-' + str(round((1 - float(new_price) / float(old_price)) * 100)) + '%'

            promo_info[i] = {
                'Product': title,
                'Discount': discount,
                'OldPrice': old_price,
                'NewPrice': new_price,
                'PromotionTime': promo_time
            }

        file_name = city + '_' + f"{datetime.datetime.now():%Y_%m_%d__%H_%M}" + '.csv'

        await save_to_csv(file_name, promo_info)

        return file_name


if __name__ == '__main__':
    asyncio.run(parse_magnit('Новосибирск'))
