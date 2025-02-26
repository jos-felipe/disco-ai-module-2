# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_weather_api.py                                :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: josfelip <josfelip@student.42sp.org.br>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/02/26 10:31:42 by josfelip          #+#    #+#              #
#    Updated: 2025/02/26 16:26:27 by josfelip         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/env python3
# test_weather_api.py

"""
Test script to verify that the virtual environment and WeatherAPI access are working correctly.
This script attempts to retrieve basic weather data from the WeatherAPI.com service
for a default location (Sao Paulo, Brazil).

Note: You'll need to sign up for a free API key at weatherapi.com
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_api_connection():
    """Test connection to the WeatherAPI and verify library installation."""
    
    # Try to get API key from environment variables
    api_key = os.getenv("WEATHER_API_KEY")
    
    # If not found, prompt the user
    if not api_key:
        print("No API key found in environment variables.")
        api_key = input("Please enter your WeatherAPI.com API key: ")
        
        # Save it to a .env file for future use
        with open(".env", "w") as env_file:
            env_file.write(f"WEATHER_API_KEY={api_key}")
        print("API key saved to .env file for future use.")
    
    try:
        # Simple test - get current weather for Sao Paulo
        url = "https://api.weatherapi.com/v1/current.json"
        params = {
            "key": api_key,
            "q": "Sao Paulo",
            "aqi": "no"
        }
        
        print("Sending request to WeatherAPI.com...")
        response = requests.get(url, params=params)
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            print("\nAPI connection successful! Response received.")
            
            # Extract and display the weather data
            if 'current' in data:
                current = data['current']
                location = data['location']
                
                print(f"\nCurrent weather data for {location['name']}, {location['country']}:")
                print(f"Temperature: {current['temp_c']}°C")
                print(f"Humidity: {current['humidity']}%")
                print(f"Cloud Cover: {current['cloud']}%")
                print(f"Wind Speed: {current['wind_kph']} km/h")
                print(f"Condition: {current['condition']['text']}")
                
                return True
            else:
                print("Response received, but no current weather data found.")
                print("Full response:", data)
                return False
        else:
            print(f"API request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            
            # Common error cases
            if response.status_code == 401:
                print("\nError 401: Unauthorized. Your API key might be invalid or expired.")
                print("Please get a new API key from weatherapi.com")
            elif response.status_code == 403:
                print("\nError 403: Forbidden. You might have exceeded your API call limits.")
            
            return False
            
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

if __name__ == "__main__":
    print("Testing WeatherAPI.com connection...\n")
    
    # Check if running in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("Virtual environment detected!")
    else:
        print("Warning: Not running in a virtual environment. It's recommended to run this script in a virtual environment.")
    
    # Test the API connection
    success = test_api_connection()
    
    if success:
        print("\nEnvironment setup is correct and API connection is working!")
        print("You're all set to proceed with the weather application.")
    else:
        print("\nFailed to connect to the API. Please check your setup, API key, and internet connection.")