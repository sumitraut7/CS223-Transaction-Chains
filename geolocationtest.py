from geopy.geocoders import Nominatim

def get_current_location():
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode("irvine")  # You can specify the city name
    if location:
        return location.latitude, location.longitude
    else:
        raise Exception("Could not determine current location.")

current_lat, current_lon = get_current_location()