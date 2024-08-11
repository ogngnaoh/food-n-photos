import requests
from dotenv import load_dotenv
import os

load_dotenv()
unsplash = os.environ.get('UNSPLASH_API_KEY')


def location_photos(location, unsplash):
    url = 'https://api.unsplash.com/search/photos'

    params = {
        'query': location,
        'per_page': 1,
        'client_id': unsplash
    }

    response = requests.get(url, params)
    data = response.json()

    if 'errors' not in data:
        return data['results'][0]['urls']['small']
    else:
        raise TypeError
