import network
import ntptime
from machine import RTC, Timer, TouchPad, Pin, deepsleep, wake_reason, reset_cause, DEEPSLEEP_RESET
from time import sleep
from neopixel import NeoPixel
from esp32 import wake_on_ext0, WAKEUP_ANY_HIGH
import esp32
import time
import urequests




# Wifi Setup, will need to eventually fill these values with wifi at the house
SSID = 'Senior House'
PASSWORD = 'Catfished'

# Connect to the WIFI *Pulled straight from documentation
def wifiConnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f'Connecting to SSID: {SSID}')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    print('Connected->True:', SSID)
    print('IP Address: ', wlan.ifconfig()[0]) #Might need to be wlan.ipconfig('addr4')???????????????????????????????????
    
    
# ThingSpeak API & URL
HTTP_HEADERS = {'Content-Type': 'application/json'} 
WRITE_API_KEY = '11943MW6RVVPEE64'


#Measure Fnction
def measureSensor(tim1):
    temp = esp32.raw_temperature()
    hall = esp32.hall_sensor()
    print("Temperature: ", temp)
    print("Hall Sensor: ", hall)
    thingSpeak(temp, hall)

def thingSpeak(temperature, hall):
    variables = {'field1' : temperature, 'field2': hall}
    request = urequests.post( 'http://api.thingspeak.com/update?api_key=' + WRITE_API_KEY, json = variables, headers = HTTP_HEADERS )  #Might need to alter
    request.close()

#Function Calls
wifiConnect()

tim1 = Timer(0)
tim1.init(period = 30000, mode = Timer.PERIODIC, callback = measureSensor)

time.sleep(300)
tim1.deinit()