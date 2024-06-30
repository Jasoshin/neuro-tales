class Localization:
    langs = [
        'en',
        'ru'
    ]

    lang = 'en'

    data = {
        'enter_city_name': {
            'en': 'Enter the name of the city',
            'ru': 'Введите название города'
        },
        'enter_genre': {
            'en': 'Enter the genre of the fairy tail',
            'ru': 'Введите жанр сказки'
        },
        'enter_max_symbols': {
            'en': 'Enter the max symbols of the completion',
            'ru': 'Введите максимальное число символов'
        },
        'enter_city_id': {
            'en': 'Enter the id of the city',
            'ru': 'Выберите id города'
        },
        'err_id_more_city_length': {
            'en': 'ID more then length of the cities',
            'ru': 'ID превышает число городов'
        },
        'err_city_not_found': {
            'en': 'City is not found',
            'ru': 'Город не найден'
        },
        'result_written_into_file': {
            'en': 'Result written into',
            'ru': 'Результат записан в файл'
        },
        'city': {
            'en': 'City',
            'ru': 'Город'
        },
        'country': {
            'en': 'Country',
            'ru': 'Страна'
        },
        'state': {
            'en': 'State',
            'ru': 'Штат/Область'
        }
    }

    def __init__(self, lang):
        """Создает объект Локализации.

            :param lang: двузначный код языка (en, ru).

        """
        self.lang = lang
        self.is_valid_lang()

    def is_valid_lang(self):
        """Проверяет корректность установленного языка.
        """
        if self.lang not in Localization.langs:
            raise Exception('Language incorrect')
        return True

    def get(self, record):
        """Получает текущую запись с нужной локализацией.

        :param record: Запись для извлечения.

        Возвращает запись с установленной локализацией.
        """
        self.is_valid_lang()
        return self.data[record][self.lang]
