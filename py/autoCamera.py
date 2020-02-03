from picamera import PiCamera, Color
import os, time
import datetime

def imageTaker():
    # camera = PiCamera()
    # dir = os.path.dirname(__file__)

    # camera.resolution = (2592,1944)
    # camera.framerate = 15
    # dateAndTime = datetime.datetime.now()
    # dateAndTime = dateAndTime.strftime("%m/%d/%Y %H:%M:%S")
    camera = PiCamera()

    for effect in camera.AWB_MODES:
        dir = os.path.dirname(__file__)

        camera.resolution = (2592,1944)
        camera.framerate = 15
        dateAndTime = datetime.datetime.now()
        dateAndTime = dateAndTime.strftime("%m/%d/%Y %H:%M:%S")

        imageName = './growPics/'+effect+'image.png'
        camera.start_preview()
        camera.awb_mode = effect
        camera.annotate_foreground = Color('black')
        camera.annotate_text_size = 60
        camera.annotate_text = dateAndTime
        time.sleep(5)
        camera.capture(os.path.join(dir, imageName))
        camera.stop_preview()
        time.sleep(20)

imageTaker()