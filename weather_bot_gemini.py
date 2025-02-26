# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    weather_bot_gemini.py                              :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: josfelip <josfelip@student.42sp.org.br>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/02/26 11:38:18 by josfelip          #+#    #+#              #
#    Updated: 2025/02/26 13:32:25 by josfelip         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/env python3
# weather_bot.py with Gemini API

"""
Weather Chatbot using Gemini API

This script creates a conversational interface where users can ask questions about
the weather in natural language. It uses Gemini API to understand the questions and
extract relevant information, then fetches weather data from WeatherAPI.com.

Usage:
    ./weather_bot.py

Requirements:
    - requests library
    - gemini library (for Gemini API)
    - python-dotenv library
    - API keys for both WeatherAPI.com and Gemini stored in .env file
"""

import os
import sys
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check for required API keys
if not WEATHER_API_KEY:
    print("Error: WeatherAPI key not found. Please add WEATHER_API_KEY to your .env file.")
    sys.exit(1)

if not GEMINI_API_KEY:
    print("Error: Gemini API key not found. Please add GEMINI_API_KEY to your .env file.")
    sys.exit(1)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def get_weather_by_location(location_name):
    """Get weather data for the given location"""
    try:
        url = "https://api.weatherapi.com/v1/current.json"
        params = {
            "key": WEATHER_API_KEY,
            "q": location_name,
            "aqi": "no"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            return None
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error connecting to weather API: {e}")
        return None

def extract_location_from_query(query):
    """Use Gemini to extract location from a query
	
	Args:
        query (str): The user's question
        
    Returns:
        str: The extracted location, or None if no location found
	"""
    prompt = f"""
    Extract the location from this weather-related query. Return ONLY the location name.
    If no location is mentioned or you're unsure, return "UNKNOWN".
    
    Query: {query}
    
    Location:
    """
    
    try:
        response = model.generate_content(prompt)
        location = response.text.strip()
        
        # If Gemini responded with "UNKNOWN", return None
        if location == "UNKNOWN":
            return None
            
        return location
        
    except Exception as e:
        print(f"Error connecting to Gemini API: {e}")
        return None

def is_weather_query(query):
    """Use Gemini to determine if a query is weather-related"""
    prompt = f"""
    Is this query asking about weather or meteorological conditions?
    Answer with ONLY "YES" or "NO".
    
    Query: {query}
    
    Answer:
    """
    
    try:
        response = model.generate_content(prompt)
        is_weather = response.text.strip()
        return is_weather == "YES"
        
    except Exception as e:
        print(f"Error connecting to Gemini API: {e}")
        return True

def generate_weather_response(query, weather_data):
    """Use Gemini to generate a natural language response about the weather"""
    location = weather_data['location']['name']
    country = weather_data['location']['country']
    temperature = weather_data['current']['temp_c']
    humidity = weather_data['current']['humidity']
    cloud = weather_data['current']['cloud']
    wind = weather_data['current']['wind_kph']
    condition = weather_data['current']['condition']['text']
    
    weather_context = f"""
    Location: {location}, {country}
    Temperature: {temperature}°C
    Humidity: {humidity}%
    Cloud Cover: {cloud}%
    Wind Speed: {wind} km/h
    Condition: {condition}
    """
    
    prompt = f"""
    User question: {query}
    
    Weather data:
    {weather_context}
    
    Provide a natural, conversational response to the user's weather-related question using the provided weather data.
    Keep your response relatively brief (2-3 sentences) and focused on answering their specific question.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        print(f"Error connecting to Gemini API: {e}")
        # Fallback to a basic response
        return f"The current weather in {location} is a temperature of {temperature} degrees (C), a humidity of {humidity}%, {'there are a lot of clouds' if cloud > 50 else 'there are few clouds'} in the sky and a wind of {wind}km/h."

def handle_user_query(query):
    """
    Process a user's query about weather.
    
    Args:
        query (str): The user's question
        
    Returns:
        str: A response to the user's question
    """
    # Check if this is a weather-related query
    if not is_weather_query(query):
        return "I'm a weather assistant. Please ask me about the weather in a specific location."
    
    # Extract location from the query
    location = extract_location_from_query(query)
    
    if not location:
        return "I couldn't determine which location you're asking about. Could you please specify a city or place?"
    
    # Get weather data for the location
    weather_data = get_weather_by_location(location)
    
    if not weather_data:
        return f"I couldn't find weather information for '{location}'. Please check the spelling or try a different location."
    
    # Generate a natural language response
    return generate_weather_response(query, weather_data)

def main():
    """Main function to run the weather chatbot."""
    print("Weather Chatbot")
    print("==============")
    print("Ask me about the weather in any location!")
    print("Type 'exit' or 'quit' to end the conversation.")
    print()
    
    # Main conversation loop
    while True:
        try:
            user_input = input("Ask?: ")
            
            # Check for exit command
            if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print("Goodbye! Have a great day!")
                break
                
            # Handle empty input
            if not user_input.strip():
                print("Please ask a question about the weather.")
                continue
                
            # Process the query and get a response
            response = handle_user_query(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye! Have a great day!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again with a different question.")

if __name__ == "__main__":
    main()