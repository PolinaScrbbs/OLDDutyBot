import asyncio
import aiohttp  
from urllib.parse import urljoin
from datetime import datetime
from config import API_URL as base_url
        
async def registration(data):
    url = urljoin(base_url, "signup/")
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.json()

            
async def authorization(data):
    url = urljoin(base_url, "login/")
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.json()

            
async def get_group_students(token):
    url = urljoin(base_url, "users/")
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                return await response.json()

        except aiohttp.ClientError as e:
            return {"error": str(e)}
        
async def get_group_duties(token):
    url = urljoin(base_url, "duties/")
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                return await response.json()

        except aiohttp.ClientError as e:
            return {"error": str(e)}
        
async def get_group_duties_count(token):
    url = urljoin(base_url, "duties_count/")
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                return await response.json()

        except aiohttp.ClientError as e:
            return {"error": str(e)}

# def get_duties(token):
#     base_url = API_URL
#     endpoint = '/api/duties/'
#     url = urljoin(base_url, endpoint)
#     headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}

#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Проверка на ошибку в ответе
        
#         if response.status_code == 200:
#             duties = response.json()
#             return duties, None
#         else:
#             return None, "Ошибка"
#     except requests.RequestException as e:
#         print(f"Произошла ошибка: {e}")


# def get_attendants(token, pass_people):
#     base_url = API_URL
#     endpoint = '/api/attendant/'
#     url = urljoin(base_url, endpoint)
#     headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}
#     data = {'pass_people': pass_people}

#     try:
#         response = requests.get(url, json=data, headers=headers)
#         response.raise_for_status()  # Проверка на ошибку в ответе
        
#         if response.status_code == 200:
#             attendants = response.json()
#             return attendants, None
#         else:
#             return None, "Ошибка"
#     except requests.RequestException as e:
#         print(f"Произошла ошибка: {e}")


# def post_duties(token, attendants):
#     base_url = API_URL
#     endpoint = '/api/duties/'
#     url = urljoin(base_url, endpoint)
#     headers = {'Authorization': f'Token {token}', 'Content-Type': 'application/json'}
#     today = str(datetime.today().date())
#     body = {
#         'duties': [
#             {
#                 "people": attendants[0]['full_name'],
#                 "date": today
#             },
#             {
#                 "people": attendants[1]['full_name'],
#                 "date": today
#             }
#         ]
#     }

#     try:
#         response = requests.post(url, json=body, headers=headers)
#         response.raise_for_status()  # Проверка на ошибку в ответе
        
#         if response.status_code == 200:
#             attendants = response.json()
#             return attendants, None
#         else:
#             return None, "Ошибка"
#     except requests.RequestException as e:
#         print(f"Произошла ошибка: {e}") 
   