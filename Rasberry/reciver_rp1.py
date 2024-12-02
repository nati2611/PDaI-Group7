import RPi.GPIO as GPIO
import time

wait = 0.006
reciving_pin = 14
sending_pin = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(reciving_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sending_pin, GPIO.OUT)
GPIO.add_event_detect(reciving_pin, GPIO.BOTH)



recived= ""
try:
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
                            break
                            
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
    time.sleep(0.1)
    if GPIO.event_detected(reciving_pin):
        print("reciving...")
    flag = False
    while True:
        if GPIO.event_detected(reciving_pin):
            if GPIO.input(reciving_pin) == GPIO.HIGH:
                time.sleep(wait)  
                if GPIO.input(reciving_pin) == GPIO.HIGH:
                    time.sleep(wait)
                    if GPIO.input(reciving_pin) == GPIO.LOW:
                        time.sleep(wait)
                        if GPIO.input(reciving_pin) == GPIO.HIGH:
                            time.sleep(wait)
                            while True:
                                if GPIO.input(reciving_pin) == GPIO.HIGH:
                                    recived = recived + "1"
                                    print("recived..",recived )
                                    time.sleep(wait)     
                                else:
                                    recived = recived + "0"
                                    print("recived..", recived)
                                    time.sleep(wait)
                                if recived.endswith("1101") and len(recived) > 4:
                                    flag = True
                                    break
        if flag == True:
            recived = recived[0:-4]
            print(recived)
            recived = ""
            flag = False
            GPIO.event_detected(reciving_pin)

except KeyboardInterrupt:
    print("^ end")

finally:
    GPIO.cleanup()
