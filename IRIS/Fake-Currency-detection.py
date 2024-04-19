import picamera
import cv2
import numpy as np
import pygame
from time import sleep

def capture_image(filename):
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 604)
        camera.start_preview()
        sleep(5)
        camera.capture(filename)

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)
    return equalized

def compare_images(image1, image2):
    img1 = cv2.imread(image1)
    img2 = cv2.imread(image2)
    
    img1_eq = preprocess_image(img1)
    img2_eq = preprocess_image(img2)
    
    hist1 = cv2.calcHist([img1_eq], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([img2_eq], [0], None, [256], [0, 256])
    
    # Compare histograms using Chi-Squared distance
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)
    print("Histogram Similarity:", similarity)
    
    if similarity < 10000000:
        return True
    else:
        return False

def play_audio(message):
    pygame.mixer.init()
    pygame.mixer.music.load(message)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def main():
    capture_image('currency_image.jpg')

    if compare_images('currency_image.jpg', 'reference_currency.jpg'):
        genuine_currency = True
    else:
        genuine_currency = False

    if genuine_currency:
        #play_audio('genuine_currency.mp3')
        print("Genuine money")
    else:
        #play_audio('fake_currency.mp3')
        print("fake money")

if __name__ == "__main__":
    main()
    
