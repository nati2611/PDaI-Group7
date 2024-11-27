import RPi.GPIO as GPIO
import time
import threading

wait = 0.009
clock_pin = 15
reciving_pin = 14
sending_pin = 18
flag = 1
clock_state = False
clock_end = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(sending_pin, GPIO.OUT)
GPIO.setup(reciving_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(reciving_pin, GPIO.BOTH)

clock_time = time.perf_counter()  # Use high-precision timer

def clock():
    global clock_time, flag, clock_state, clock_end
    while not clock_end:
        current_time = time.perf_counter()  # Use high-precision timer
        if current_time - clock_time >= wait:
            if flag % 2:
                GPIO.output(clock_pin, GPIO.HIGH)
                clock_state = True
            else:
                GPIO.output(clock_pin, GPIO.LOW)
                clock_state = False
            clock_time = current_time
            flag += 1
        time.sleep(0.001)  # Minimal delay to prevent excessive CPU usage

clock_thread = threading.Thread(target=clock)
clock_thread.daemon = True
clock_thread.start()

try:
    while True:
        if clock_state:  # Synchronization with the clock
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
                            '''_____________clock thread end_____________'''

                            clock_end = True 

                            '''_____________clock thread end_____________'''
                            break

except KeyboardInterrupt:
    print("^ KUNIEC")

finally:
    GPIO.cleanup()
