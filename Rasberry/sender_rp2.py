import RPi.GPIO as GPIO
import time

wait = 0.01
reciving_pin = 14
sending_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(sending_pin, GPIO.OUT)
GPIO.setup(reciving_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(reciving_pin, GPIO.BOTH)


try:
    time.sleep(wait)
    while True:
            GPIO.output(sending_pin, GPIO.HIGH)
            print("1 - out")
            time.sleep(wait)
            GPIO.output(sending_pin, GPIO.HIGH)
            print("2 - out")
            time.sleep(wait)
            GPIO.output(sending_pin, GPIO.LOW)
            print("3 - out")
            time.sleep(wait)
            GPIO.output(sending_pin, GPIO.HIGH)
            print("4 - out")
            time.sleep(wait)
            break
    GPIO.output(sending_pin, GPIO.LOW)
    while True:
        if GPIO.event_detected(reciving_pin):
            if GPIO.input(reciving_pin) == GPIO.HIGH:
                print("1 - in")
                time.sleep(wait)  
                if GPIO.input(reciving_pin) == GPIO.HIGH:
                    print("2 - in")
                    time.sleep(wait)
                    if GPIO.input(reciving_pin) == GPIO.LOW:
                        print("3 - in")
                        time.sleep(wait)
                        if GPIO.input(reciving_pin) == GPIO.HIGH:
                            print("4 - in")
                            print("connect")
                            time.sleep(wait)
                            break

except KeyboardInterrupt:
    print("^ end")

finally:
    GPIO.cleanup()
