import network
import ntptime
from machine import RTC, Timer, TouchPad, Pin, deepsleep, wake_reason, reset_cause, DEEPSLEEP_RESET
from time import sleep
from neopixel import NeoPixel
from esp32 import wake_on_ext0, WAKEUP_ANY_HIGH
import socket
import esp32



red_led = Pin(13, Pin.OUT) #Connect red led which is pin 13

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
    print('IP Address: ', wlan.ifconfig()[0]) #Might need to be wlan.ipcon
    
    
    
# Global variables
temp = esp32.raw_temperature() # measure temperature sensor data
hall = esp32.hall_sensor() # measure hall sensor data
red_led_state = "ON" if red_led.value() else "OFF" # string, check state of red led, ON or OFF


def web_page():
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    temp, hall, red_led_state
    """
    
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h1 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>ESP32 WEB Server</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    RED LED Current State: <strong>""" + red_led_state + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p>
    <a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    </body>
    </html>"""
    return html_webpage




#Find value of temp sensor, hall sensor and state of red LED
def valueFinder(tim1): 
    global temp, hall, red_led_state
    temp = esp32.raw_temperature()
    hall = esp32.hall_sensor()
    if red_led.value() == 1: #If on
        red_led_state = "ON"
    else: #If off
        red_led_state = "OFF"
 
addr = socket.getaddrinfo('192.168.4.82', 80)[0][-1] #My IP ADDY
s = socket.socket()
s.bind(addr)
s.listen(1) #Enable listening on sepcified port
 
            
            
wifiConnect() #Call the wifi connect funtion            
tim1 = Timer(0)
tim1.init(period=50, mode=Timer.PERIODIC, callback=valueFinder)

while True:
    connect, addr = s.accept() #Wait for client to connect to server
    request = str(connect.recv(1024)) #reads 1024 bytes of data
    #Check button
    red_led_off = request.find('/?red_led=off') #request to off
    red_led_on = request.find('/?red_led=on') #request to on
    if red_led_off == 6:
        red_led.off()
        red_led_state = "OFF"
    if red_led_on == 6:
        red_led.on()
        red_led_state = "ON"
        
    response_back = web_page()
    
    connect.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n') #ends an HTTP response header TA HELP
    connect.sendall(response_back)
    connect.close()
    
    
