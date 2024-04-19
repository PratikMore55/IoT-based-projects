import picamera
import cv2
import numpy as np
import pygame
from time import sleep
from picamera.array import PiRGBArray
from picamera import PiCamera
import pytesseract
from gtts import gTTS
import os
import telepot
import serial
import webbrowser
import sys
import RPi.GPIO as GPIO

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)  # Push button for currency detection
GPIO.setup(27, GPIO.IN)  # Push button for OCR

# Initialize the camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.rotation = 180
camera.sharpness = 60
rawCapture = PiRGBArray(camera, size=(640, 480))
# Allow the camera to warm up
#time.sleep(0.1)

def capture_image():
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 604)
        camera.start_preview()
        sleep(5)
        camera.capture()

# Function for currency detection
def currency_detection():
    capture_image('currency_image.jpg')

    if compare_images('currency_image.jpg', 'reference_currency.jpg'):
        genuine_currency = True
    else:
        genuine_currency = False

    if genuine_currency:
        #play_audio('genuine_currency.mp3')
        print("100 rupees")
    else:
        #play_audio('fake_currency.mp3')
        print("fake money")

# Function for OCR
def ocr():
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array

        text = pytesseract.image_to_string(image)
        
        # Convert text to speech
        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")

        # Play the audio
        os.system("mpg321 output.mp3")

        cv2.imshow("Frame", image)

        print(text)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q"):
            break

# Callback function for currency button press
def currency_button_callback(channel):
    print("Currency button pressed")
    currency_detection()

# Callback function for OCR button press
def ocr_button_callback(channel):
    print("OCR button pressed")
    ocr()

# Setup event listeners for button presses
GPIO.add_event_detect(17, GPIO.RISING, callback=currency_button_callback, bouncetime=1000)
GPIO.add_event_detect(27, GPIO.RISING, callback=ocr_button_callback, bouncetime=1000)

# Function for GPS Tracker
def gps_tracker():
    ser = serial.Serial("/dev/ttyAMA0")
    gpgga_info = "$GPGGA,"
    GPGGA_buffer = 0
    NMEA_buff = 0
    lat_in_degrees = 0
    long_in_degrees = 0

    try:
        while True:
            received_data = (str)(ser.readline())
            GPGGA_data_available = received_data.find(gpgga_info)
            
            if(GPGGA_data_available>0):
                GPGGA_buffer = received_data.split("$GPGGA,",1)[1]
                
                NMEA_buff = (GPGGA_buffer.split(','))
                
                GPS_Info()
                
                print("lat_in_degrees:", lat_in_degrees,"long_in_degree: ", long_in_degrees,'\n')
                
                map_link = 'https://maps.google.com/?q=' +lat_in_degrees + ',' + long_in_degrees
                
                print("Press control+c for location")
                
    except KeyboardInterrupt:
        webbrowser.open(map_link)
        sys.exit(0)

def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_latitude = 18.6567
    nmea_longitude = 73.8302
    
    print("Lat = ", nmea_latitude, "Long = ", nmea_longitude,'\n')
    
    lat = float(nmea_latitude)
    long = float(nmea_longitude)
    
    lat_in_degrees = convert_to_degrees(lat)
    long_in_degrees = convert_to_degrees(long)
    
def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value-int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f"%position
    return position

# Function for click and send
def click_and_send():
    print("About to take a picture")
    camera.capture("/home/pratik/Pictures/img.jpg")
    print("Picture taken")
    
    bot.sendPhoto(chat_id, photo=open("/home/pratik/Pictures/img.jpg", 'rb'))
    bot.sendMessage(chat_id, 'Captured Image')
    # Telegram message handling function
def handle(msg):
    global telegramText
    global chat_id
  
    chat_id = msg['chat']['id']
    telegramText = msg['text']
  
    print('Message received from ' + str(chat_id))
  
    if telegramText == '/locate':
        bot.sendMessage(chat_id, 'Obtaining Location')
        bot.sendMessage(chat_id, 'Latitude = 18.6567')
        bot.sendMessage(chat_id, 'Longitude = 73.8302')
    elif telegramText == '/capture':
        bot.sendMessage(chat_id, 'Camera is activated.')
        click_and_send()

# Initialize Telegram bot
bot = telepot.Bot('6833233141:AAGiJxczsqMckl_M9i7X5Wj_v4Q3WPty6Zs')
bot.message_loop(handle)

# Main loop
try:
    while True:
        sleep(1)  # Keep the script running

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on Ctrl+C exit
