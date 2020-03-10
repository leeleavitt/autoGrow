# This is a series of functions to turn on and off the fans
# lights and solenoid valve when we get to it.
import RPi.GPIO as GPIO
import time
import datetime
from picamera import PiCamera, Color
import os

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
    #dir_path = os.path.dirname(os.path.abspath(__file__))
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
# Function that runs the fan automatically every morning
def fanManager2():
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
    
    # This is added functionality to add automating the fans
    # Load in the settings
    fanTime = SETTINGS['fanTime']
    fanLogic = [] #intitialize an empty list
    #Loop through each time setting and find if the condition holds
    for i in range(len(fanTime)):
        fanLogic.append(fanTime[i][0] <= currentTime < fanTime[i][1])
    
    print(fanLogic)

    if not any(fanLogic):
        print('fans off')
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
    '''
    This shows the resolution settings to use
    https://picamera.readthedocs.io/en/release-1.12/fov.html
    '''
    SETTINGS = settingReader()
    currentTime = timeFinder()
    if currentTime < SETTINGS['lightOn']  or currentTime >= SETTINGS['lightOff']:
        print('hello')
    else:
        #Turn on the LED and turn off the grow light for better Image, 
        GPIO.setup((26,17), GPIO.OUT, initial = GPIO.LOW)

        #Start making names for the image and the file name
        dateAndTime = datetime.datetime.now()
        fileDateAndTime = dateAndTime.strftime("%Y%m%d_%H%M")
        imageDateAndTime = dateAndTime.strftime("%m-%d-%Y_%H:%M")
        imageName = '/home/pi/Documents/autoGrow/growPics/'+fileDateAndTime+'image.png'

        with PiCamera() as camera:
            camera.resolution = (1640,1232)
            camera.framerate = 15
            camera.awb_mode = 'auto'
            camera.annotate_foreground = Color('black')
            camera.annotate_text_size = 30
            camera.annotate_text = imageDateAndTime
            camera.rotation = 180
            camera.start_preview()
            time.sleep(2)
            camera.capture(imageName)
            camera.stop_preview()
        # Now Turn off the LED and turn back on the grow light
        GPIO.setup((26,17), GPIO.OUT, initial = GPIO.HIGH)

def prettyLighter(input = 'on'):
    if(input == 'on'):
        GPIO.setup((26,17), GPIO.OUT, initial = GPIO.LOW)
    elif(input == 'off'):
        GPIO.setup((26,17), GPIO.OUT, initial = GPIO.HIGH)

def dataMaker():
    import sys
    import Adafruit_DHT
    import csv
    import datetime

    # import the settings
    SETTINGS = settingReader()
    # Read the Sensor
    humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302,SETTINGS['sensorPins'][0])
    #convert temp to farenheit
    temp = round(temp * (9/5) + 32,2)
    humidity = round(humidity,2)

    # Get the date and time
    current = datetime.datetime.now()
    date = current.strftime("%Y%m%d")
    time = current.strftime("%H%M")

    with open('/home/pi/Documents/autoGrow/data/tempHumidData.csv', "a+") as f:
        fileWriter = csv.writer(f, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
        fileWriter.writerow([date, time, temp, humidity])





# Run the functions at each script call within the cron job
if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    lightController()
    fanManager2()
    #prettyLighter('off')
    #imageTaker()
    dataMaker()




