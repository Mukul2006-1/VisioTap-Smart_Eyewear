import RPi.GPIO as GPIO
import time
import subprocess
import os
import threading
import sys
import smtplib
from email.message import EmailMessage

# --- GPIO setup ---
GPIO.setmode(GPIO.BCM)
blink_pin = 17  # GPIO pin connected to your eye blink sensor
GPIO.setup(blink_pin, GPIO.IN)

print("Monitoring blinks... Press Ctrl+C to stop.")

# --- Variables ---
blink_count = 0
last_blink_time = 0
double_blink_interval = 0.5  # seconds between two short blinks
long_blink_threshold = 1.5   # seconds held HIGH = long blink
recording = False
video_process = None
current_video_path = None
recording_start_time = 0
rec_thread = None
stop_rec_thread = False

# --- EMAIL CONFIGURATION ---
EMAIL_ADDRESS = "email1@gmail.com"        # your Gmail
EMAIL_PASSWORD = "16char long GMAIL app passwod"  # Gmail app password
TO_EMAIL = "email2@gmail.com"         # recipient email

# --- Helper Threads (for live timer display) ---
def recording_indicator():
    global recording_start_time, stop_rec_thread
    while not stop_rec_thread:
        elapsed = int(time.time() - recording_start_time)
        sys.stdout.write(f"\r🔴 REC {elapsed}s ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rRecording stopped.           \n")

# --- Functions ---
def capture_image():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    image_path = f"/home/mukul/captured_{timestamp}.jpg"
    print("\n📸 Double blink detected! Capturing image...")
    subprocess.run(["rpicam-still", "-o", image_path])
    print(f"✅ Image saved as {image_path}")
    return image_path

def send_sos_alert(image_path):
    """Send SOS email with captured image"""
    print("\n🚨 Sending SOS alert with captured image...")

    msg = EmailMessage()
    msg["Subject"] = "🚨 SOS Alert from Smart Eyewear"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg.set_content("Emergency detected via double blink. Please check attached image.")

    # Attach the image
    try:
        with open(image_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(f.name)
        msg.add_attachment(file_data, maintype="image", subtype="jpeg", filename=file_name)
    except Exception as e:
        print(f"⚠ Error attaching image: {e}")
        msg.set_content("Emergency detected (image not available).")

    # Send email via Gmail SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ SOS alert sent successfully!\n")
    except Exception as e:
        print(f"❌ Failed to send SOS alert: {e}")

def start_video():
    global video_process, recording, current_video_path, recording_start_time, rec_thread, stop_rec_thread
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    current_video_path = f"/home/mukul/video_{timestamp}.h264"
    print("\n🎥 Long blink detected! Starting video recording...")

    # '-t 0' keeps recording until manually stopped
    video_process = subprocess.Popen(["rpicam-vid", "-t", "0", "-o", current_video_path])
    recording = True
    recording_start_time = time.time()
    stop_rec_thread = False

    # Start live indicator thread
    rec_thread = threading.Thread(target=recording_indicator)
    rec_thread.start()
    print(f"\n🔴 Recording started: {current_video_path}")

def stop_video():
    global video_process, recording, current_video_path, stop_rec_thread, rec_thread
    if video_process:
        print("\n🛑 Long blink detected! Stopping video recording...")
        video_process.terminate()
        video_process.wait()
        recording = False

        # Stop indicator thread
        stop_rec_thread = True
        if rec_thread:
            rec_thread.join()

        # Convert to MP4
        mp4_path = current_video_path.replace(".h264", ".mp4")
        print("🔄 Converting to MP4 format...")
        try:
            subprocess.run(
                ["ffmpeg", "-y", "-i", current_video_path, "-c", "copy", mp4_path],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            os.remove(current_video_path)
            print(f"✅ Video saved as {mp4_path}\n")
        except subprocess.CalledProcessError:
            print("⚠ MP4 conversion failed. Check ffmpeg installation.")

        video_process = None
        current_video_path = None

# --- Main loop ---
try:
    blink_start_time = 0
    while True:
        sensor_value = GPIO.input(blink_pin)

        # Detect blink start
        if sensor_value and blink_start_time == 0:
            blink_start_time = time.time()

        # Detect blink end
        elif not sensor_value and blink_start_time != 0:
            blink_duration = time.time() - blink_start_time
            blink_start_time = 0

            # Long blink: toggle video
            if blink_duration >= long_blink_threshold:
                if not recording:
                    start_video()
                else:
                    stop_video()

            # Short blink: count for photo/SOS
            else:
                current_time = time.time()
                if current_time - last_blink_time > 0.2:  # debounce
                    blink_count += 1
                    last_blink_time = current_time
                    print(f"Blink detected ({blink_count})")

        # --- Double blink → Capture photo + send SOS ---
        if blink_count == 2 and not recording:
            image_path = capture_image()
            send_sos_alert(image_path)
            blink_count = 0

        # Reset blink count if time gap too large
        if time.time() - last_blink_time > double_blink_interval:
            blink_count = 0

        time.sleep(0.05)

except KeyboardInterrupt:
    if recording:
        stop_video()
    GPIO.cleanup()
    print("\nExiting program. GPIO cleaned up.")