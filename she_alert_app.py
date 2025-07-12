import streamlit as st
import cv2
import os
import requests
import csv
import folium
import platform
import speech_recognition as sr
import threading
from datetime import datetime
from streamlit_folium import st_folium
import urllib.parse
import webbrowser

# Set page config
st.set_page_config(page_title="SHE-ALERT 🚨", page_icon="👩‍🦰")

# Sidebar for navigation/info
with st.sidebar:
    st.header("👩‍🦰 SHE-ALERT Menu")
    st.markdown("---")
    st.markdown("**Developed for Women's Safety**")
    st.markdown("---")
    st.subheader("ℹ️ How it Works")
    st.markdown("""
    1. Click **Send Emergency Alert** or speak **'help'** to trigger the alert.
    2. Your webcam captures your photo.
    3. Your current location is detected via IP.
    4. Alert is saved with time and location.
    5. WhatsApp alert message opens for emergency contacts.
    6. You or your saved contact can act on the alert.
    """)

    st.subheader("❓ FAQ")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Q1: Does this work offline?**")
        st.markdown("No, it needs internet for WhatsApp and map location.")

        st.markdown("**Q2: Can I add multiple contacts?**")
        st.markdown("Yes, save multiple WhatsApp numbers.")

    with col2:
        st.markdown("**Q3: Is my data saved online?**")
        st.markdown("No, all alerts are stored locally.")

        st.markdown("**Q4: Can I test without alerting real people?**")
        st.markdown("Yes, use your own number during testing.")

st.title("🚨 SHE-ALERT Emergency System")

# ---------- Function to get IP-based location ----------
def get_location():
    try:
        ipinfo = requests.get("https://ipinfo.io").json()
        loc = ipinfo.get("loc", "0,0").split(',')
        city = ipinfo.get("city", "")
        region = ipinfo.get("region", "")
        country = ipinfo.get("country", "")
        return {
            "latitude": float(loc[0]),
            "longitude": float(loc[1]),
            "address": f"{city}, {region}, {country}",
            "city": city
        }
    except:
        return {
            "latitude": 0.0,
            "longitude": 0.0,
            "address": "Unknown",
            "city": "Unknown"
        }

# ---------- Static police stations (based on city) ----------
def get_nearest_police(city):
    police_db = {
        "Mumbai": "Dadar Police Station",
        "Pune": "Shivaji Nagar Police Station",
        "Delhi": "Connaught Place Police Station",
        "Bangalore": "MG Road Police Station",
        "Chennai": "T Nagar Police Station",
        "Hyderabad": "Jubilee Hills Police Station",
        "Unknown": "-- Not available --"
    }
    return police_db.get(city, "-- No data for this city --")

# ---------- WhatsApp message sender ----------
def send_whatsapp_alerts(location_data, timestamp):
    message = (
        f"🚨 EMERGENCY ALERT!\n"
        f"Time: {timestamp}\n"
        f"Location: {location_data['address']}\n"
        f"https://www.google.com/maps?q={location_data['latitude']},{location_data['longitude']}\n"
        f"Please help me immediately!"
    )
    encoded_message = urllib.parse.quote(message)

    if os.path.exists("contacts.csv"):
        with open("contacts.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                number = row[0].strip()
                if number.isdigit():
                    link = f"https://api.whatsapp.com/send?phone={number}&text={encoded_message}"
                    webbrowser.open(link)

# ---------- Emergency alert function ----------
def trigger_emergency_alert():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image_path = "alert_photo.jpg"
    location_data = get_location()
    location = location_data["address"]

    # Capture photo
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        cv2.imwrite(image_path, frame)
        st.image(image_path, caption="📸 Captured Photo", width=400)
    cam.release()

    # Log to CSV
    with open("alert_log.csv", "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        if os.stat("alert_log.csv").st_size == 0:
            writer.writerow(["Timestamp", "Image", "Location"])
        writer.writerow([now, image_path, location])
    st.success(f"✅ Alert logged at {now} - {location}")

    # Send WhatsApp alerts
    send_whatsapp_alerts(location_data, now)
    st.info("📤 WhatsApp opened for contacts. Please click Send.")

# ---------- Voice recognition thread ----------
def voice_mode():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    st.info("🎤 Listening for keyword 'help'... Speak now")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        if "help" in text.lower():
            st.warning("🔊 'Help' detected! Triggering alert...")
            trigger_emergency_alert()
        else:
            st.info("❌ Keyword 'help' not detected.")
    except:
        st.error("Speech recognition failed. Please try again.")

# ---------- Custom dark red emergency button ----------
custom_button_style = """
    <style>
    div.stButton > button:first-child {
        background-color: #8B0000;
        color: white;
        font-weight: bold;
        height: 3em;
        width: 100%;
        border-radius: 10px;
    }
    </style>
"""
st.markdown(custom_button_style, unsafe_allow_html=True)

# Emergency Button
if st.button("📸 Send Emergency Alert"):
    trigger_emergency_alert()

# Voice Button
if st.button("🎤 Voice Mode ON"):
    threading.Thread(target=voice_mode).start()

# Location Refresh Button
if st.button("🔄 Refresh Location"):
    st.success("📍 Location refreshed!")

# Map
st.subheader("🗺️ Your Location on Map")
loc = get_location()
m = folium.Map(location=[loc["latitude"], loc["longitude"]], zoom_start=13)
folium.Marker([loc["latitude"], loc["longitude"]], tooltip="You are here").add_to(m)
st_folium(m, width=700, height=350)

st.markdown("<hr>", unsafe_allow_html=True)

# Nearest Police Station
st.subheader("🚓 Nearest Police Station")
st.info(f"👮 Based on your city ({loc['city']}): {get_nearest_police(loc['city'])}")

# Alert History
st.subheader("📄 Alert History")
if os.path.exists("alert_log.csv"):
    with open("alert_log.csv", "r", encoding="utf-8") as f:
        st.code(f.read())
else:
    st.info("No alerts logged yet.")
