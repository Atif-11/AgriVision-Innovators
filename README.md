# Crop Recommendation System

This project is an AI-powered web application designed to assist farmers in making informed crop choices based on various inputs such as region, soil type, investment amount, and available resources.

## Features

- User Authentication (Sign up and Login)
- Region and Soil Type Selection
- Seasonal and Financial Inputs (investment, area, ROI expectations)
- Resource Specification (water, fertilizers, machinery, labor)
- Real-time Weather Data Integration (OpenWeather API)
- Static Agricultural Data (Historical crop prices and stats for India and Pakistan)
- AI-powered Crop Recommendations (Meta-Llama 3.1 LLM)
- Detailed Suggestions on Projected Return, Investment Ratio, and Risk Level
- Interactive UI with expandable recommendation sections

## Technologies Used

- **Streamlit** for building the web interface
- **Meta-Llama 3.1** hosted on the Together platform for generating crop recommendations
- **OpenWeather API** for real-time weather data
- **Python** for backend logic and data processing

## How it Works

1. Users provide region, soil type, and resources available.
2. The application uses real-time weather data and static agricultural data to generate personalized crop recommendations.
3. Each recommendation includes projected returns, investment ratios, and associated risks.
