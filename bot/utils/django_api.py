import csv

import requests
from datetime import datetime
from typing import Optional, Any


def format_date(date_string: str) -> str:
    if date_string:
        date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        formated_date = date.strftime("%d-%m-%Y")
        return formated_date
    else:
        return '-'


class WebAppAPI:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def get_all_data(self, endpoint: str, page_number: Optional[int] = None, page_size: Optional[int] = None,
                     bought: Optional[bool] = None, canceled: Optional[bool] = None, product: Optional[str] = None):
        url = f"{self.base_url}/{endpoint}"

        params = {}
        if page_number:
            params['page'] = page_number
        if page_size:
            params['page_size'] = page_size

        if bought is not None:
            params['bought'] = bought
            if bought:
                info_text = ' выкупленных '

        if canceled is not None:
            params['canceled'] = canceled
            if canceled:
                info_text = ' отменённых '

        if not canceled and not bought:
            info_text = ' действующих '

        if canceled is None and bought is None:
            info_text = ' '

        if product is not None:
            params['product'] = product
            info_text = f' для товара {product} '

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                result_data = dict()
                response = response.json()

                count = response.get('count', 0)
                result_data['count'] = count
                results = response.get('results', [])
                pages = response.get('pages', 0)
                result_data['pages'] = pages

                response_text = f'Всего{info_text}предзаказов: {count}\n\n'
                for i in results:
                    date_ordered = format_date(i['date_ordered'])
                    date_of_bought = format_date(i['day_of_bought'])
                    date_of_canceled = format_date(i['day_of_canceled'])

                    response_text += f"ID: {i['id']} ,Номер заказа Tilda: {i['number']}\nДата заказа: {date_ordered}\n" \
                              f"Товар: {i['product']} {i['color']} {i['size']} - {i['quantity']} шт. - {i['price']} р.\n" \
                              f"Адрес доставки: {i['city']}, {i['shipping_adress']}\n" \
                              f"Цена доставки: {i['shipping_price']}\nИмя: {i['client_name']}\n" \
                              f"Телефон: {i['client_phone_number']}, Вид связи: {i['type_of_connect']}\n" \
                              f"Куплен: {'Да' if i['bought'] == True else 'Нет'}, " \
                              f"Дата продажи: {date_of_bought}\n" \
                              f"Отменен: {'Да' if i['canceled'] == True else 'Нет'}, " \
                              f"Дата отмены: {date_of_canceled}\n\n"

                response_text += f"{'=' * 30}\n"
                result_data['response_text'] = response_text
                return result_data

            else:
                error_message = response.json().get("detail", "Unknown error")
                result_data = {
                    "count": 0,
                    "pages": 0,
                    "response_text": f"Ошибка при получении данных: {error_message}"
                }
                return result_data

        except requests.exceptions.RequestException as ex:
            print(f"Проблема с получением данных: {ex}")

    def export_csv(self, endpoint: str) -> Optional[str]:
        url = f"{self.base_url}/{endpoint}"
        headers = ['№ п/п', 'Номер заказ', 'Продукт', 'Цвет', 'Размер', 'Количество', 'Цена', 'Город', 'Адрес доставки',
                       'Цена доставки', 'Имя клиента', 'Номер телефона', 'Тип связи', 'Дата заказа', 'Предзаказ Выкуплен',
                       'Дата выкупа', 'Предзаказ отменен', 'Дата отмены']
        try:
            response = requests.get(url=url)
            if response.status_code == 200:
                data = response.json()
                filename = f'preorders_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'

                with open(filename, 'w', encoding='utf-8') as output:
                    writer = csv.writer(output, delimiter=';')
                    writer.writerow(headers)

                    for item in data.get('results'):
                        row = [item['id'], item['number'], item['product'], item['color'], item['size'],
                               item['quantity'], item['price'], item['city'], item['shipping_adress'],
                               item['shipping_price'], item['client_name'], item['client_phone_number'],
                               item['type_of_connect'], item['date_ordered'], item['bought'],
                               item['day_of_bought'], item['canceled'], item['day_of_canceled']]
                        writer.writerow(row)

                return filename

        except requests.exceptions.RequestException as ex:
            print(f"Проблема с получением данных: {ex}")

    def post_data(self, endpoint: str, data: Any) -> Optional[dict]:
        url = f"{self.base_url}/{endpoint}/"

        number = data.get('number')
        product = data.get('product')
        color = data.get('color')
        size = data.get('size')
        quantity = data.get('quantity')
        price = data.get('price')
        city = data.get('city')
        shipping_adress = data.get('shipping_adress')
        shipping_price = data.get('shipping_price')
        client_name = data.get('client_name')
        client_phone_number = data.get('client_phone_number')
        type_of_connect = data.get('type_of_connect')

        result_data = {
            'number': number,
            'product': product,
            'color': color,
            'size': size,
            'quantity': quantity,
            'price': price,
            'city': city,
            'shipping_adress': shipping_adress,
            'shipping_price': shipping_price,
            'client_name': client_name,
            'client_phone_number': client_phone_number,
            'type_of_connect': type_of_connect,
            "bought": False,
            "day_of_bought": None,
            "canceled": False,
            "day_of_canceled": None,
        }

        try:
            response = requests.post(url, json=result_data)
            if response.status_code == 201:
                return response.json()
        except requests.exceptions.RequestException as ex:
            print(f"Проблема с внесением данных: {ex}")
            return f'{result_data}\n{ex}'

    def update_data(self, endpoint: str, data: Any) -> Optional[dict]:
        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.patch(url, json=data)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as ex:
            print(f"Проблема с изменением данных: {ex}")

    def delete_data(self, endpoint: str) -> Optional[bool]:
        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.delete(url)
            if response.status_code == 204:
                return True
        except requests.exceptions.RequestException as ex:
            print(f"Проблема с удалением данных: {ex}")
