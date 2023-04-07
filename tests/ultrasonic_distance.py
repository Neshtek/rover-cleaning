import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO1_TRIGGER = 7
GPIO1_ECHO = 8
GPIO.setup(GPIO1_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO1_ECHO, GPIO.IN)

def distance(GPIO_TRIGGER, GPIO_ECHO):
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist1 = distance(GPIO1_TRIGGER, GPIO1_ECHO)
            print ("Measured Distance 1 = %.1f cm" % dist1)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
