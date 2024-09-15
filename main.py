import streamlit as st
from together import Together
from dotenv import load_dotenv
import os
import re
import requests
import hashlib

# Load environment variables
load_dotenv()

# Configure API keys
Together.api_key = os.getenv("TOGETHER_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Static Data: Avrage Crop Prices for both Pakistan and India for last 5 years
CROP_PRICES = {
    "Pakistan": {
        "Wheat": {"price": 1500, "unit": "PKR/40kg"},
        "Cotton": {"price": 4200, "unit": "PKR/40kg"},
        "Mustard": {"price": 3600, "unit": "PKR/40kg"},
        "Sugarcane": {"price": 180, "unit": "PKR/40kg"},
        "Rice": {"price": 2200, "unit": "PKR/40kg"},
        "Maize": {"price": 1800, "unit": "PKR/40kg"},
        "Chickpeas": {"price": 3000, "unit": "PKR/40kg"},
        "Potatoes": {"price": 1200, "unit": "PKR/40kg"}
    },
    "India": {
        "Wheat": {"price": 2200, "unit": "INR/Quintal"},
        "Cotton": {"price": 6200, "unit": "INR/Quintal"},
        "Mustard": {"price": 5500, "unit": "INR/Quintal"},
        "Sugarcane": {"price": 315, "unit": "INR/Quintal"},
        "Rice": {"price": 2000, "unit": "INR/Quintal"},
        "Maize": {"price": 1850, "unit": "INR/Quintal"},
        "Soybeans": {"price": 4000, "unit": "INR/Quintal"},
        "Turmeric": {"price": 7500, "unit": "INR/Quintal"}
    }
}

# Static Data: Agricultural Land Stats
AGRICULTURAL_STATS = {
    "Pakistan": {"agricultural_land_percent": 47.6},
    "India": {"agricultural_land_percent": 60.5}
}

# Expanded Mapping of Regions to Coordinates (latitude, longitude)
REGION_COORDINATES = {
    "Punjab, Pakistan": (31.1471, 75.3412),
    "Sindh, Pakistan": (25.8943, 68.5247),
    "Balochistan, Pakistan": (29.4202, 65.5943),
    "Khyber Pakhtunkhwa, Pakistan": (34.9526, 72.3311),
    "Gujarat, India": (22.2587, 71.1924),
    "Maharashtra, India": (19.7515, 75.7139),
    "Punjab, India": (31.1471, 75.3412),
    "Tamil Nadu, India": (11.1271, 78.6569),
    "Rajasthan, India": (27.0238, 74.2179)
}

# Expanded Soil Types
SOIL_TYPES = ["Sandy", "Clay", "Loamy", "Silt", "Peaty", "Saline", "Chalky", "Red Soil", "Black Soil", "Alluvial Soil"]

# Expanded Resources Available
RESOURCES = ["Water", "Fertilizers", "Machinery", "Labor", "Pesticides", "Electricity", "Seeds", "Organic Fertilizer"]

# Sample user database (extend to use a real database for production)
user_db = {
    "user1": hashlib.sha256("washingMachine".encode()).hexdigest(),
    "user2": hashlib.sha256("ironStand".encode()).hexdigest()
}

# Function to hash the passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check if the password is correct
def check_password(username, password):
    if username in user_db:
        return user_db[username] == hash_password(password)
    return False

# Function to handle user signup
def signup(username, password):
    if username in user_db:
        st.error("Username already exists. Please choose a different username.")
        return False
    user_db[username] = hash_password(password)
    st.success("Signup successful! You can now log in.")
    return True

# Login/Signup form
def login_page():
    st.title("Welcome to AI-Powered Crop Recommendation System")
    
    # Create login or signup tabs
    choice = st.sidebar.radio("Login or Signup", ["Login", "Signup"])
    
    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if check_password(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password.")
    
    elif choice == "Signup":
        username = st.text_input("New Username")
        password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Signup"):
            if password != confirm_password:
                st.error("Passwords do not match!")
            else:
                if signup(username, password):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username

# The main application after user logs in
def main_app():
    st.title("AI-Powered Crop Recommendation System")
    
    # User input fields
    if st.button("Sign Out"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.rerun()

    region = st.selectbox("Select Region", list(REGION_COORDINATES.keys()))
    soil_type = st.selectbox("Soil Type", SOIL_TYPES)
    season = st.selectbox("Time of the Year", ["Spring", "Summer", "Autumn", "Winter"])
    return_expectation = st.selectbox("Return Expectation", ["High", "Medium", "Low"])
    investment_amount = st.slider("Investment Amount (in local currency)", 500000, 5000000)
    available_area = st.number_input("Available Area (in hectares)", min_value=0.1, max_value=1000.0, value=1.0)
    
    resources = st.multiselect("Available Resources", RESOURCES)
    
    if st.button("Get Crop Recommendations"):
        with st.spinner("Fetching recommendations..."):
            recommendations = get_crop_recommendations(region, soil_type, season, return_expectation, investment_amount, available_area, resources)
            display_recommendations(recommendations)

# Display recommendations as before
def get_crop_recommendations(region, soil_type, season, return_expectation, investment_amount, available_area, resources):
    market_prices = fetch_market_prices(region)
    weather_data = fetch_weather_data(region)
    agricultural_stats = fetch_agricultural_stats(region)
    
    prompt = f"""
    Given the following farming scenario:
    - Region: {region}
    - Soil Type: {soil_type}
    - Season: {season}
    - Return Expectation: {return_expectation}
    - Investment Amount: {investment_amount}
    - Available Area: {available_area} hectares
    - Available Resources: {', '.join(resources)}
    
    Real-time data:
    - Market Prices: {market_prices}
    - Weather Data: {weather_data}
    - Agricultural Statistics: {agricultural_stats}
    
    Recommend the top 3 crops to cultivate and provide detailed explanations. For each crop, use the following format:

    Crop: [Crop Name]
    Explanation: [Detailed explanation of why it's suitable]
    Projected Return: [Percentage]
    Investment Ratio: [Decimal]
    Risk Level: [Low/Medium/High]

    Ensure you provide exactly 3 recommendations, numbered from 1 to 3. Do not include additional placeholder text.
    """

    client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[            
            {"role": "system", "content": "You are an expert agricultural consultant with decades of experience in crop selection and farming strategies."},
            {"role": "user", "content": prompt}
            ],
        max_tokens=1000,
        temperature=0.7,
        stream=False
    )

    if response and hasattr(response, 'choices') and len(response.choices) > 0:
        return response.choices[0].message.content.strip()
    else:
        st.error("Failed to fetch crop recommendations.")
        return "No recommendations available."

# Fetch other static data as before
def fetch_market_prices(region):
    country = "Pakistan" if "Pakistan" in region else "India"
    prices = ", ".join([f"{crop}: {data['price']} {data['unit']}" for crop, data in CROP_PRICES[country].items()])
    return f"Average market prices in {country}: {prices}"

def fetch_weather_data(region):
    lat, lon = REGION_COORDINATES[region]
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        return f"Temperature: {temp}°C, Humidity: {humidity}%, Conditions: {description}"
    except requests.RequestException as e:
        st.error(f"Failed to fetch weather data: {str(e)}")
        return "Weather data unavailable"

def fetch_agricultural_stats(region):
    country = "Pakistan" if "Pakistan" in region else "India"
    stats = AGRICULTURAL_STATS.get(country, {"agricultural_land_percent": "N/A"})
    return f"Agricultural land: {stats['agricultural_land_percent']}%"

def display_recommendations(recommendations):
    st.subheader("Crop Recommendations")
    
    # Split the recommendations into individual crop suggestions
    crops = re.split(r'\n\s*\d+\.', recommendations)
    crops = [crop.strip() for crop in crops if crop.strip()]
    
    # Iterate through the crops and display them
    for i, crop in enumerate(crops[:3], 1):
        lines = crop.split('\n')
        crop_name = lines[0].split(': ')[1] if len(lines) > 0 and ': ' in lines[0] else f"Recommendation {i}"

        if crop_name.startswith("Recommendation"):
            continue
        
        with st.expander(f"Recommendation {i}: {crop_name}"):
            for line in lines:
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    st.write(f"{key}:{value}")

# Main application flow
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    main_app()
else:
    login_page()
