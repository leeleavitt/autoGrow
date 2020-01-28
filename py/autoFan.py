# This is a series of functions to turn on and off the fans
# To alternate fans I am deciding to 
# 1 keep track of a setting as to which fan was last on
# 2 alternate the fans one on one off per hour

import RPi.GPIO as GPIO
import time
import datetime

# Function to Return the hour of day.
def timeFinder():
    return datetime.datetime.now().minute

def settingWriter(SETTINGS):
    print('writing')
    print(SETTINGS)
    import json
    json = json.dumps(SETTINGS)
    f = open('SETTINGS.json', 'w')
    f.write(json)
    f.close()

def settingReader():
    import json
    datum = json.load(open('SETTINGS.json'))
    return datum

def fanManager():
    # First check to see what time it is
    currentTime = timeFinder()
    # Read the setting file in
    SETTINGS = settingReader()

    # If the current time is not equal to settings current Time
    # Change the current time
    if currentTime != SETTINGS['currentTime']:
        # Change the setting to the time that it doesn't match
        SETTINGS['currentTime'] = currentTime
        print(SETTINGS['currentTime'])
        # First Turn off the Other fan
        GPIO.setup(SETTINGS['fanPins'][ SETTINGS['currentFanIndex'] ], GPIO.OUT, initial=GPIO.HIGH)
        # Change the fan index
        SETTINGS['currentFanIndex'] = int(not SETTINGS['currentFanIndex'])
        print(SETTINGS['currentFanIndex'])
        # save the setting
        settingWriter(SETTINGS)
        #Now turn on the correct fan
        GPIO.setup(SETTINGS['fanPins'][ SETTINGS['currentFanIndex'] ], GPIO.OUT, initial=GPIO.LOW)

    
    
if __name__ == '__main__':
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        #fanManager()
        GPIO.cleanup()

    except:
        GPIO.cleanup()

   

