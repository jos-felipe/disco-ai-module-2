#!/usr/bin/env python3
# weather.py

"""
Weather Information Program

This script asks for latitude and longitude coordinates and displays
the current weather information for that location using WeatherAPI.com.

Usage:
    ./weather.py
    
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

def validate_coordinates(value, coord_type):
    """
    Validate latitude or longitude input.
    
    Args:
        value (str): The input value to validate
        coord_type (str): Either 'latitude' or 'longitude'
        
    Returns:
        float: The validated coordinate value
        
    Raises:
        ValueError: If the input is not a valid coordinate
    """
    try:
        coordinate = float(value)
        
        # Check range
        if coord_type == 'latitude' and (coordinate < -90 or coordinate > 90):
            raise ValueError("Latitude must be between -90 and 90 degrees")
        elif coord_type == 'longitude' and (coordinate < -180 or coordinate > 180):
            raise ValueError("Longitude must be between -180 and 180 degrees")
            
        return coordinate
    except ValueError:
        raise ValueError(f"Invalid {coord_type} format. Please enter a number.")

def get_weather(latitude, longitude):
    """
    Get current weather data for the given coordinates.
    
    Args:
        latitude (float): The latitude coordinate
        longitude (float): The longitude coordinate
        
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
            "q": f"{latitude},{longitude}",
            "aqi": "no"
        }
        
        # Send the request
        response = requests.get(url, params=params, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
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
    
    print(f"\nThe current weather for this location is:")
    print(f"- temperature(C): {current['temp_c']}")
    print(f"- humidity: {current['humidity']}%")
    print(f"- cloud: {current['cloud']}%")
    print(f"- wind: {current['wind_kph']}km/h")
    
    # Additional information (optional)
    print(f"- condition: {current['condition']['text']}")
    print(f"- feels like: {current['feelslike_c']}°C")
    print(f"- UV index: {current['uv']}")
    
    # Location information
    print(f"\nLocation: {location['name']}, {location['region']}, {location['country']}")
    print(f"Local time: {location['localtime']}")

def main():
    """Main function to run the weather information program."""
    print("Weather Information Program")
    print("==========================")
    
    # Ask for latitude and longitude
    try:
        # Get latitude with validation
        while True:
            try:
                lat_input = input("Latitude?: ")
                latitude = validate_coordinates(lat_input, 'latitude')
                break
            except ValueError as e:
                print(f"Error: {e}")
        
        # Get longitude with validation
        while True:
            try:
                lon_input = input("Longitude?: ")
                longitude = validate_coordinates(lon_input, 'longitude')
                break
            except ValueError as e:
                print(f"Error: {e}")
        
        # Get and display weather data
        weather_data = get_weather(latitude, longitude)
        if weather_data:
            display_weather(weather_data)
        else:
            print("Failed to retrieve weather information. Please try again later.")
            
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()