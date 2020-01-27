import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pins = [17, 13, 6, 5 ]
pinDesc = ["Light", "Fan Right", "Fan Left", "Solenoid"]
pinTime = [5, 7, 7, 5 ]

GPIO.setup(pins[0], GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(pins[1:], GPIO.OUT, initial=GPIO.HIGH)
time.sleep(5)


for i in range(len(pins)):

    print('pin # ', pins[i], ' is ', pinDesc[i])
    print('Turning on for ', pinTime[i], ' seconds\n')
    currentGPIO = GPIO.input(pins[i])
    GPIO.output(pins[i], not currentGPIO)
    
    time.sleep(pinTime[i])
    currentGPIO = GPIO.input(pins[i])
    GPIO.output(pins[i], not currentGPIO)

GPIO.cleanup()


##########
#TESTING
##########
import json
json = json.dumps(SETTINGS)
f = open('SETTINGS.json', 'w')
f.write(json)
f.close()

import json
datum = json.load(open('SETTINGS.json'))