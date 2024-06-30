import concurrent
import json
import math
import os
import sys
from concurrent.futures import ThreadPoolExecutor

from component.geo import GeoLocation
from component.gigachad_gpt import GigaChadGPT
from component.localization import Localization
from component.yandex_gpt import YandexGPT


def k_2_c(kelvin) -> float:
    """Конвертирует указанное значение в Кельвинах в Градусы Цельсия.

        :param kelvin: Значение температуры в Кельвинах.
    """
    return kelvin - 273.15


class App:
    geo = GeoLocation()
    localization: Localization = None

    def choose_language(self):
        """Запрашивает ввод языка локализации от пользователя в консольном приложении.
            Кэширует объект локализации в текущем объекте приложения
        """
        while True:
            lang = input('Choose the language (en/ru):\t')
            try:
                self.localization = Localization(lang)
                break
            except Exception as e:
                print('Exception:', e, file=sys.stderr)

    def enter_city(self):
        """Запрашивает ввод названия города в консольном приложении.

            Возвращает введенное название города.
        """
        while True:
            try:
                city_name = input(self.localization.get('enter_city_name') + ':\t')
            except Exception as e:
                print('Exception:', e, file=sys.stderr)
                continue
            return city_name

    def enter_geo(self, city_name):
        """Предлагает пользователю выбрать город в консольном приложении из списка запрошенных геолокацией.


            :param city_name: Название города

            Возвращает словарь геолокации выбранного города.
        """
        data = self.geo.request_city_data(city_name)
        json_data = json.loads(data.text)
        for i, city_data in enumerate(json_data):
            print('ID:', i + 1)
            print(self.localization.get('city') + ':', city_data['name'])
            print(self.localization.get('country') + ':', city_data['country'])
            print(self.localization.get('state') + ':', city_data['state'])
            print('==========================================')

        if len(json_data) == 0:
            raise Exception(self.localization.get('err_city_not_found'))

        city_id = 0
        while True:
            city_id_str = input(self.localization.get('enter_city_id') + ':\t')
            try:
                city_id = int(city_id_str) - 1

                if city_id >= len(json_data):
                    raise Exception(self.localization.get('err_id_more_city_length'))
            except Exception as e:
                print('Exception:', e, file=sys.stderr)
                continue
            return json_data[city_id]

    def request_tomorrow_weather(self, city_data):
        """Запрашивает информацию о погоде на завтра используя геолокацию города.

            :param city_data: словарь с геолокацией города.

            Возвращает словарь с информацией о погоде на завтра.
        """
        data = self.geo.request_city_weather_data(
            city_data['lat'],
            city_data['lon'],
            self.localization.lang
        )
        return json.loads(data.text)['list'][3]

    def enter_genre(self):
        """Запрашивает пользовательский ввод жанра.

            Возвращает введенный жанр.
        """
        return input(
            self.localization.get('enter_genre') + ':\t'
        )

    def enter_max_symbols(self):
        """Запрашивает пользовательский ввод максимального числа символов для запроса с нейросетей.

            Возвращает максимальное число в токенах.
        """
        while True:
            max_symbols_str = input(
                self.localization.get('enter_max_symbols') + ':\t'
            )
            try:
                max_tokens = math.trunc(int(max_symbols_str) / 4)
            except Exception as e:
                print('Exception:', e, file=sys.stderr)
                continue
            return max_tokens

    def done_completion(self, generation_name, data):
        """Выполняет финишную запись результата работы нейросети

            :param generation_name: название файла используемой нейросети (ex. yandex, gigachat).
            :param data: словарь с информацией о модели, времени запроса, текстовом ответе модели.

            Возвращает текстовый результат для вывода в консоль.
        """
        with open(f'{generation_name}.txt', 'wb') as file:
            file.write(b'Model: ' + data['model'].encode() + b'\n')
            file.write(b'Elapsed time: ' + str(data['time']).encode() + b'\n')
            file.write(b'Text: \n' + data['text'].encode() + b'\n')
        return self.localization.get('result_written_into_file') + f' {generation_name}.txt'

    def request_completions(self, max_tokens, genre, city_data, weather_data):
        """Запрашивает информацию о погоде на завтра используя геолокацию города.

            :param max_tokens: максимальное число токенов в запросе.
            :param genre: жанр для получения соответствующего текста ответа от нейросети.
            :param city_data: словарь с геолокацией города.
            :param weather_data: словарь с информацией о погоде.

        """
        ya_gpt = YandexGPT()
        giga_gpt = GigaChadGPT()

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [
                executor.submit(
                    ya_gpt.completion,
                    max_tokens,
                    genre,
                    city_data['name'],
                    weather_data['weather'][0]['description'],
                    math.trunc(k_2_c(weather_data['main']['temp']))
                ),

                executor.submit(
                    giga_gpt.completion,
                    max_tokens,
                    genre,
                    city_data['name'],
                    weather_data['weather'][0]['description'],
                    math.trunc(k_2_c(weather_data['main']['temp']))
                )
            ]
            for future in concurrent.futures.as_completed(futures):
                gpt = future.result()
                result = self.done_completion(gpt.name,
                                              gpt.result)
                print(result)

    def run(self):
        """Основной цикл консольного приложения.
        """
        self.choose_language()
        while True:
            city_name = self.enter_city()
            try:
                city_data = self.enter_geo(city_name)
                weather_data = self.request_tomorrow_weather(city_data)
                genre = self.enter_genre()
                max_tokens = self.enter_max_symbols()
                self.request_completions(
                    max_tokens,
                    genre,
                    city_data,
                    weather_data
                )
            except Exception as e:
                print('Exception:', e, file=sys.stderr)
                continue
            os.system('pause')
