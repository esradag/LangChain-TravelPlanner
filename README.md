# Travel Itinerary Planner

A personalized travel itinerary planner that generates a detailed day trip schedule based on your selected city, interests, and time slots. The application also provides a dynamically centered map showing recommended places along with photos, distances, and durations.

## Features

- **Personalized Itinerary**: Generates a custom day trip itinerary using OpenAI's GPT-4.
- **Google Maps Integration**: Fetches place recommendations and calculates distances and durations.
- **Dynamic Map**: Displays recommended places on a map with interactive popups including images and details.
- **User Inputs**: Allows selection of city, interests, and preferred time slots.
- **Time Slot Division**: Divides recommendations into user-defined time slots for better planning.

## Tech Stack

## Prerequisites

1. Python 3.11 or higher.
2. API keys for:
   - OpenAI
   - Google Maps API (enable Places API and Distance Matrix API).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/travel-itinerary-planner.git
   cd travel-itinerary-planner
## Install Dependencies

Run the following command to install the required dependencies:

    ```bash
     pip install -r requirements.txt

## Create a `.env` File

Create a `.env` file in the root directory and add your API keys as follows:

    ```env
     GOOGLE_MAPS_API_KEY=your_google_maps_api_key
     OPENAI_API_KEY=your_openai_api_key
   
## Usage

Run the application with the following command:

```bash
python app.py
```

You can copy and paste this into your documentation directly.
```

