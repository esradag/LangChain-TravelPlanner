import gradio as gr
import os
from typing import TypedDict, Annotated, List
from langchain.schema import HumanMessage, AIMessage
from langchain_community.chat_models import ChatOpenAI

from langchain.prompts import ChatPromptTemplate
import requests
import folium
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

class PlannerState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], "The messages in the conversation"]
    city: str
    interests: List[str]
    times: List[str]
    recommendations: List[dict]
    itinerary: str

# Define the LLM
llm = ChatOpenAI(
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4"
)

# Define the itinerary prompt
itinerary_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a travel assistant. Create a detailed day trip itinerary for {city} during the following time slots: {times}. Use the user's interests and the recommended places: {recommendations}. For each time slot:\n"
               "- Suggest a place to visit and an activity.\n"
               "- Include the travel time and distance between locations.\n"
               "- Make the itinerary clear and actionable."),
    ("human", "Generate a travel itinerary."),
])

# Function to fetch recommendations from Google Maps API
def get_recommendations_with_distance(city: str, interests: List[str]) -> List[dict]:
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    distance_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    recommendations = []

    for interest in interests:
        params = {
            "query": f"{interest} in {city}",
            "key": GOOGLE_MAPS_API_KEY
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            places = response.json().get("results", [])
            if places:
                for place in places[:5]:  # İlk 5 öneriyi alıyoruz
                    name = place.get("name")
                    address = place.get("formatted_address")
                    rating = place.get("rating", "N/A")
                    location = place.get("geometry", {}).get("location", {})
                    latitude = location.get("lat")
                    longitude = location.get("lng")
                    photo_reference = place.get("photos", [{}])[0].get("photo_reference", "")
                    photo_url = (
                        f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_reference}&key={GOOGLE_MAPS_API_KEY}"
                        if photo_reference
                        else "https://via.placeholder.com/400x300?text=No+Image"
                    )

                    # Calculate distance from city center
                    distance_params = {
                        "origins": f"{latitude},{longitude}",
                        "destinations": f"{city}",
                        "key": GOOGLE_MAPS_API_KEY
                    }
                    distance_response = requests.get(distance_url, params=distance_params)
                    distance_data = distance_response.json()
                    distance = distance_data["rows"][0]["elements"][0]["distance"]["text"] if distance_data["rows"] else "N/A"
                    duration = distance_data["rows"][0]["elements"][0]["duration"]["text"] if distance_data["rows"] else "N/A"

                    recommendations.append({
                        "name": name,
                        "address": address,
                        "rating": rating,
                        "latitude": latitude,
                        "longitude": longitude,
                        "photo_url": photo_url,
                        "distance": distance,
                        "duration": duration
                    })
    return recommendations

# Function to divide recommendations into user-selected time slots
def divide_into_time_slots(recommendations: List[dict], times: List[str]) -> dict:
    time_slots = {time: [] for time in times}  # Kullanıcı zaman dilimlerine göre böl
    for i, rec in enumerate(recommendations):
        slot = times[i % len(times)]  # Mekanları sırasıyla zaman dilimlerine ata
        time_slots[slot].append(rec)
    return time_slots

# Function to plot recommendations on a map with dynamic centering
def plot_map_by_time_slots(time_slots: dict) -> str:
    # İlk önerinin koordinatlarını kullanarak harita merkezi belirle
    first_location = None
    for recs in time_slots.values():
        if recs:
            first_location = [recs[0]["latitude"], recs[0]["longitude"]]
            break

    if not first_location:
        # Eğer öneri yoksa varsayılan bir konum (ör. Roma)
        first_location = [41.9028, 12.4964]  # Roma

    # Create a base map centered around the first location
    travel_map = folium.Map(location=first_location, zoom_start=13)

    # Define colors for different time slots
    colors = ["red", "blue", "green", "purple"]
    time_slot_colors = {time: colors[i % len(colors)] for i, time in enumerate(time_slots.keys())}

    # Add markers for each time slot
    for time_slot, recs in time_slots.items():
        for rec in recs:
            # Custom HTML for the popup with image
            popup_html = f"""
            <div style="width:200px;">
                <h4>{rec['name']}</h4>
                <p>{rec['address']}</p>
                <p>Rating: {rec['rating']}/5</p>
                <p>Distance: {rec['distance']} | Duration: {rec['duration']}</p>
                <img src="{rec['photo_url']}" alt="Image" style="width:100%;height:auto;">
                <p><b>Time Slot:</b> {time_slot}</p>
            </div>
            """
            popup = folium.Popup(popup_html, max_width=250)
            folium.Marker(
                location=[rec["latitude"], rec["longitude"]],
                popup=popup,
                icon=folium.Icon(color=time_slot_colors[time_slot])
            ).add_to(travel_map)

    # Save map to an HTML string
    return travel_map._repr_html_()

# Function to generate an itinerary
def travel_planner(city: str, interests: List[str], times: List[str]):
    # Fetch recommendations
    recommendations = get_recommendations_with_distance(city, interests)
    time_slots = divide_into_time_slots(recommendations, times)

    # Generate map
    map_html = plot_map_by_time_slots(time_slots)

    # Format recommendations for the model
    formatted_recommendations = "\n".join([
        f"{slot}:\n" + "\n".join([f"- {rec['name']} ({rec['rating']}/5): {rec['address']} (Distance: {rec['distance']}, Duration: {rec['duration']})" for rec in recs])
        for slot, recs in time_slots.items()
    ])

    # Generate itinerary using LLM
    response = llm(itinerary_prompt.format_messages(
        city=city,
        times=", ".join(times),
        recommendations=formatted_recommendations
    ))
    itinerary = response.content if response.content else "The model could not generate an itinerary."

    # Combine itinerary and map
    return itinerary, map_html

# Build the Gradio interface
interface = gr.Interface(
    fn=travel_planner,
    inputs=[
        gr.Textbox(label="Enter the city for your trip"),
        gr.CheckboxGroup(
            choices=["Museum", "Restaurant", "Park", "Shopping", "Historical Places", "Nature"],
            label="Select your interests"
        ),
        gr.CheckboxGroup(
            choices=["09:00-12:00 (Morning)", "12:00-15:00 (Afternoon)", "15:00-18:00 (Evening)", "18:00-21:00 (Night)"],
            label="Select the time slots for your trip"
        ),
    ],
    outputs=[
        gr.Textbox(label="Generated Itinerary"),
        gr.HTML(label="Map of Recommended Places by Time Slot")
    ],
    title="Travel Itinerary Planner",
    description="Enter a city, select your interests, and choose time slots to generate a personalized itinerary including travel distances, durations, and view a dynamically centered map with images."
)

interface.launch()
