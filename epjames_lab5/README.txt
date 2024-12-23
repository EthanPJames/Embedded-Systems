My system allows for an alarm to activate if the device senses motion when it is activate

Hardware Connections:
    - Pin 14 is connected to SCL
    - SDA Pin is connected to the SDA Pin
    - Ground is connected to Ground
    - 3V is connected to Vin
    - LED is Pin 13

Software Connections: 
    - Applet 1 is an applet that delivers a post request to allow notifications once "OK google activate sensor" is said
    - Applet 2 is a webhooks applet that delivers notifications via the IFTT app once motion is detected
    - Applet 3 is an applet that delivers a post request to deactivate the device once "Ok google activate deactivate" is said

ThingstoSpeak:
    - Channel Called google sensor deactivate
    - Field one contains data for sensor_state

Extra notes:
    - I ended up not requiring mpu6050.py as I just copied the class into motion_detector.py script

Video Link:
    https://www.youtube.com/watch?v=GETsOgDmFEo
    