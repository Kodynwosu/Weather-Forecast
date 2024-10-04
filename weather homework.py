
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import requests

def fetch_current_weather(city):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={city['latitude']}&longitude={city['longitude']}&current_weather=true"
    response = requests.get(url)
    data = response.json()

    # Check if the request was successful and contains weather data
    if response.status_code == 200 and 'current_weather' in data:
        temperature = data['current_weather']['temperature']  # Get the current temperature
        weather_code = data['current_weather']['weathercode']  # Get the weather code
        return temperature, weather_code  # Return temperature and weather code
    else:
        return None, None  # Return None if data is not available

# Function to get predicted weather data
def fetch_predicted_weather(city):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={city['latitude']}&longitude={city['longitude']}&daily=temperature_2m_max,temperature_2m_min&timezone=America%2FToronto"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and 'daily' in data:
        max_temperatures = data['daily']['temperature_2m_max']
        min_temperatures = data['daily']['temperature_2m_min']
        return max_temperatures, min_temperatures
    else:
        return None, None
def fetch_historical_weather(city):
    # Here we are using mocked data for the last 5 days
    return np.array([8, 9, 11, 10, 12])  # Mocked historical temperatures

def show_current_weather(city_name, city_coords):
    temperature, weather_code = fetch_current_weather(city_coords)

    if temperature is not None:
        weather_icon = get_weather_icon(weather_code)
        current_weather_label.config(text=f"Current Weather in {city_name}: {temperature}°C {weather_icon}")
    else:
        current_weather_label.config(text=f"{city_name}: Weather data not available.")


def get_weather_icon(weather_code):
    if weather_code == 0:
        return "☀️"
    elif weather_code in [1, 2]:
        return "🌤️"
    elif weather_code in [3, 4]:
        return "☁️"
    elif weather_code in [5, 6, 7]:
        return "🌧️"
    elif weather_code in [8, 9]:
        return "❄️"
    else:
        return "🌈"


def plot_predicted_weather(city_name, city_coords):
    max_temps, min_temps = fetch_predicted_weather(city_coords)
    days = np.array(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'])

    if max_temps is not None and min_temps is not None:
        plt.figure(figsize=(10, 5))  # Create a new figure for the plot
        plt.plot(days, max_temps[:5], marker='o', color='blue', label='Max Temp (°C)')  # Plot max temperatures
        plt.plot(days, min_temps[:5], marker='o', color='orange', label='Min Temp (°C)')  # Plot min temperatures
        plt.title(f'Predicted Weather for {city_name}')
        plt.xlabel('Days')
        plt.ylabel('Temperature (°C)')
        plt.grid()
        plt.legend()
        plt.show()
    else:
        print("Predicted weather data not available.")



def plot_historical_weather(city_name, city_coords):
    historical_temperatures = fetch_historical_weather(city_coords)
    days = np.array(['Last Mon', 'Last Tue', 'Last Wed', 'Last Thu', 'Last Fri'])

    plt.figure(figsize=(10, 5))
    plt.plot(days, historical_temperatures, marker='o', color='orange', label='Historical Temp (°C)')
    plt.title(f'Historical Weather for {city_name}')
    plt.xlabel('Days')
    plt.ylabel('Temperature (°C)')
    plt.grid()
    plt.legend()
    plt.show()

cities = {
    "Beamsville": {"latitude": 43.1731, "longitude": -79.4663},
    "Hamilton": {"latitude": 43.2557, "longitude": -79.8711},
    "Toronto": {"latitude": 43.6510, "longitude": -79.3470}
}

root = tk.Tk()
root.title("Weather App")

current_weather_label = tk.Label(root, font=('Times New Romans', 16), justify='left')
current_weather_label.pack(pady=20)

for city_name, city_coords in cities.items():
    weather_button = tk.Button(root, text=f"Get Weather for {city_name}",
                                command=lambda name=city_name, coords=city_coords: show_current_weather(name, coords))
    weather_button.pack(pady=5)

    predicted_button = tk.Button(root, text=f"Show Predicted Weather for {city_name}",
                                  command=lambda name=city_name, coords=city_coords: plot_predicted_weather(name, coords))
    predicted_button.pack(pady=5)

    historical_button = tk.Button(root, text=f"Show Historical Weather for {city_name}",
                                   command=lambda name=city_name, coords=city_coords: plot_historical_weather(name, coords))
    historical_button.pack(pady=5)

root.mainloop()

