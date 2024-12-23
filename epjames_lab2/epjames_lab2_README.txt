In this lab, I create an LED that changes with the potentiometer. Based on the mode, the potentiometer can either adjust the frequency 
at which the light blinks or the brightness of the LED. 

Connections:
    I have my power connected to 3.3V of the ESP32 board
    I have my ground connected to the ground of the ESP32 board
    I have my potentiometer wired up to the A2 port of the ESP32 which is pin 34 because this uses ADC1
    I then have my LED wired up through a resistor to D33 which is pin 33 becuase it also uses ADC1
    I also have my switch in the code as Pin 38 since that seems to be the default for the switch

Youtube link:
    https://www.youtube.com/watch?v=oQ9lTpmI9SA


Sample Terminal Output:
Date: 2024-10-03
Time: 03:20:30
Date: 2024-10-03
Time: 03:21:00
