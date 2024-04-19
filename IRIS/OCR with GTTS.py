import time
import RPi.GPIO as GPIO
import pytesseract
import pyttsx3
import cv2

engine = pyttsx3.init()

GPIO.setmode(GPIO.BCM)

TRIG = 2
ECHO = 3
BUZZER = 17

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)

GPIO.output(TRIG, False)
print("Starting...")
time.sleep(2)

def read_text(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    print("Recognized text: ")
    print(text)

    engine.say(text)
    engine.runAndWait()
    distance = measure_distance()
    print("Distance: ", distance, "cm")
    if distance <= 10:
        print("Obstacle")
        GPIO.output(Buzzer, GPIO.HIGH)
        time.sleep(2)
    else:
        print("naa")
        GPIO.output(BUZZER, GPIO.LOW)

def capture_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow("Smart Glasses", frame)

        if cv2.waitKey(1) & 0xFF == ord('g'):
            break

        read_text(frame)
    cap.release()
    cv2.destroyAllWindows()

def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_stop = time.time()

    pulse_time = pulse_stop - pulse_start
    distance = pulse_time * 17150
    return round(distance, 2)

try:
    while True:
        capture_frames()

except KeyboardInterrupt:
    print("Measurement stopped by user")
