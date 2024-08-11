import googlemaps
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('GOOGLE_API_KEY')
gmaps = googlemaps.Client(key=api_key)
min_rating = 4.5
min_review = 500
radius = 2000


# obtain coordinates of location given
def search_coordinates(client, location_text):
    place_result = client.places(query=location_text)

    if place_result['status'] == 'OK':
        location = place_result['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        return lat, lng

    return None


# obtain the list of restaurants given
def search_nearby_restaurants(client, min_rating, min_review, lat, lng, radius):
    restaurant_results = client.places_nearby(
        location=(lat, lng),
        type='restaurant',
        radius=radius
    )

    if restaurant_results['status'] == 'OK':
        filtered_results = [
            place for place in restaurant_results['results']
            if place.get('rating', 0) >= min_rating and place.get('user_ratings_total') >= min_review
        ]

        return filtered_results

    return []


# find the photogenic spots that are near a specified location

def search_photogenic_spots(client, lat, lng):

    photogenic_spots = client.places_nearby(
        location=(lat, lng),
        type='tourist_attraction',
        radius=5000
    )

    if photogenic_spots['status'] == 'OK':
        filtered_results = [
            place.get('name') for place in photogenic_spots['results']
        ]

        if len(filtered_results) > 5:
            filtered_results = filtered_results[0:5]

        return filtered_results

    return []



