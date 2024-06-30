import datetime
import json

import requests

from component.environment import Environment
from component.generation import Generation
from component.gpt import GPT


class YandexGPT(GPT):
    name = 'yandex'
    model = 'yandexgpt-lite'
    oauth_token = Environment.yandex_oauth_token
    catalog_id = Environment.yandex_catalog_id
    token: str = None

    def update_token(self):
        data = {
            'yandexPassportOauthToken': self.oauth_token,
        }
        response = requests.post(
            url='https://iam.api.cloud.yandex.net/iam/v1/tokens',
            data=json.dumps(data)
        )
        self.token = json.loads(response.text)['iamToken']

    def completion(self, max_tokens, genre, city_name, weather, degree):
        start_time = datetime.datetime.now()

        self.update_token()

        headers = {
            'Authorization': f'Bearer {self.token}',
            'x-folder-id': self.catalog_id
        }
        data = {
            "modelUri": f"gpt://{self.catalog_id}/{self.model}",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": f"{max_tokens}"
            },
            "messages": [
                {
                    "role": "system",
                    "text": Generation.prompt
                },
                {
                    "role": "user",
                    "text": Generation.message.format(
                        genre=genre,
                        city=city_name,
                        weather=weather,
                        degree=degree)
                }
            ]
        }
        request_data = json.dumps(data)
        response = requests.post(
            url='https://llm.api.cloud.yandex.net/foundationModels/v1/completion',
            headers=headers,
            data=request_data
        )

        end_time = datetime.datetime.now()

        self.result['text'] = json.loads(response.text)['result']['alternatives'][0]['message']['text']
        self.result['time'] = end_time-start_time
        self.result['model'] = self.model
        return self
