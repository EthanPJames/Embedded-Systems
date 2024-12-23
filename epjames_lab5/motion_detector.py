from machine import Timer, RTC, TouchPad, deepsleep, SoftI2C, Pin
from neopixel import NeoPixel
import machine
import network
import ntptime
import time
from time import sleep
import utime
import socket
import esp32
import urequests
import network
#import requests
import json

#Include class import given to us
class MPU:
    # Static MPU memory addresses
    ACC_X = 0x3B
    ACC_Y = 0x3D
    ACC_Z = 0x3F
    TEMP = 0x41
    GYRO_X = 0x43
    GYRO_Y = 0x45
    GYRO_Z = 0x47

    def acceleration(self):
        self.i2c.start()
        acc_x = self.i2c.readfrom_mem(self.addr, MPU.ACC_X, 2)
        acc_y = self.i2c.readfrom_mem(self.addr, MPU.ACC_Y, 2)
        acc_z = self.i2c.readfrom_mem(self.addr, MPU.ACC_Z, 2)
        self.i2c.stop()

        # Accelerometer by default is set to 2g sensitivity setting
        # 1g = 9.81 m/s^2 = 16384 according to mpu datasheet
        acc_x = self.__bytes_to_int(acc_x) / 16384 * 9.81
        acc_y = self.__bytes_to_int(acc_y) / 16384 * 9.81
        acc_z = self.__bytes_to_int(acc_z) / 16384 * 9.81

        return acc_x, acc_y, acc_z

    def temperature(self):
        self.i2c.start()
        temp = self.i2c.readfrom_mem(self.addr, self.TEMP, 2)
        self.i2c.stop()

        temp = self.__bytes_to_int(temp)
        return self.__celsius_to_fahrenheit(temp / 340 + 36.53)
    
    def gyro(self):
        return self.pitch, self.roll, self.yaw

    def __init_gyro(self):
        # MPU must be stationary
        gyro_offsets = self.__read_gyro()
        self.pitch_offset = gyro_offsets[1]
        self.roll_offset = gyro_offsets[0]
        self.yaw_offset = gyro_offsets[2]

    def __read_gyro(self):
        self.i2c.start()
        gyro_x = self.i2c.readfrom_mem(self.addr, MPU.GYRO_X, 2)
        gyro_y = self.i2c.readfrom_mem(self.addr, MPU.GYRO_Y, 2)
        gyro_z = self.i2c.readfrom_mem(self.addr, MPU.GYRO_Z, 2)
        self.i2c.stop()

        # Gyro by default is set to 250 deg/sec sensitivity
        # Gyro register values return angular velocity
        # We must first scale and integrate these angular velocities over time before updating current pitch/roll/yaw
        # This method will be called every 100ms...
        gyro_x = self.__bytes_to_int(gyro_x) / 131 * 0.1
        gyro_y = self.__bytes_to_int(gyro_y) / 131 * 0.1
        gyro_z = self.__bytes_to_int(gyro_z) / 131 * 0.1

        return gyro_x, gyro_y, gyro_z
    
    def __update_gyro(self, timer):
        gyro_val = self.__read_gyro()
        self.pitch += gyro_val[1] - self.pitch_offset
        self.roll += gyro_val[0] - self.roll_offset
        self.yaw += gyro_val[2] - self.yaw_offset

    @staticmethod
    def __celsius_to_fahrenheit(temp):
        return temp * 9 / 5 + 32

    @staticmethod
    def __bytes_to_int(data):
        # Int range of any register: [-32768, +32767]
        # Must determine signing of int
        if not data[0] & 0x80:
            return data[0] << 8 | data[1]
        return -(((data[0] ^ 0xFF) << 8) | (data[1] ^ 0xFF) + 1)

    def __init__(self, i2c):
        # Init MPU
        self.i2c = i2c
        self.addr = i2c.scan()[0]
        self.i2c.start()
        self.i2c.writeto(0x68, bytearray([107,0]))
        self.i2c.stop()
        print('Initialized MPU6050.')

    # Gyro values will be updated every 100ms after creation of MPU object
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.pitch_offset = 0
        self.roll_offset = 0
        self.yaw_offset = 0
        self.__init_gyro()
        gyro_timer = Timer(3)
        gyro_timer.init(mode=Timer.PERIODIC, callback=self.__update_gyro, period=100)
        
#Begin code that utilizes the class
movement = 0
prev = 0
on = False
notify = 0
timed_out = 0

LED = Pin(13, Pin.OUT)
LED.off()
led_np = Pin(0, Pin.OUT)
led_power = Pin(2, Pin.OUT)
led_power.value(1)
np = NeoPixel(led_np, 1)
i2c = SoftI2C(sda=Pin(22), scl=Pin(14))
mpu = MPU(i2c)


#Connect to WIFI
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
    print('IP Address: ', wlan.ifconfig()[0]) 
    
def calibrate():
    xcal, ycal, zcal = mpu.acceleration()
#     print(f"Xcal value: {xcal}")
#     print(f"Ycal value: {ycal}")
#     print(f"Zcal value: {zcal}")
    print("Done Calibrating")
    return(xcal, ycal, zcal)
xoff, yoff, zoff = calibrate() #Might need to be a global value
    
def read(timer):
    global movement
    global prev
    global on
    global notify
    global timed_out
    print("Reading from thingtospeak")
    #Need to fix, why does my last entry ID not increment??????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
    message = urequests.get('https://api.thingspeak.com/channels/2757466/feeds.json?api_key=27IE4EK001NZXYT3&results=1') #Intially had at 2
    message_data = message.json() #This is my copy that works: json.loads(message.content)
    print(message_data)

    
    
    req = message_data.get("feeds", [])
    print(req)
    if req:
        field_value = int(req[-1].get("field1", 0))
        toggle(field_value)
    else:
        print("No data\n")
activation = False
check_motion_timer = Timer(1)

#Function to activate or deactivate system
def toggle(state):
    global activation
    
    if state == 1 and not activation:
        print("Activating System")
        activation = True
        np[0] = (0,255,0,)
        np.write()
        check_motion_timer.init(period = 1000, mode=Timer.PERIODIC, callback=motion_check)
    elif state == 0 and activation:
        print("Deactivating System")
        activation = False
        np[0] = (0,0,0,)
        np.write()
        LED.off()
        check_motion_timer.deinit()
    else:
        print("System inactive")

def motion_check(timer):
    x,y,z = mpu.acceleration()
    if((x + xoff > 2) or (x + xoff < -3) or (y + yoff > 2) or (y + yoff < -2) or (z + zoff > 16) or (z + zoff < -16) and notify):
        print("Motion detected")
        LED.on()
        response = urequests.post('https://maker.ifttt.com/trigger/movement/with/key/d-8JicSBRXhJKB3DAmYKNx')
        response.close()
    else:
        LED.off()
    

       
wifiConnect()    
    
#Beign Timer calls
timer0 = Timer(0)
timer0.init(period=30000, mode=Timer.PERIODIC, callback=read)


 

while(True):
    pass
    
#Code issues:
    #Not turning on the Neopixel when I say activate
    #Not sending data to thingtospeak correctly
    #Does not deactivate correctly, can I just say it twice?


    #Might need to change to post
