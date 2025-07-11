# 🛡️ SHE-ALERT PRO – Smart Emergency Safety System for Women



## 🚀 Overview

**SHE-ALERT PRO** is a powerful, AI-driven emergency alert system designed specifically to enhance women’s safety. With just one tap, it captures your live location, clicks an instant photo, and sends an alert message to trusted contacts. The system works even on low-end systems, ensuring accessibility for everyone.

> 🔒 **Mission:** To provide a reliable, real-time, and cost-free solution for women's safety using smart tech.

---

## 🎯 Features

- 📍 **Live Location Tracking** – Sends real-time GPS coordinates of the user.
- 📸 **Automatic Photo Capture** – Captures an image through webcam (front or back) for visual evidence.
- 🆘 **Instant SOS Alert** – Sends a predefined emergency message with media to trusted contacts.
- 📢 **Voice Alerts** – Speaks warning messages using Text-to-Speech.
- 📝 **Custom Message Support** – Users can edit and personalize the emergency message.
- 📴 **Offline-Ready** – Designed to support SMS fallback and local storage.
- 🪄 **User-Friendly GUI** – Clean interface for easy access and interaction.

---

## 💻 Tech Stack

| Component        | Technology          |
|------------------|---------------------|
| Programming      | Python              |
| GUI              | Tkinter             |
| Location         | Geopy, Geocoder     |
| Camera           | OpenCV              |
| Alerts           | Twilio API          |
| Speech           | pyttsx3             |
| Threads          | Python threading    |
| Mobile App (Upcoming) | Kivy           |

---

## 🧠 How It Works

1. User launches the application and clicks the **"Alert Now"** button.
2. App performs the following actions simultaneously:
   - Captures user’s **live GPS location**
   - Takes a **photo** using the system camera
   - Sends an **SOS message**, photo, and location to the contact list via Twilio or email
   - Plays a **voice message** for alerting people nearby

3. Displays confirmation pop-ups after successful alert delivery.

---


