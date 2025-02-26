# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    weather_bot_openai.py                              :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: josfelip <josfelip@student.42sp.org.br>    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/02/26 13:56:06 by josfelip          #+#    #+#              #
#    Updated: 2025/02/26 14:03:46 by josfelip         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/env python3
# weather_bot_openai.py

import os
import sys
import requests
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API keys
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure OpenAI
openai.api_key = OPENAI_API_KEY

# Check for required API keys
if not WEATHER_API_KEY:
    print("Error: WeatherAPI key not found. Please add WEATHER_API_KEY to your .env file.")
    sys.exit(1)

if not OPENAI_API_KEY:
    print("Error: OpenAI API key not found. Please add OPENAI_API_KEY to your .env file.")
    sys.exit(1)

def get_weather_by_location(location_name):
    """
    Get current weather data for the given location name.
    
    This function connects to the WeatherAPI service and retrieves 
    current weather conditions for the specified location.
    
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
        
        # Send the request with a timeout to prevent hanging
        response = requests.get(url, params=params, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            # This typically means the location wasn't found
            return None
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error connecting to weather API: {e}")
        return None

def extract_location_from_query(query):
    """
    Use OpenAI to extract location information from a user query.
    
    This function sends the user's question to OpenAI's language model,
    asking it to identify and extract any location mentioned in the text.
    
    Args:
        query (str): The user's question
        
    Returns:
        str: The extracted location, or None if no location found
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You extract location names from weather-related queries. Return ONLY the location name, nothing else. If no location is mentioned or you're unsure, return only the word 'UNKNOWN'."},
                {"role": "user", "content": query}
            ],
            max_tokens=20,
            temperature=0.1  # Low temperature for more predictable responses
        )
        
        location = response.choices[0].message.content.strip()
        
        # If OpenAI responded with "UNKNOWN", return None
        if location.upper() == "UNKNOWN":
            return None
            
        return location
        
    except Exception as e:
        print(f"Error connecting to OpenAI API: {e}")
        return None

def is_weather_query(query):
    """
    Use OpenAI to determine if a query is weather-related.
    
    This function analyzes the user's question to determine if it's asking
    about weather conditions or other meteorological information.
    
    Args:
        query (str): The user's question
        
    Returns:
        bool: True if the query is about weather, False otherwise
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Determine if a query is asking about weather or meteorological conditions. Answer with ONLY 'YES' or 'NO', nothing else."},
                {"role": "user", "content": query}
            ],
            max_tokens=5,
            temperature=0.1  # Low temperature for more deterministic responses
        )
        
        is_weather = response.choices[0].message.content.strip()
        return is_weather.upper() == "YES"
        
    except Exception as e:
        print(f"Error connecting to OpenAI API: {e}")
        # If there's an error, we'll assume it's a weather query to be safe
        return True

def generate_weather_response(query, weather_data):
    """
    Use OpenAI to generate a natural language response about the weather.
    
    This function takes the user's original question and the retrieved weather data
    and creates a conversational, natural language response that directly addresses
    the user's query.
    
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
    
    # Create a context for OpenAI with the weather data
    weather_context = f"""
    Location: {location}, {country}
    Temperature: {temperature}°C
    Humidity: {humidity}%
    Cloud Cover: {cloud}%
    Wind Speed: {wind} km/h
    Condition: {condition}
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful weather assistant. Provide a natural, conversational response to the user's weather-related question using the provided weather data. Keep your response relatively brief (2-3 sentences) and focused on answering their specific question using the weather data provided. Do not invent weather data or make predictions unless the data explicitly supports it."},
                {"role": "user", "content": f"User question: {query}\n\nWeather data:\n{weather_context}"}
            ],
            max_tokens=150,
            temperature=0.7  # Slightly higher temperature for more natural responses
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error connecting to OpenAI API: {e}")
        # Fallback to a basic response if OpenAI API fails
        return f"The current weather in {location} is a temperature of {temperature} degrees (C), a humidity of {humidity}%, {'there are a lot of clouds' if cloud > 50 else 'there are few clouds'} in the sky and a wind of {wind}km/h."

def handle_user_query(query):
    """
    Process a user's query about weather.
    
    This function coordinates the entire response generation process:
    1. Checks if the question is weather-related
    2. Extracts the location mentioned in the question
    3. Retrieves weather data for that location
    4. Generates a natural language response
    
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
    """
    Main function to run the weather chatbot.
    
    This function handles the conversation loop, user input, and displays
    responses from the chatbot system.
    """
    print("Weather Chatbot (OpenAI Version)")
    print("================================")
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