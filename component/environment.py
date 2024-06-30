import os
from dotenv import load_dotenv

load_dotenv()


class Environment:
    openweathermap_token = os.getenv('OPENWEATHERMAP_API_TOKEN')
    gigachad_client_secret = os.getenv('GIGACHAT_CLIENT_SECRET')
    gigachad_authorization = os.getenv('GIGACHAT_AUTHORIZATION')
    yandex_oauth_token = os.getenv('YANDEX_OAUTH_TOKEN')
    yandex_catalog_id = os.getenv('YANDEX_CATALOG_ID')
