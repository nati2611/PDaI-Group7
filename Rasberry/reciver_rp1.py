import RPi.GPIO as GPIO
import time
import threading

wait = 0.06
reciving_pin = 14
sending_pin = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(reciving_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sending_pin, GPIO.OUT)
GPIO.add_event_detect(reciving_pin, GPIO.BOTH)



def send_data():
    while True:
        input_user= input()
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(wait)
        GPIO.output(sending_pin, GPIO.LOW)
        time.sleep(wait)
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(wait*3)
        GPIO.output(sending_pin, GPIO.LOW)
        time.sleep(wait)
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(wait*3)
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
        GPIO.output(sending_pin, GPIO.LOW)
        time.sleep(wait)
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(wait*3)
        GPIO.output(sending_pin, GPIO.LOW)
        time.sleep(wait)
        GPIO.output(sending_pin, GPIO.HIGH)
        time.sleep(wait*3)
        GPIO.output(sending_pin, GPIO.LOW)
    
    print("thread stoped")
        


recived= ""
try:
    while True:
        time.sleep(0.001)
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
    sender_thread = threading.Thread(target=send_data, daemon=True)
    sender_thread.start()

    
    flag = False
    
    '''sender message code  1011110111  - 99 (if in code numbers above and including 80 appear the system won't work)'''
    '''reciver message code 101110111   - 98'''

    while True:
        time.sleep(0.001)
        if GPIO.event_detected(reciving_pin):
            if GPIO.input(reciving_pin) == GPIO.HIGH:
                time.sleep(wait)  
                if GPIO.input(reciving_pin) == GPIO.LOW:
                    time.sleep(wait)
                    if GPIO.input(reciving_pin) == GPIO.HIGH:
                        time.sleep(wait)
                        if GPIO.input(reciving_pin) == GPIO.HIGH:
                            time.sleep(wait)
                            if GPIO.input(reciving_pin) == GPIO.HIGH:
                                time.sleep(wait)
                                if GPIO.input(reciving_pin) == GPIO.HIGH:
                                    time.sleep(wait)
                                    if GPIO.input(reciving_pin) == GPIO.LOW:
                                        time.sleep(wait)
                                        if GPIO.input(reciving_pin) == GPIO.HIGH:
                                            time.sleep(wait)
                                            if GPIO.input(reciving_pin) == GPIO.HIGH:
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
                                                        if recived.endswith("1011110111") and len(recived) > 10:
                                                            flag = True
                                                            break
        if flag == True:
            recived = recived[0:-10]
            print(recived)
            recived = ""
            flag = False
            GPIO.event_detected(reciving_pin)

except KeyboardInterrupt:
    print("^ end")

finally:
    GPIO.cleanup()
