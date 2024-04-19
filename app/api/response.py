import httpx
from urllib.parse import urljoin
from config import API_URL

async def authorization(login, password):
    base_url = API_URL
    endpoint = '/auth/login/'
    url = urljoin(base_url, endpoint)
    headers = {'Content-Type': 'application/json'}
    data = {'login': login, 'password': password}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()  # Проверка на ошибку в ответе

            if response.status_code == 200:
                token = response.json().get('token')
                return token, None
            else:
                return None, "Ошибка аутентификации"
        except httpx.RequestError as e:
            print(f"У пользователя {login} Произошла ошибка: {e}")

async def get_duties_count(token):
    base_url = API_URL
    endpoint = '/api/people/'
    url = urljoin(base_url, f"{endpoint}?token={token}")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # Проверка на ошибку в ответе
        
            if response.status_code == 200:
                duties_count = response.json()
                return duties_count, None
            else:
                return None, "Ошибка"
        except httpx.RequestError as e:
            print(f"Произошла ошибка: {e}")
