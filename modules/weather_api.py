import requests

GEOCODING_URL = 'http://api.openweathermap.org/geo/1.0/direct'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'

class Weather:
    """
    Class for handling the OpenWeatherMap API.
    Converts city names to coordinates (latitude and longitude), 
    then fetches weather data based on those coordinates.
    """

    def __init__(self, api_key:str):
        self.city_name = ""
        self.api_key = api_key
        self.longitude = None
        self.latitude = None


    def get_coordinates(self, user_city:str):
        """Fetches city coordinates and stores them as object attributes."""
        if not user_city:
            print("[ERROR]: You did not enter anything.\n")
            return False
        elif not user_city.replace(" ", "").isalpha():
            print("[ERROR]: You may only enter letters.\n")
            return False
        self.city_name = user_city
        geocoding = f"{GEOCODING_URL}?q={user_city}&appid={self.api_key}"

        try:
            # timeout=5 to prevent the program from freezing if the server is slow
            response = requests.get(url=geocoding, timeout=5)
            if response.status_code == 200:
                # [NOTE]: API request returns a list of json data
                # It will be converted into list of dictionaries
                result = response.json()
                # get() is a 'dict method', it cannot be applied
                # on a list, the first element of this list is a dictionary

                # [NOTE]: Why the first element?
                # Because the first result is typically the best match
                # Example: France has city 'Paris'
                #          USA Texas also has a small city 'Paris'
                # So algorithmically, the first element must be the most
                # relevant and common.
                self.longitude = result[0].get('lon')
                self.latitude = result[0].get('lat')
                return True
            else:
                print(f"[ERROR]: Server responded with status code: {response.status_code}.")
                return False
        except requests.exceptions.ConnectionError:
            print("[ERROR]: You are currently offline, connect to a Wi-Fi network.")
            return False
        except requests.exceptions.ConnectTimeout:
            print("[ERROR]: Server took too much to respond [Timeout > 5].")
            return False
        # If the user attempts to enter a non-existing city, the server will respond
        # with an empty list [], accessing the index 0 of an empty list will certainly
        # result in IndexError.
        except IndexError:
            print(f"[ERROR]: The city of {user_city} does not exist.\n")
            return False
        

    def get_weather(self):
        """Fetches the temperature and weather status, returning them as a list."""
        weather_url = f"{WEATHER_URL}?lat={self.latitude}&lon={self.longitude}&appid={self.api_key}&units=metric"

        try:
            response = requests.get(url=weather_url, timeout=5)
            if response.status_code == 200:
                weather_info = response.json()

                # Accurately extracting data from the nested JSON dictionary
                temperature = weather_info.get("main").get("temp")
                weather_description = weather_info.get("weather")[0].get("description")

                return [float(round(temperature)), str(weather_description).title()]
            
            else:
                print(f"[ERROR]: Server responded with status code: {response.status_code}.\n")
                return
            
        except requests.exceptions.ConnectionError:
            print("[ERROR]: You are currently offline, connect to a Wi-Fi network.")
            return 
        
        except requests.exceptions.ConnectTimeout:
            print("[ERROR]: Server took too much to respond [Timeout > 5].")
            return 