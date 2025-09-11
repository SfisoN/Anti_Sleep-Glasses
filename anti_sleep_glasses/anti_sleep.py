
"""
import RPi.GPIO as GPIO
import time
"""

# Pin definitions (BCM numbering)
SENSOR_PIN = 2    # GPIO2 connected to IR/eye-detection sensor
MOTOR_PIN = 8     # GPIO8 connected to the motor relay/driver
BUZZER_PIN = 9    # GPIO9 connected to the buzzer

# Track the last time the sensor detected closed eyes
last_trigger_time = time.time()

def time_delay():
    """Return elapsed seconds since last sensor trigger."""
    return int(time.time() - last_trigger_time)

# --- Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # pull-up similar to Arduino default

GPIO.output(MOTOR_PIN, GPIO.HIGH)  # motor on initially
GPIO.output(BUZZER_PIN, GPIO.LOW)  # buzzer off

try:
    while True:
        if GPIO.input(SENSOR_PIN) == GPIO.LOW:
            # Eyes closed: reset timer, run motor, silence buzzer
            last_trigger_time = time.time()
            while GPIO.input(SENSOR_PIN) == GPIO.LOW:
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                GPIO.output(MOTOR_PIN, GPIO.HIGH)
                time.sleep(1)
        else:
            # Eyes open: check elapsed time
            if time_delay() >= 3:
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
            if time_delay() >= 4:
                GPIO.output(MOTOR_PIN, GPIO.LOW)

        time.sleep(0.1)  # small loop delay to reduce CPU usage

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
