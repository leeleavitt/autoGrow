# This is a series of functions to turn on and off the fans
# lights and solenoid valve when we get to it.
import RPi.GPIO as GPIO
import time
import datetime

SETTINGS = {
    # Light Settings
    'lightPin' : 17,
    'lightOn' : 8,
    'hoursOn' : 12,
    'lightOff' : 8 + 12,

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
    # If the current time is less than the specified time, or greater than the light off time
    # then turn off the light
    if currentTime <= SETTINGS['lightOn']  or currentTime >= SETTINGS['lightOff']:
        GPIO.setup(SETTINGS['lightPin'], GPIO.OUT, initial = GPIO.LOW)
    else:
        print('fuck you')
        GPIO.setup(SETTINGS['lightPin'], GPIO.OUT, initial = GPIO.HIGH)

lightController()
# Function to run the two fans and alternate each direction
# Basically I want to run the fans alternating each hour
def fanController():
    currentTime = timeFinder()

    if currentTime < SETTINGS['fanOn'] or currentTime > SETTINGS['fanOff']:




# Run the functions at each script call within the cron job
if __name__ == '__main__':
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        lightController()
    except:
        GPIO.cleanup()

