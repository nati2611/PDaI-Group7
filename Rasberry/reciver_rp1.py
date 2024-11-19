import RPi.GPIO as GPIO
import time
wait = 0.1
reciving_pin = 14
sending_pin = 18
clock_pin = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(reciving_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(clock_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sending_pin, GPIO.OUT)


GPIO.add_event_detect(clock_pin, GPIO.BOTH)

try:
    while True:
        if GPIO.event_detected(clock_pin):
            if GPIO.input(reciving_pin) == GPIO.HIGH:
                print("1")
                while not GPIO.event_detected(clock_pin):
                    pass  
                if GPIO.input(reciving_pin) == GPIO.HIGH:
                    print("2")
                    while not GPIO.event_detected(clock_pin):
                        pass
                    if GPIO.input(reciving_pin) == GPIO.LOW:
                        print("3")
                        while not GPIO.event_detected(clock_pin):
                            pass
                        if GPIO.input(reciving_pin) == GPIO.HIGH:
                            print("4")
                            print("connect")
                            break
    while True:
        if GPIO.event_detected(clock_pin):  # Synchronizacja z zegarem
            GPIO.output(sending_pin, GPIO.HIGH)
            print("1")
            time.sleep(wait)
            GPIO.output(sending_pin, GPIO.HIGH)
            print("2")
            time.sleep(wait)
            GPIO.output(sending_pin, GPIO.LOW)
            print("3")
            time.sleep(wait)
            GPIO.output(sending_pin, GPIO.HIGH)
            print("4")
            time.sleep(wait)
            break
            
    

except KeyboardInterrupt:
    print("Przerwano przez użytkownika")

finally:
    GPIO.cleanup()
