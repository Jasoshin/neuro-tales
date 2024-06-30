import requests

from component.environment import Environment


class GeoLocation:
    geo_url = 'https://api.openweathermap.org'
    api_token = Environment.openweathermap_token

    def set_url(self, geo_url):
        self.geo_url = geo_url

    def set_token(self, api_token):
        self.api_token = api_token

    def request_city_data(self, city_name):
        """Запрашивает геолокационные данные по названию города.

            :param city_name: Название города.

        Возвращает данные геолокации города.
        """
        data = requests.get(f'{self.geo_url}/geo/1.0/direct?q={city_name}&appid={self.api_token}')
        return data

    def request_city_weather_data(self, lat, lon, lang):
        """Запрашивает данные о погоде по геолокации.

            :param lat: Широта.
            :param lon: Долгота.
            :param lang: Язык результата запроса.

        Возвращает данные о погоде.
        """
        data = requests.get(
            f'{self.geo_url}/data/2.5/forecast?lat={lat}&lon={lon}&lang={lang}&appid={self.api_token}'
        )
        return data
