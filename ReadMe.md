<h1>Консольное приложение для запроса погоды на завтра от нейросетей Yandex и GigaChat.</h1>

<h2>Подготовка</h2>

<p>Создайте файл .env</p>
<p>Заполните переменные окружения для доступа к услугам нейросетей и сервису геолокации:</p>

```commandline
OPENWEATHERMAP_API_TOKEN=<ваш api токен api.openweathermap.org>
GIGACHAT_CLIENT_SECRET=<ваш client_secret GigaChat>
GIGACHAT_AUTHORIZATION=<ваш authorization_key GigaChat>
YANDEX_OAUTH_TOKEN=<ваш OAUTH токен Yandex>
YANDEX_CATALOG_ID=<ваш catalog_id Yandex>
```

<p>Установите необходимые библиотеки для запуска:</p>

```commandline
pip install -r requirements.txt
```
<h2>Запуск</h2>
<p>Для запуска приложения используйте:</p>

```commandline
python main.py
```