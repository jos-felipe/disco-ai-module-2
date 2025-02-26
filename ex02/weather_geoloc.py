# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    weather_ge                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: josfelip <josfelip@student.42sp.org.br>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/02/26 11:30:11 by josfelip          #+#    #+#              #
#    Updated: 2025/02/26 11:30:14 by josfelip         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/env python3
# weather_geoloc.py

"""
Weather Information Program with Geolocation

This script accepts a location name (like "Paris" or "New York") and displays
the current weather information for that location using WeatherAPI.com.

Usage:
    ./weather_geoloc.py
    
Requirements:
    - requests library (install with pip install requests)
    - Python virtual environment with necessary packages
    - API key from WeatherAPI.com stored in .env file
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather_by_location(location_name):
    """
    Get current weather data for the given location name.
    
    The WeatherAPI.com service handles geolocation automatically when we pass
    a location name instead of coordinates. This simplifies our code as we don't
    need a separate geolocation service.
    
    Args:
        location_name (str): The name of the location (city, address, etc.)
        
    Returns:
        dict: Weather data if successful, None otherwise
    """
    if not API_KEY:
        print("Error: No API key found. Please create a .env file with your WEATHER_API_KEY.")
        return None
    
    try:
        # Construct the API request
        url = "https://api.weatherapi.com/v1/current.json"
        params = {
            "key": API_KEY,
            "q": location_name,
            "aqi": "no"
        }
        
        # Send the request
        response = requests.get(url, params=params, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            # This typically means the location wasn't found
            print(f"Error: Could not find location '{location_name}'")
            return None
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to connect to the weather API: {e}")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return None

def display_weather(weather_data):
    """
    Display weather information in a formatted way.
    
    Args:
        weather_data (dict): The weather data from the API
    """
    if not weather_data or 'current' not in weather_data:
        print("No weather data available to display.")
        return
    
    current = weather_data['current']
    location = weather_data['location']
    
    # Format the location name properly
    location_name = location['name']
    if location.get('region') and location['region'] != location['name']:
        location_name += f", {location['region']}"
    
    print(f"\nThe current weather in {location_name} is:")
    print(f"- temperature(C): {current['temp_c']}")
    print(f"- humidity: {current['humidity']}%")
    print(f"- cloud: {current['cloud']}%")
    print(f"- wind: {current['wind_kph']}km/h")
    
    # Additional information (optional)
    print(f"- condition: {current['condition']['text']}")
    print(f"- feels like: {current['feelslike_c']}°C")
    print(f"- UV index: {current['uv']}")
    
    # Extra location information
    print(f"\nCoordinates: {location['lat']}, {location['lon']}")
    print(f"Country: {location['country']}")
    print(f"Local time: {location['localtime']}")

def main():
    """Main function to run the weather information program with geolocation."""
    print("Weather Information Program with Geolocation")
    print("===========================================")
    
    try:
        # Get location name
        location = input("Location?: ")
        
        # Validate input
        if not location.strip():
            print("Error: Location cannot be empty.")
            sys.exit(1)
        
        # Get and display weather data
        weather_data = get_weather_by_location(location)
        if weather_data:
            display_weather(weather_data)
        else:
            print("Failed to retrieve weather information. Please try a different location or try again later.")
            
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()