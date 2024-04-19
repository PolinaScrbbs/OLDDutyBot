import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError

def get_group_list():
    url = "https://schedule.kg-college.ru/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        options = soup.find_all('option', value=True)
        group_names = [option['value'].lower() for option in options if len(option['value']) < 8]
        return group_names
    except requests.RequestException as e:
        raise ValidationError(f'Ошибка при получении данных: {e}')