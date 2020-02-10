from picamera import PiCamera, Color
import RPi.GPIO as GPIO
import os, time
import datetime

def imageTaker():
    GPIO.setmode(GPIO.BCM)
    # camera = PiCamera()
    # dir = os.path.dirname(__file__)

    # camera.resolution = (2592,1944)
    # camera.framerate = 15
    # dateAndTime = datetime.datetime.now()
    # dateAndTime = dateAndTime.strftime("%m/%d/%Y %H:%M:%S")
    camera = PiCamera()
    GPIO.setup(26, GPIO.OUT, initial = GPIO.LOW)
    time.sleep(5)

    for effect in camera.AWB_MODES:
        print(effect)
        camera.resolution = (2592,1944)
        camera.framerate = 15
        dateAndTime = datetime.datetime.now()
        dateAndTime = dateAndTime.strftime("%m/%d/%Y %H:%M:%S")

        imageName = '/home/pi/Documents/autoGrow/growPics/imageTroubleShoot/'+effect+'image.png'
        camera.start_preview()
        camera.awb_mode = effect
        camera.annotate_foreground = Color('black')
        camera.annotate_text_size = 60
        camera.annotate_text = dateAndTime
        camera.rotation = 180
        time.sleep(5)
        camera.capture(imageName)
        camera.stop_preview()
        #time.sleep(5)

    GPIO.setup(26, GPIO.OUT, initial = GPIO.HIGH)


imageTaker()