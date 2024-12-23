import network
import ntptime
from machine import RTC, Timer, TouchPad, Pin, deepsleep, wake_reason, reset_cause, DEEPSLEEP_RESET
from time import sleep
from neopixel import NeoPixel
from esp32 import wake_on_ext0, WAKEUP_ANY_HIGH

# if wake_reason() == 2:
#     print("Woke up due to EXT0 wake-up.")
# elif wake_reason() == 4:
#     print('Woke up due to timer wake-up')
# else:
#     pass

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
    
# Get current Date and Time using NTP to set the RTC
def dateTimeFetch(tim):
    if rtc.datetime()[4] < 4:
        print('Date: {:02}/{:02}/{:4}'.format(rtc.datetime()[1], rtc.datetime()[2]-1, rtc.datetime()[0]))
        print('Time: {:02}:{:02}:{:02} HRS'.format((rtc.datetime()[4]+20), rtc.datetime()[5], rtc.datetime()[6]))
    else:
        print('Date: {:02}/{:02}/{:4}'.format(rtc.datetime()[1], rtc.datetime()[2], rtc.datetime()[0]))
        print('Time: {:02}:{:02}:{:02} HRS'.format(rtc.datetime()[4]-4, rtc.datetime()[5], rtc.datetime()[6]))

#Set up Neo Pixel control by touch
def touchInput(touch_tim):
    touch_output = touch.read() #Read touch pin
    if touch_output < 600: #How do we get this value???????????????????????????????????????????????????????????????????????????
        np[0] = (0,50,0) #Green on, might need to reduce value?????????????????????????????????????????????????????????????????
        np.write()
    else:
        np[0] = (0,0,0) #Nothing on
        np.write()
    
    
#Sleep Timer
def sleepTimer(red_tim):
    print("I am going to sleep for one minute")
    led.off() #turn off the LED when asleep
    deepsleep(60000)  # Put device to sleep for one minute
    led.on()

if wake_reason() == 2:
    print("Woke up due to EXT0 wake-up.")
elif wake_reason() == 4:
    print('Woke up due to timer wake-up')
else:
    pass
    



#Setup My Pins
touch = TouchPad(Pin(14))
led = Pin(13, Pin.OUT)
led.on() #LED on
np_on = Pin(2, Pin.OUT)
np_on.value(1) #On
button = Pin(37, Pin.IN)
temp_for_np = Pin(0, Pin.OUT)
np = NeoPixel(temp_for_np, 1) #Set pin 0 for 1 pixel
wake_on_ext0(button, WAKEUP_ANY_HIGH)

#Setup and Call all the Functions I wrote
wifiConnect() #Function I wrote
rtc = RTC() #From imports
ntptime.settime()

#Set timer to update every 15 sec for RTC
tim = Timer(0)
tim.init(mode=Timer.PERIODIC, period = 15000, callback=dateTimeFetch)

#Set time to update every 50 sec for touch
touch_tim = Timer(1)
touch_tim.init(mode=Timer.PERIODIC, period = 50, callback=touchInput)

#Set time to update for sleep mode using LED
red_tim = Timer(2)
red_tim.init(mode=Timer.PERIODIC, period = 30000, callback=sleepTimer) #Call function every 30 seconds becuase that is how long it is awake
             

while True:
    pass
    


