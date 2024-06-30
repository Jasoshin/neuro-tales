import datetime
import json
import random

import requests

from component.environment import Environment
from component.generation import Generation
from component.gpt import GPT


class GigaChadGPT(GPT):
    name = 'gigachat'
    model = 'GigaChat'
    client_secret = Environment.gigachad_client_secret
    authorization = Environment.gigachad_authorization
    token: str = None

    def update_token(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': f'{self.client_secret}',
            'Authorization': f'Basic {self.authorization}'
        }
        data = 'scope=GIGACHAT_API_PERS'
        response = requests.post(
            url='https://ngw.devices.sberbank.ru:9443/api/v2/oauth',
            headers=headers,
            data=data,
            verify=False
        )
        self.token = json.loads(response.text)['access_token']

    def completion(self, max_tokens, genre, city_name, weather, degree):
        start_time = datetime.datetime.now()

        self.update_token()

        headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            "model": self.model,
            "temperature": 0.6,
            "top_p": 0.1,
            "n": 1,
            "stream": False,
            "max_tokens": max_tokens,
            "repetition_penalty": 1,
            "messages": [
                {
                  "role": "system",
                  "content": Generation.prompt
                },
                {
                  "role": "user",
                  "content": Generation.message.format(
                      genre=genre,
                      city=city_name,
                      weather=weather,
                      degree=degree)
                }
            ],
        }
        request_data = json.dumps(data)
        response = requests.post(
            url='https://gigachat.devices.sberbank.ru/api/v1/chat/completions',
            headers=headers,
            data=request_data,
            verify=False
        )

        end_time = datetime.datetime.now()

        self.result['text'] = json.loads(response.text)['choices'][0]['message']['content']
        self.result['time'] = end_time-start_time
        self.result['model'] = self.model
        return self
