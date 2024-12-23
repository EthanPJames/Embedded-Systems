import machine
from machine import Pin, RTC, Timer, PWM, ADC

year = int(input("Year? "))
month = int(input("Month? ")) #1-12 with 1 being january and 12 being december
day = int(input("Day? "))
weekday = int(input("Weekday? ")) #0 is monday and 6 is sunday
hour = int(input("Hour? "))
minute = int(input("Minute? "))
second = int(input("Second? "))
m_second = int(input("Microsecond? "))

clock = machine.RTC()
clock.datetime((year, month, day, weekday, hour, minute, second, m_second))

#Display the date correctly
def display_datetime(timer):
    current_datetime = clock.datetime()
    formatted_date = f"Date: {current_datetime[0]:04}-{current_datetime[1]:02}-{current_datetime[2]:02}"
    formatted_time = f"Time: {current_datetime[4]:02}:{current_datetime[5]:02}:{current_datetime[6]:02}"
    print(f"{formatted_date}\n{formatted_time}")

#Hardware timer setup to call display current time every 30 seconds using doc.micropython.org/timers
timer = Timer(0) 
timer.init(period = 30000, mode = Timer.PERIODIC, callback = display_datetime) #Set timer for every 30 seconds

#Toggle between various modes as per the lab document
def switch_press(x):
    #Pressing switch button to switch between frequency and duty cycle
    global frequency_mode
    global press_one
    frequency_mode = not frequency_mode #Ta help
    press_one = False #TA help
    
def potentiometerReader(y):
    #Read potentiometer every 100 ms
    global frequency_mode
    global press_one
    potentiometer_val = adc.read_u16() #From manual to read analog value, range from 0 to 65535
    if(False if press_one else True): #Help
        if(frequency_mode):
            newF = int(1 + potentiometer_val * 50/65535) #Max analog range, how do we get this equation??????, make it so new frequency is 1-51%, 4096
            led_light.freq(newF)
        else:
            duty_new = int(1 + int(potentiometer_val * 50 /65535)) #How do we get this equation????????, make it so new duty cycle is 1-51%, 4096
            led_light.duty(duty_new)
            
#Set all Pin values for ADC and Switching Pins and LED Pins
pin_out = Pin(34, Pin.IN)
adc = ADC(pin_out)
switch = Pin(38, Pin.IN)
switch.irq(trigger=Pin.IRQ_FALLING, handler=switch_press)
led_light = machine.PWM(Pin(33,Pin.OUT), freq = 10, duty = 512)

#Set my initial presses and Modes
frequency_mode = False
press_one = True
analog_clock = Timer(1) #Assign timer ID
analog_clock.init(mode=Timer.PERIODIC, period=100, callback=potentiometerReader) #Intialzie analog clock to read every 100ms






 