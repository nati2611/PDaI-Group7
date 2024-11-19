import RPi.GPIO as GPIO
import time
import threading

wait = 0.1
clock_pin = 15
reciving_pin = 14
sending_pin = 18
flag = 1
clock_state = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(sending_pin, GPIO.OUT)
GPIO.setup(reciving_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(reciving_pin, GPIO.BOTH)

clock_time = time.time()

def clock():
    global clock_time, flag, clock_state
    while True:
        current_time = time.time()
        if current_time - clock_time >= wait:
            if flag % 2:
                GPIO.output(clock_pin, GPIO.HIGH)
                clock_state = True
            else:
                GPIO.output(clock_pin, GPIO.LOW)
                clock_state = False
            clock_time = current_time
            flag += 1
        time.sleep(0.01)

clock_thread = threading.Thread(target=clock)
clock_thread.daemon = True
clock_thread.start()

try:
    while True:
        if clock_state:  # Synchronizacja z zegarem
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
    GPIO.output(sending_pin, GPIO.LOW)
    while True:
        if GPIO.event_detected(reciving_pin):
            if GPIO.input(reciving_pin) == GPIO.HIGH:
                print("1")
                time.sleep(wait)  
                if GPIO.input(reciving_pin) == GPIO.HIGH:
                    print("2")
                    time.sleep(wait)
                    if GPIO.input(reciving_pin) == GPIO.LOW:
                        print("3")
                        time.sleep(wait)
                        if GPIO.input(reciving_pin) == GPIO.HIGH:
                            print("4")
                            print("connect")
                            time.sleep(wait)
                            break

except KeyboardInterrupt:
    print("^ KUNIEC")

finally:
    GPIO.cleanup()
