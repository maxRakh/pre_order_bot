import unittest
from unittest.mock import patch
from datetime import datetime

from bot.utils.django_api import format_date, WebAppAPI


class WebAppAPITest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.api = WebAppAPI("http://example.com/")

    def test_format_date(self):
        date_string = "2023-06-28T12:00:00.000Z"
        expected_result = '28-06-2023'
        result = format_date(date_string)
        self.assertEqual(result, expected_result)

    @patch("bot.utils.django_api.requests.get")
    def test_get_all_data_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "count": 2,
            "results": [
                {
                    "id": 1,
                    "number": 1,
                    "product": "Телогрейка",
                    "color": "Молочная",
                    "size": "S-M",
                    "quantity": 1,
                    "price": 8000,
                    "city": "Жданово",
                    "shipping_adress": "Опушка 1-1",
                    "shipping_price": 300,
                    "client_name": "Сенокос Петрович",
                    "client_phone_number": "+79227770000",
                    "type_of_connect": "WhatsApp",
                    "date_ordered": "2023-06-28T12:00:00.000Z",
                    "bought": False,
                    "day_of_bought": None,
                    "canceled": False,
                    "day_of_canceled": None
                },
                {
                    "id": 2,
                    "number": 2,
                    "product": "Жилетка",
                    "color": "Голубика",
                    "size": "S-M",
                    "quantity": 1,
                    "price": 11000,
                    "city": "Жданово",
                    "shipping_adress": "Опушка 2-1",
                    "shipping_price": 400,
                    "client_name": "Сенокос Петрович",
                    "client_phone_number": "+79227770000",
                    "type_of_connect": "SMS",
                    "date_ordered": "2023-06-28T12:00:00.000Z",
                    "bought": True,
                    "day_of_bought": "2023-06-28T12:00:00.000Z",
                    "canceled": False,
                    "day_of_canceled": None
                }
            ]
        }

        result = self.api.get_all_data("preorders")
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["pages"], 0)

        expected_response_text = "Всего предзаказов: 2\n\n"
        expected_response_text += f"ID: 1 ,Номер заказа Tilda: 1\nДата заказа: 28-06-2023\n" \
                              f"Товар: Телогрейка Молочная S-M - 1 шт. - 8000 р.\n" \
                              f"Адрес доставки: Жданово, Опушка 1-1\n" \
                              f"Цена доставки: 300\nИмя: Сенокос Петрович\n" \
                              f"Телефон: +79227770000, Вид связи: WhatsApp\n" \
                              f"Куплен: Нет, " \
                              f"Дата продажи: -\n" \
                              f"Отменен: Нет, " \
                              f"Дата отмены: -\n\n"

        expected_response_text += f"ID: 2 ,Номер заказа Tilda: 2\nДата заказа: 28-06-2023\n" \
                                  f"Товар: Жилетка Голубика S-M - 1 шт. - 11000 р.\n" \
                                  f"Адрес доставки: Жданово, Опушка 2-1\n" \
                                  f"Цена доставки: 400\nИмя: Сенокос Петрович\n" \
                                  f"Телефон: +79227770000, Вид связи: SMS\n" \
                                  f"Куплен: Да, " \
                                  f"Дата продажи: 28-06-2023\n" \
                                  f"Отменен: Нет, " \
                                  f"Дата отмены: -\n\n"

        expected_response_text += f"{'=' * 30}\n"

        self.assertEqual(result["response_text"], expected_response_text)

    @patch("bot.utils.django_api.requests.get")
    def test_get_all_data_error(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        mock_response.json.return_value = {"detail": "Not found"}

        result = self.api.get_all_data("endpoint")
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["pages"], 0)
        self.assertEqual(result["response_text"], "Ошибка при получении данных: Not found")


if __name__ == '__main__':
    unittest.main()

