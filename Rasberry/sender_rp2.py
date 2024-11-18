import RPi.GPIO as GPIO
import time
import threading

wait = 1  # czas trwania stanu HIGH i LOW w sekundach
clock_pin = 15
sending_pin = 14
flag = 1
clock_state = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(sending_pin, GPIO.OUT)

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
            
            if flag == 100000:
                flag = 1
            else:
                flag += 1  

        time.sleep(0.1)  

clock_thread = threading.Thread(target=clock)
clock_thread.daemon = True  
clock_thread.start()

try:
    while True:
        if clock_state == True:
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
        

        time.sleep(0.1)  

except KeyboardInterrupt:
    print("^ KUNIEC")

finally:
    GPIO.cleanup()
