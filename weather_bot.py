# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    weather_bot.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: josfelip <josfelip@student.42sp.org.br>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/02/26 11:38:18 by josfelip          #+#    #+#              #
#    Updated: 2025/02/26 11:47:07 by josfelip         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/env python3
# weather_bot.py

"""
Weather Chatbot using Claude API

This script creates a conversational interface where users can ask questions about
the weather in natural language. It uses Claude API to understand the questions and
extract relevant information, then fetches weather data from WeatherAPI.com.

Usage:
    ./weather_bot.py

Requirements:
    - requests library
    - anthropic library (for Claude API)
    - python-dotenv library
    - API keys for both WeatherAPI.com and Claude stored in .env file
"""

import os
import sys
import json
import requests
import anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Check for required API keys
if not WEATHER_API_KEY:
    print("Error: WeatherAPI key not found. Please add WEATHER_API_KEY to your .env file.")
    sys.exit(1)

if not CLAUDE_API_KEY:
    print("Error: Claude API key not found. Please add ANTHROPIC_API_KEY to your .env file.")
    sys.exit(1)

# Initialize Claude client
claude = anthropic.Anthropic(
    api_key=CLAUDE_API_KEY,
)

def get_weather_by_location(location_name):
    """
    Get current weather data for the given location name.
    
    Args:
        location_name (str): The name of the location (city, address, etc.)
        
    Returns:
        dict: Weather data if successful, None otherwise
    """
    try:
        # Construct the API request
        url = "https://api.weatherapi.com/v1/current.json"
        params = {
            "key": WEATHER_API_KEY,
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
            return None
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error connecting to weather API: {e}")
        return None

def extract_location_from_query(query):
    """
    Use Claude to extract location information from a user query.
    
    Args:
        query (str): The user's question
        
    Returns:
        str: The extracted location, or None if no location found
    """
    system_prompt = """
    You are a helpful assistant that extracts location information from weather-related queries.
    Your task is to identify the location mentioned in the query and return ONLY the location name.
    If multiple locations are mentioned, identify the main one the user is asking about.
    If no location is mentioned or you're unsure, return "UNKNOWN".
    
    For example:
    - "What's the weather in Paris?" → "Paris"
    - "Tell me about Tokyo's temperature" → "Tokyo"
    - "Is it raining in New York City today?" → "New York City"
    - "Will it be sunny tomorrow?" → "UNKNOWN"
    
    Return ONLY the location name or "UNKNOWN", nothing else.
    """
    
    try:
        message = claude.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=50,
            system=system_prompt,
            messages=[
                {"role": "user", "content": query}
            ]
        )
        
        location = message.content[0].text.strip()
        
        # If Claude responded with "UNKNOWN", return None
        if location == "UNKNOWN":
            return None
            
        return location
        
    except Exception as e:
        print(f"Error connecting to Claude API: {e}")
        return None

def is_weather_query(query):
    """
    Use Claude to determine if a query is weather-related.
    
    Args:
        query (str): The user's question
        
    Returns:
        bool: True if the query is about weather, False otherwise
    """
    system_prompt = """
    You are a helpful assistant that determines if a query is related to weather or not.
    Your task is to respond with ONLY "YES" if the query is asking about weather, 
    temperature, precipitation, or other meteorological conditions. Otherwise, respond with ONLY "NO".
    
    For example:
    - "What's the weather in Paris?" → "YES"
    - "Tell me about the temperature" → "YES"
    - "Is it going to rain today?" → "YES"
    - "What's the capital of France?" → "NO"
    - "Tell me a joke" → "NO"
    
    Return ONLY "YES" or "NO", nothing else.
    """
    
    try:
        message = claude.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=5,
            system=system_prompt,
            messages=[
                {"role": "user", "content": query}
            ]
        )
        
        is_weather = message.content[0].text.strip()
        return is_weather == "YES"
        
    except Exception as e:
        print(f"Error connecting to Claude API: {e}")
        # If there's an error, we'll assume it's a weather query to be safe
        return True

def generate_weather_response(query, weather_data):
    """
    Use Claude to generate a natural language response about the weather.
    
    Args:
        query (str): The user's original question
        weather_data (dict): Weather data from the API
        
    Returns:
        str: A natural language response
    """
    # Extract relevant weather information
    location = weather_data['location']['name']
    country = weather_data['location']['country']
    temperature = weather_data['current']['temp_c']
    humidity = weather_data['current']['humidity']
    cloud = weather_data['current']['cloud']
    wind = weather_data['current']['wind_kph']
    condition = weather_data['current']['condition']['text']
    
    # Create a context for Claude with the weather data
    weather_context = f"""
    Location: {location}, {country}
    Temperature: {temperature}°C
    Humidity: {humidity}%
    Cloud Cover: {cloud}%
    Wind Speed: {wind} km/h
    Condition: {condition}
    """
    
    system_prompt = """
    You are a helpful weather assistant. You should provide a natural, conversational
    response to the user's weather-related question using the provided weather data.
    
    Keep your response relatively brief (2-3 sentences) and focused on answering
    their specific question using the weather data provided.
    
    Do not invent weather data or make predictions unless the data explicitly supports it.
    """
    
    try:
        message = claude.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=150,
            system=system_prompt,
            messages=[
                {"role": "user", "content": f"User question: {query}\n\nWeather data:\n{weather_context}"}
            ]
        )
        
        return message.content[0].text.strip()
        
    except Exception as e:
        print(f"Error connecting to Claude API: {e}")
        # Fallback to a basic response if Claude API fails
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