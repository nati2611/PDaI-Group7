import RPi.GPIO as GPIO
import time

wait = 0.006
reciving_pin = 14
sending_pin = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(sending_pin, GPIO.OUT)
GPIO.setup(reciving_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(reciving_pin, GPIO.BOTH)


try:
    time.sleep(wait)
    while True:
            GPIO.output(sending_pin, GPIO.HIGH)
            time.sleep(wait)
            GPIO.output(sending_pin, GPIO.HIGH)
            time.sleep(wait)
            GPIO.output(sending_pin, GPIO.LOW)
            time.sleep(wait)
            GPIO.output(sending_pin, GPIO.HIGH)
            time.sleep(wait)
            break
    GPIO.output(sending_pin, GPIO.LOW)
    while True:
        if GPIO.event_detected(reciving_pin):
            if GPIO.input(reciving_pin) == GPIO.HIGH:
                time.sleep(wait)  
                if GPIO.input(reciving_pin) == GPIO.HIGH:
                    time.sleep(wait)
                    if GPIO.input(reciving_pin) == GPIO.LOW:
                        time.sleep(wait)
                        if GPIO.input(reciving_pin) == GPIO.HIGH:
                            print("connect")
                            time.sleep(wait)
                            break
    while True:
        input_user= input()
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(wait)
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(wait)
        GPIO.output(sending_pin, GPIO.LOW)
        time.sleep(wait)
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(wait)
        for i in input_user:
            if i == '0':
                GPIO.output(sending_pin, GPIO.LOW)
                time.sleep(wait)
            else:
                GPIO.output(sending_pin, GPIO.HIGH)
                time.sleep(wait)
        print("stop")
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(wait)
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(wait)
        GPIO.output(sending_pin, GPIO.LOW)
        time.sleep(wait)
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(wait)
        GPIO.output(sending_pin, GPIO.LOW)


    



except KeyboardInterrupt:
    print("^ end")

finally:
    GPIO.cleanup()
