import requests
from urllib.parse import urljoin

from config import API_URL

def authorization(login, password):
    base_url = API_URL
    endpoint = '/auth/login/'
    url = urljoin(base_url, endpoint)
    headers = {'Content-Type': 'application/json'}
    data = {'login': login, 'password': password}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Проверка на ошибку в ответе

        if response.status_code == 200:
            token = response.json().get('token')
            return token, None
        else:
            return None, "Ошибка аутентификации"
    except requests.exceptions.RequestException as e:
        print(f"У пользователя {login} Произошла ошибка: {e}")