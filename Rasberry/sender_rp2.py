import RPi.GPIO as GPIO
from time import sleep

pin = 14  
GPIO.setmode(GPIO.BCM)

GPIO.setup(pin, GPIO.OUT)  

try:
    while True:
        GPIO.output(pin, GPIO.HIGH)  
        print("HIGH")
        sleep(2)
        GPIO.output(pin, GPIO.LOW)   
        print("LOW")
        sleep(2)

except KeyboardInterrupt:
    print("Przerwano przez użytkownika")

finally:
    GPIO.cleanup()  
