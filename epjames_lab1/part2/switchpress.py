from machine import Pin
from neopixel import NeoPixel
from time import sleep


led = Pin(0, Pin.OUT) #Set pin 0 as output
power = Pin(2, Pin.OUT) #Set the power
power.value(1) #turns on RGB LED #
NP = NeoPixel(led, 1) #Controls neopixel using pin 0, using only 1 LED
switch = Pin(38, Pin.IN) #Set my switch button

index = 0
while index < 5:
    if switch() == 0: #If swtich is pressed
        NP[0] = (0, 255, 0) #Set color to green if button is being pressed
        NP.write() #Input new color
        index = index + 1
        sleep(0.5)
    else:           
        NP[0] = (255, 0, 0) #Set color to red if button not being pressed
        NP.write()
        
NP[0] = (0, 0, 0) #Turn off the LED
NP.write()
print("You have successfully implemented LAB1!")



    