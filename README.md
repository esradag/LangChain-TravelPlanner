Here's the cleaned-up and properly formatted version of your documentation:

---

# Travel Itinerary Planner

A personalized travel itinerary planner that generates a detailed day trip schedule based on your selected city, interests, and time slots. The application also provides a dynamically centered map showing recommended places along with photos, distances, and durations.

---

## Features

- **Personalized Itinerary**: Generates a custom day trip itinerary using OpenAI's GPT-4.
- **Google Maps Integration**: Fetches place recommendations and calculates distances and durations.
- **Dynamic Map**: Displays recommended places on a map with interactive popups including images and details.
- **User Inputs**: Allows selection of city, interests, and preferred time slots.
- **Time Slot Division**: Organizes recommendations into user-defined time slots for seamless planning.

---

## Tech Stack

- **Python**: Core programming language.
- **Gradio**: For building the user interface.
- **LangChain**: For handling prompts and conversations with OpenAI's GPT-4.
- **OpenAI GPT-4**: For generating personalized itineraries.
- **Google Maps API**: For fetching recommendations, distances, and durations.
- **Folium**: For creating dynamic, interactive maps.

---

## Prerequisites

1. Python 3.11 or higher.
2. API keys for:
   - **OpenAI**: To access GPT-4.
   - **Google Maps API**: Ensure the Places API and Distance Matrix API are enabled.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/travel-itinerary-planner.git
cd travel-itinerary-planner
```

### 2. Install Dependencies
Run the following command to install the required dependencies:
```bash
pip install -r requirements.txt
```

---

## Create a `.env` File

Create a `.env` file in the root directory and add your API keys as follows:
```env
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
OPENAI_API_KEY=your_openai_api_key
```

---

## Usage

Run the application with the following command:
```bash
python app.py
```

After running, open your browser and go to `http://127.0.0.1:7860` to interact with the app.

To make the app publicly accessible, modify the `interface.launch()` function in `app.py`:
```python
interface.launch(share=True)
```

---

## Contribution

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-or-bugfix
   ```
3. Commit your changes and push the branch:
   ```bash
   git push origin feature-or-bugfix
   ```
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Let me know if you'd like to add or modify any sections! 🚀
