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
        
async def get_group_attendants(token, pass_people):
    url = urljoin(base_url, "attendants/")
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {'pass_attendant': pass_people}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, json=payload) as response:
                return await response.json()
        except aiohttp.ClientError as e:
            return {"error": str(e)}
        
async def add_attendant_duties(token, attendants):
    url = urljoin(base_url, "duties/")
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {'attendants': attendants}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=payload) as response:
                return await response.json()
        except aiohttp.ClientError as e:
            return {"error": str(e)}
   