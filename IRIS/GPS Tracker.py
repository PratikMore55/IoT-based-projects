import serial
from time import sleep
import webbrowser
import sys
import telepot
from telepot.loop import MessageLoop
#import os

def handle(msg):
    global telegramText
    global chat_id
  
    chat_id = msg['chat']['id']
    telegramText = msg['text']
  
    print('Message received from ' + str(chat_id))
  
    if telegramText == '/locate':
        bot.sendMessage(chat_id, 'Obtaining Location')
        
        #bot.sendMessage(chat_id)
        #bot.sendMessage(chat_id, 'Latitude = xxxxx')   # for tesing purpose
        #bot.sendMessage(chat_id)
        #bot.sendMessage(chat_id, 'Longitude = xxxxx')       # for tesing purpose
        
        #bot.sendMessage(chat_id)
        #print("GPS_Info()")
        #bot.sendMessage(chat_id, print(GPS_Info()))

    while True:
        GPS_Info()
        #convert_to_degrees(raw_value)
    
           

bot = telepot.Bot('Telegram Bot ID')
bot.message_loop(handle)   

def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude =[]
    nmea_time = NMEA_buff[0]
    nmea_latitude = NMEA_buff[1]
    nmea_longitude = NMEA_buff[3]
    
    nmea_latitude = 18.6229
    nmea_longitude = 73.8161
    
    print(nmea_time,'\n')
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

gpgga_info = "$GPGGA,"
ser = serial.Serial("/dev/ttyAMA0")         # write ttyAMAO or ttyS0 after searching into the files
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
            
            print("press control+c for location")
            
except KeyboardInterrupt:
    webbrowser.open(map_link)
    sys.exit(0)
