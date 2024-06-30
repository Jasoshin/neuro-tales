class GPT:
    name = 'gpt'
    model = ''
    result = {
        'time': None,
        'model': '',
        'text': ''
    }

    def update_token(self):
        """Виртуальная функция обновления временного токена.
        """
        pass

    def completion(self, max_tokens, genre, city_name, weather, degree):
        """Виртуальная функция запроса текста от нейросети.
        """
        pass
