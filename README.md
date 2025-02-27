# Weather Information Chatbot

A Python-based chatbot that uses external APIs to answer weather-related questions in real-time. This project is part of the Discovery Piscine - AI/ML Module 2.

## Project Overview

This project demonstrates how to build an intelligent agent that can respond to user queries about weather conditions in various locations. It progresses through several stages of complexity:

1. **Basic Weather Information** - Retrieving weather data using coordinates
2. **Geolocation Support** - Adding the ability to use location names instead of coordinates
3. **Conversational Interface** - Creating a chatbot that can interpret natural language questions

## Features

- Get current weather data using latitude and longitude coordinates
- Get weather data by location name (city, region, etc.)
- Natural language processing for weather queries using Groq API integration
- Display of comprehensive weather information including:
  - Temperature
  - Humidity
  - Cloud coverage
  - Wind speed
  - Weather conditions
  - UV index
  - Local time

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- A WeatherAPI.com API key (free tier available)
- A Groq API key (for the chatbot functionality)

### Setting Up the Virtual Environment

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     weather_venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source weather_venv/bin/activate
     ```

3. Install the required packages:
   ```bash
   pip install -r ex00/requirements.txt
   ```

### API Keys Configuration

1. Create a `.env` file in the project root with the following content:
   ```
   WEATHER_API_KEY=your_weatherapi_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

2. Replace the placeholder values with your actual API keys.

## Usage

### Exercise 1: Weather by Coordinates

Run the script and input the latitude and longitude when prompted:

```bash
cd ex01
python weather.py
```

Example output:
```
Weather Information Program
==========================
Latitude?: 48.866667
Longitude?: 2.333333

The current weather for this location is:
- temperature(C): 11
- humidity: 64%
- cloud: 72%
- wind: 13km/h
- condition: Partly cloudy
- feels like: 9°C
- UV index: 2

Location: Paris, Ile-de-France, France
Local time: 2025-02-26 17:30
```

### Exercise 2: Weather by Location Name

Run the script and enter a location name when prompted:

```bash
cd ex02
python weather_geoloc.py
```

Example output:
```
Weather Information Program with Geolocation
===========================================
Location?: Paris

The current weather in Paris is:
- temperature(C): 11
- humidity: 64%
- cloud: 72%
- wind: 13km/h
- condition: Partly cloudy
- feels like: 9°C
- UV index: 2

Coordinates: 48.87, 2.33
Country: France
Local time: 2025-02-26 17:30
```

### Exercise 3: Weather Chatbot

Run the chatbot and ask it weather-related questions in natural language:

```bash
cd ex03
python weather_bot_groq.py
```

Example conversation:
```
Weather Chatbot (Groq Version)
==============================
Ask me about the weather in any location!
Type 'exit' or 'quit' to end the conversation.

Ask?: What's the weather like in Tokyo right now?
The current weather in Tokyo is quite pleasant with a temperature of 18 degrees Celsius. The humidity is at 65% with partly cloudy skies, and there's a gentle breeze at 8km/h.

Ask?: How about San Francisco?
San Francisco is currently experiencing cool weather at 14 degrees Celsius with a humidity of 72%. It's mostly cloudy with fog rolling in from the bay, and there's a light wind at 10km/h.

Ask?: quit
Goodbye! Have a great day!
```

## Project Structure

```
├── ex00/                       # Virtual environment setup
│   ├── requirements.txt        # Required Python packages
│   └── test_weather_api.py     # Script to test WeatherAPI connectivity
│
├── ex01/                       # Weather by coordinates
│   ├── 42spCoordinates.txt     # Example coordinates file
│   └── weather.py              # Script to get weather by coordinates
│
├── ex02/                       # Weather by location name
│   └── weather_geoloc.py       # Script to get weather by location name
│
├── ex03/                       # Weather chatbot
│   ├── weather_bot_groq.py     # Main chatbot script using Groq
│   └── groq_models_list.py     # Utility to list available Groq models
│
└── README.md                   # Project documentation
```

## Troubleshooting

- **API Key Issues**: Ensure your API keys are correct and properly set in the `.env` file.
- **Location Not Found**: Try providing more specific location names (e.g., "Paris, France" instead of just "Paris").
- **Connection Errors**: Check your internet connection and firewall settings.

## Further Development Ideas

- Add support for weather forecasts (not just current weather)
- Implement caching to reduce API calls
- Add a graphical user interface (GUI)
- Support for voice input/output
- Handle more complex weather-related queries

## License

This project is part of the Discovery Piscine - AI/ML educational curriculum.

## Acknowledgments

- WeatherAPI.com for providing weather data
- Groq API for natural language processing capabilities