import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT, initial  = GPIO.HIGH)