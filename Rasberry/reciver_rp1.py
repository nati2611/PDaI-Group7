import RPi.GPIO as GPIO
import time

wait = 1
reciver_pin = 14 
clock_pin = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(reciver_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(clock_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(clock_pin, GPIO.RISING)

try:
    while True:
        if GPIO.event_detected(clock_pin):
            if GPIO.input(reciver_pin) == GPIO.HIGH:
                print("1")
                time.sleep(wait)
                if GPIO.input(reciver_pin) == GPIO.HIGH:
                    print("2")
                    time.sleep(wait)
                    if GPIO.input(reciver_pin) == GPIO.LOW:
                        print("3")
                        time.sleep(wait)
                        if GPIO.input(reciver_pin) == GPIO.HIGH:
                            print("4")
                            time.sleep(wait)
                            print("connect")
                            
                            
except KeyboardInterrupt:
    print("Przerwano przez użytkownika")

finally:
    GPIO.cleanup()
