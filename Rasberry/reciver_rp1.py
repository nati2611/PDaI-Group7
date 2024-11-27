import RPi.GPIO as GPIO
import time
import threading

wait = 0.009
reciving_pin = 14
sending_pin = 18
clock_pin = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(reciving_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(clock_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sending_pin, GPIO.OUT)
GPIO.add_event_detect(clock_pin, GPIO.BOTH)

'''___________synchro___________'''

clock_end = False
flag = 1
clock_show_pin = 23
GPIO.setup(clock_show_pin, GPIO.OUT)

clock_time = time.perf_counter()  # Use high-precision timer

def clock():
    global clock_time, flag, clock_state, clock_end
    while not clock_end:
        current_time = time.perf_counter()  # Use high-precision timer
        if current_time - clock_time >= wait:
            if flag % 2:
                GPIO.output(clock_show_pin, GPIO.HIGH)
                clock_state = True
            else:
                GPIO.output(clock_show_pin, GPIO.LOW)
                clock_state = False
            clock_time = current_time
            flag += 1
        time.sleep(0.001)  # Minimal delay to prevent excessive CPU usage

clock_thread = threading.Thread(target=clock)
clock_thread.daemon = True
clock_thread.start()

'''___________synchro___________'''

try:
    while True:
        if GPIO.event_detected(clock_pin):
            if GPIO.input(reciving_pin) == GPIO.HIGH:
                print("1 - in")
                while not GPIO.event_detected(clock_pin):
                    pass  
                if GPIO.input(reciving_pin) == GPIO.HIGH:
                    print("2 - in")
                    while not GPIO.event_detected(clock_pin):
                        pass
                    if GPIO.input(reciving_pin) == GPIO.LOW:
                        print("3 - in")
                        while not GPIO.event_detected(clock_pin):
                            pass
                        if GPIO.input(reciving_pin) == GPIO.HIGH:
                            print("4 - in")
                            print("connect")
                            break
    while True:
        if GPIO.event_detected(clock_pin):  # Synchronization with the clock
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
            '''_____________clock thread end_____________'''

            clock_end = True 

            '''_____________clock thread end_____________'''
            break

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    GPIO.cleanup()
