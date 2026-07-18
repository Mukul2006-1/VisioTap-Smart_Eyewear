# 👓 Smart Eyewear – Blink Gesture Controlled IoT Assistive Device

An IoT-based smart eyewear system that enables **hands-free interaction** through **eye-blink gestures**. Using an infrared eye-blink sensor, Raspberry Pi, and camera module, the system can capture images, record videos, and automatically send emergency alerts with captured images via email—without any manual intervention.

The project combines **embedded systems**, **IoT**, and **wearable technology** to provide an intuitive and accessible human-computer interaction interface.

---

## ✨ Features

- 👁️ **Blink Gesture Recognition**
  - **Double Blink** → Capture an image and automatically send an SOS email with the image attached.
  - **Long Blink (≈1.5 seconds)** → Start video recording.
  - **Long Blink while recording** → Stop recording and save the video.

- 📸 **Automatic Image Capture**
  - Captures images using the Raspberry Pi Camera Module.
  - Saves images with timestamp-based filenames.

- 🎥 **Hands-Free Video Recording**
  - Starts and stops recording using only eye gestures.
  - Converts recorded `.h264` videos into `.mp4` format using FFmpeg.

- 📧 **Emergency SOS Alert**
  - Sends the captured image to a predefined email address automatically.
  - Uses Gmail SMTP with secure App Password authentication.
  - Requires no user interaction after the blink gesture.

- ⚡ **Completely Hands-Free Operation**
  - No physical buttons, keyboard, or touchscreen required.
  - All actions are controlled using eye blinks.

---

# 🛠️ Hardware Used

- Raspberry Pi 4
- Infrared Eye Blink Sensor
- Raspberry Pi Camera Module
- MicroSD Card
- Power Supply / Battery

---

# 💻 Software Stack

- Python 3
- Raspberry Pi OS
- RPi.GPIO
- rpicam-still
- rpicam-vid
- FFmpeg
- smtplib
- EmailMessage
- threading
- subprocess

---

# ⚙️ System Workflow

The eye-blink sensor continuously monitors eye movements.

The system classifies blinks into two categories:

- **Short Blink**
- **Long Blink (≥ 1.5 seconds)**

### Double Short Blink

```
User Double Blinks
        │
        ▼
IR Eye Blink Sensor
        │
        ▼
Raspberry Pi
        │
        ▼
Capture Image
        │
        ▼
Save Image
        │
        ▼
Send SOS Email
```

### Long Blink

```
Long Blink
      │
      ▼
Start Video Recording
      │
      ▼
Long Blink Again
      │
      ▼
Stop Recording
      │
      ▼
Convert .h264 → .mp4
```

---

# 📂 Project Structure

```
Smart-Eyewear/
│
├── smart_eyewear.py      # Main application
├── README.md
└── assets/               # Images/GIFs (optional)
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/Smart-Eyewear.git
cd Smart-Eyewear
```

## 2. Install Dependencies

```bash
pip install RPi.GPIO

sudo apt update
sudo apt install ffmpeg
```

Ensure the Raspberry Pi Camera is enabled.

---

## 3. Configure Email Credentials

Replace the following variables inside the script:

```python
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_16_character_app_password"
TO_EMAIL = "recipient@gmail.com"
```

> **Note:** Use a Gmail App Password instead of your Gmail account password.

---

## 4. Run the Application

```bash
python3 smart_eyewear.py
```

---

# 👁️ Blink Gesture Mapping

| Gesture | Action |
|----------|--------|
| Double Short Blink | Capture Image + Send SOS Email |
| Long Blink (≈1.5s) | Start Video Recording |
| Long Blink While Recording | Stop Recording |

---

# 📁 Output

### Captured Images

```
captured_YYYYMMDD-HHMMSS.jpg
```

### Recorded Videos

```
video_YYYYMMDD-HHMMSS.mp4
```

---

# 📧 Email Alert

When a double blink is detected:

- An image is captured.
- The image is attached to an email.
- An SOS alert is automatically sent to the configured recipient.

Example email:

**Subject**

```
🚨 SOS Alert from Smart Eyewear
```

**Body**

```
Emergency detected via double blink.
Please check the attached image.
```

---

# 🌍 Potential Applications

- Emergency assistance systems
- Assistive technology for people with disabilities
- Smart wearable devices
- Hands-free photography
- Personal safety solutions
- Healthcare monitoring
- Industrial hands-free operation

---

# 🔮 Future Enhancements

- Live video streaming
- GPS location sharing in SOS emails
- Cloud backup for captured media
- WhatsApp/Telegram emergency alerts
- AI-based blink classification
- Face recognition
- Voice assistant integration
- Mobile application support

---

# 👨‍💻 Author

**Mukul**

If you found this project helpful, consider giving it a ⭐ on GitHub!
