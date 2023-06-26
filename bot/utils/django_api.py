import requests
from datetime import datetime


def format_date(date_string):
    if date_string:
        date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        formated_date = date.strftime("%d-%m-%Y")
        return formated_date
    else:
        return '-'


class WebAppAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_all_data(self, endpoint, page_number=None, page_size=None, bought=None, canceled=None):
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
                              f"Цена доставки: {'shipping_price'}\nИмя: {i['client_name']}\n" \
                              f"Телефон: {i['client_phone_number']}, Вид связи: {i['type_of_connect']}\n" \
                              f"Куплен: {'Да' if i['bought'] == True else 'Нет'}, " \
                              f"Дата продажи: {date_of_bought}\n" \
                              f"Отменен: {'Да' if i['canceled'] == True else 'Нет'}, " \
                              f"Дата отмены: {date_of_canceled}\n\n"

                response_text += f"{'=' * 30}\n"
                result_data['response_text'] = response_text
                return result_data
        except requests.exceptions.RequestException as ex:
            print(f"Проблема с получением данных: {ex}")

    def post_data(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                return response.json()
        except requests.exceptions.RequestException as ex:
            print(f"Проблема с внесением данных: {ex}")

    def update_data(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.patch(url, json=data)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as ex:
            print(f"Проблема с изменением данных: {ex}")

    def delete_data(self, endpoint):
        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.delete(url)
            if response.status_code == 204:
                return True
        except requests.exceptions.RequestException as ex:
            print(f"Проблема с удалением данных: {ex}")
