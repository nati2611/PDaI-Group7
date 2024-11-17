import RPi.GPIO as GPIO
from time import sleep

flag = 1
button_pin = 14 
GPIO.setmode(GPIO.BCM)

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
   
        if GPIO.input(button_pin) == GPIO.HIGH:
                flag +=1
                if flag % 2:
                    print("hello")
                else:
                    print(" HELLO")
        sleep(0.3)
        
except KeyboardInterrupt:
    print("Przerwano przez użytkownika")

finally:
    GPIO.cleanup()
