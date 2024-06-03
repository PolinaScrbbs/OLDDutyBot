from bs4 import BeautifulSoup
from django.forms import ValidationError
import requests
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def get_group_list():
    cache_key = "group_list"
    
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return cached_data.decode('utf-8').split(',')
    
    url = "https://schedule.kg-college.ru/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        options = soup.find_all('option', value=True)
        group_names = [option['value'].upper() for option in options if len(option['value']) < 8]
        
        redis_client.set(cache_key, ','.join(group_names), ex=3600)
        
        return group_names
    except requests.RequestException as e:
        raise ValidationError(f'Ошибка при получении данных: {e}')

