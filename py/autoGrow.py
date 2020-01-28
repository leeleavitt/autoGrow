# This is a series of functions to turn on and off the fans
# lights and solenoid valve when we get to it.
import RPi.GPIO as GPIO
import time
import datetime

SETTINGS = {
    # Light Settings
    'lightPin' : 17,
    'lightOn' : 7,
    'hoursOn' : 12,
    'lightOff' : 18,

    # Fan One settings
    'fanOnePin' : 6,
    'fanTwoPin': 13,
    'fanOn' : 8,
    'fanOff' : 8 + 12,
}

# Function to Return the hour of day.
def timeFinder():
    return datetime.datetime.now().hour

# Function to look at the time, and turn the light on or off
def lightController():
    currentTime = timeFinder()
    print('Time is ', currentTime)
    # If the current time is less than the specified time, or greater than the light off time
    # then turn off the light
    if currentTime < SETTINGS['lightOn']  or currentTime >= SETTINGS['lightOff']:
        GPIO.setup(SETTINGS['lightPin'], GPIO.OUT, initial = GPIO.LOW)
    else:
        GPIO.setup(SETTINGS['lightPin'], GPIO.OUT, initial = GPIO.HIGH)

# This function writes to my settings file
def settingWriter(SETTINGS):
    print('writing')
    print(SETTINGS)
    import json
    json = json.dumps(SETTINGS)
    f = open('SETTINGS.json', 'w')
    f.write(json)
    f.close()

# This function reads in the settings
def settingReader():
    import json
    datum = json.load(open('SETTINGS.json'))
    return datum

# Function that runs the fan automatically every morning
def fanManager():
    # First check to see what time it is
    currentTime = timeFinder()
    # Read the setting file in
    SETTINGS = settingReader()

    # First Make sure this operates within operating hours
    if currentTime < SETTINGS['lightOn']  or currentTime >= SETTINGS['lightOff']:
        GPIO.setup(SETTINGS['fanPins'], GPIO.OUT, initial=GPIO.HIGH)
    else:
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




    
# Run the functions at each script call within the cron job
if __name__ == '__main__':
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        lightController()
        fanManager()
    except:
        GPIO.cleanup()

