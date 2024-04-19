import serial
from time import sleep
import webbrowser
import sys
#import os

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
