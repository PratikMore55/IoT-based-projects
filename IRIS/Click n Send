import telepot
from picamera import PiCamera
import time

picamera = PiCamera()
picamera.resolution = (640, 480)
picamera.framerate = 25

def handle(msg):
    global chat_id
    chat_id = msg['chat']['id']
    telegramText = msg['text']

    print('Message received from ' + str(chat_id))

    if telegramText == '/capture':
        bot.sendMessage(chat_id, 'Camera is activated.')
        main()

def main():
    global chat_id

    print("About to take a picture")
    picamera.capture("/home/pratik/Pictures/img.jpg")
    print("Picture taken")

    bot.sendPhoto(chat_id, photo=open("/home/pratik/Pictures/img.jpg", 'rb'))
    bot.sendMessage(chat_id, 'Captured Image')

bot = telepot.Bot('TELEGRAM BOT ID')
bot.message_loop(handle)

while True:
    time.sleep(10)
