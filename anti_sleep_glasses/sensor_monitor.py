import threading, time, RPi.GPIO as GPIO

class SensorMonitor(threading.Thread):
    def __init__(self, dashboard, sensor_pin=2, motor_pin=8, buzzer_pin=9):
        super().__init__(daemon=True)
        self.dashboard = dashboard
        self.sensor_pin = sensor_pin
        self.motor_pin = motor_pin  
        self.buzzer_pin = buzzer_pin
        self.last_trigger_time = time.time()
        self.running = True

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_pin, GPIO.OUT)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
        GPIO.setup(self.sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(self.motor_pin, GPIO.HIGH)
        GPIO.output(self.buzzer_pin, GPIO.HIGH)

        def run(self):
            while self.running:
                if GPIO.input(self.sensor_pin) == GPIO.LOW:
                    self.last_trigger_time = time.time()
                    GPIO.output(self.buzzer_pin, GPIO.LOW)
                    GPIO.output(self.motor_pin, GPIO.HIGH)
                    self.dashboard.update_status("Drowsy state detected. Stay alert!")

                else:
                    elapsed_time = time.time() - self.last_trigger_time
                    if elapsed_time >= 5:
                        GPIO.output(self.buzzer_pin, GPIO.HIGH)
                        if elapsed_time >= 3:
                         GPIO.output(self.motor_pin, GPIO.LOW)
                        if elapsed_time < 3:
                            self.last_trigger_time = time.time()
                        self.dashboard.update_status("Alert state. You are awake!")    

                time.sleep(0.1)

        def stop(self):
            self.running = False
            GPIO.cleanup()                