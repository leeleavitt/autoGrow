# This is a series of functions to turn on and off the fans
# lights and solenoid valve when we get to it.
import RPi.GPIO as GPIO
import time
import datetime
from picamera import PiCamera, Color
import os

# SETTINGS = {
#     # Light Settings
#     'lightPin' : 17,
#     'lightOn' : 7,
#     'hoursOn' : 12,
#     'lightOff' : 23,

#     # Fan One settings
#     'fanOnePin' : 6,
#     'fanTwoPin': 13,
#     'fanOn' : 8,
#     'fanOff' : 8 + 12,
# }

# Function to Return the hour of day.
def timeFinder():
    return datetime.datetime.now().hour

# This function writes to my settings file
def settingWriter(SETTINGS):
    print('writing')
    print(SETTINGS)
    import json
    import os
    dir_path = os.path.dirname(os.path.abspath(__file__))
    json = json.dumps(SETTINGS)
    f = open('/home/pi/Documents/autoGrow/py/SETTINGS.json', 'w')
    f.write(json)
    f.close()

# This function reads in the settings
def settingReader():
    import json
    import os
    dir_path = os.path.dirname(os.path.abspath(__file__))
    datum = json.load(open('/home/pi/Documents/autoGrow/py/SETTINGS.json'))
    return datum

# # Function to Log Each time the Fans were switched
# def fileWriter():


# Function to look at the time, and turn the light on or off
def lightController():
    import os
    dir_path = os.path.dirname(os.path.abspath(__file__))
    print(os.path.join(dir_path,'SETTINGS.json'))

    # First check to see what time it is
    currentTime = timeFinder()
    # Read the setting file in
    SETTINGS = settingReader()

    print('Time is ', currentTime)
    # If the current time is less than the specified time, or greater than the light off time
    # then turn off the light
    if currentTime < SETTINGS['lightOn']  or currentTime >= SETTINGS['lightOff'] or SETTINGS['lightOffOverride']:
        GPIO.setup(SETTINGS['lightPin'], GPIO.OUT, initial = GPIO.LOW)
    else:
        GPIO.setup(SETTINGS['lightPin'], GPIO.OUT, initial = GPIO.HIGH)

# Function that runs the fan automatically every morning
def fanManager():
    # First check to see what time it is
    currentTime = timeFinder()
    # Read the setting file in
    SETTINGS = settingReader()

    # LOGIC SERIES
    # Are they operating within time ranges
    # Have we Over ridden the fan?
    # WHat are the current fan settings

    # for i in range(len(SETTINGS['fanPins'])):
    #     print(GPIO.input(SETTINGS['fanPins'][i]))

    if currentTime < SETTINGS['lightOn']  or currentTime >= SETTINGS['lightOff'] or SETTINGS['fanOffOverride']:
        print('hi')
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

def imageTaker():
    SETTINGS = settingReader()
    currentTime = timeFinder()
    if currentTime < SETTINGS['lightOn']  or currentTime >= SETTINGS['lightOff']:
        print('hello')
    else:
        camera = PiCamera()

        dir = os.path.dirname(__file__)

        camera.resolution = (1296,972)
        camera.framerate = 15
        dateAndTime = datetime.datetime.now()
        fileDateAndTime = dateAndTime.strftime("%Y%m%d_%H%M")
        imageDateAndTime = dateAndTime.strftime("%m-%d-%Y_%H:%M")

        imageName = '/home/pi/Documents/autoGrow/growPics/'+fileDateAndTime+'image.png'
        camera.start_preview()
        camera.awb_mode = 'tungsten'
        camera.annotate_foreground = Color('black')
        camera.annotate_text_size = 30
        camera.annotate_text = imageDateAndTime
        camera.rotation = 180
        time.sleep(5)
        camera.capture(imageName)

        camera.stop_preview()


# Run the functions at each script call within the cron job
if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    #GPIO.cleanup()
    lightController()
    fanManager()
    imageTaker()


