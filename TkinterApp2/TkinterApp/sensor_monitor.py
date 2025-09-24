import threading
import time
import platform
from datetime import datetime

# Check if we're on Raspberry Pi
IS_RASPBERRY_PI = platform.machine() in ('armv7l', 'aarch64')

if IS_RASPBERRY_PI:
    try:
        import RPi.GPIO as GPIO
        print("Running on Raspberry Pi - using real GPIO")
    except ImportError:
        IS_RASPBERRY_PI = False
        print("RPi.GPIO not available - using simulation mode")
else:
    print("Running on Windows/other - using simulation mode")

class SensorMonitor(threading.Thread):
    def __init__(self, dashboard, sensor_pin=2, motor_pin=8, buzzer_pin=9):
        super().__init__(daemon=True)
        self.dashboard = dashboard
        self.sensor_pin = sensor_pin
        self.motor_pin = motor_pin  
        self.buzzer_pin = buzzer_pin
        self.last_trigger_time = time.time()
        self.running = True
        
        # Data for dashboard
        self.battery_level = 85  # Start with 85%
        self.current_status = "Alert"
        self.alert_count = 0
        self.new_alerts = []
        
        # Simulation variables (for Windows testing)
        self.simulation_mode = not IS_RASPBERRY_PI
        self.sim_eyes_closed = False
        self.sim_cycle_time = 0

        # Setup GPIO only if on Raspberry Pi
        if IS_RASPBERRY_PI:
            self.setup_real_gpio()
        else:
            self.setup_simulation()
            
        print(f"Sensor monitor initialized ({'Real Hardware' if IS_RASPBERRY_PI else 'Simulation Mode'})")

    def setup_real_gpio(self):
        """Setup real GPIO for Raspberry Pi"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_pin, GPIO.OUT)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
        GPIO.setup(self.sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(self.motor_pin, GPIO.HIGH)
        GPIO.output(self.buzzer_pin, GPIO.LOW)
        
    def setup_simulation(self):
        """Setup simulation for Windows testing"""
        print("Simulation mode: Will fake sensor readings for testing")
        self.motor_on = True
        self.buzzer_on = False

    def run(self):
        """Main sensor monitoring loop"""
        while self.running:
            try:
                if IS_RASPBERRY_PI:
                    self.run_real_hardware()
                else:
                    self.run_simulation()
                    
                # Slowly decrease battery for realism
                self.battery_level -= 0.01
                if self.battery_level < 20:
                    self.battery_level = 100  # Reset when low
                    
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Sensor error: {e}")
                time.sleep(1)

    def run_real_hardware(self):
        """Real hardware sensor reading"""
        if GPIO.input(self.sensor_pin) == GPIO.LOW:
            # Eyes closed detected
            self.last_trigger_time = time.time()
            GPIO.output(self.buzzer_pin, GPIO.LOW)
            GPIO.output(self.motor_pin, GPIO.HIGH)
            
            self.current_status = "Eyes Closed"
            self.dashboard.update_status("Eyes closed detected. Monitoring...")
            
        else:
            # Eyes open - check how long
            elapsed_time = time.time() - self.last_trigger_time
            
            if elapsed_time >= 5:
                GPIO.output(self.buzzer_pin, GPIO.HIGH)
                self.current_status = "Drowsy"
                self.dashboard.update_status("DROWSINESS ALERT! Take a break!")
                self.create_alert("Eyes open for 5+ seconds")
                
            if elapsed_time >= 3:
                GPIO.output(self.motor_pin, GPIO.LOW)
                
            if elapsed_time < 3:
                self.current_status = "Alert"
                self.dashboard.update_status("Alert state. You are awake!")
                GPIO.output(self.buzzer_pin, GPIO.LOW)

    def run_simulation(self):
        """Simulation for Windows testing"""
        import random
        
        # Simulate a cycle: alert -> drowsy -> alert
        self.sim_cycle_time += 0.1
        
        # Every 10 seconds, change state
        if self.sim_cycle_time > 10:
            self.sim_cycle_time = 0
            self.sim_eyes_closed = not self.sim_eyes_closed
        
        if self.sim_eyes_closed:
            # Simulate eyes closed
            self.last_trigger_time = time.time()
            self.current_status = "Eyes Closed"
            self.dashboard.update_status("SIMULATION: Eyes closed detected")
            self.motor_on = True
            self.buzzer_on = False
            
        else:
            # Simulate eyes open for varying time
            elapsed_time = self.sim_cycle_time
            
            if elapsed_time > 7:  # Simulate drowsiness after 7 seconds
                self.current_status = "Drowsy"
                self.dashboard.update_status("SIMULATION: Drowsiness detected!")
                self.buzzer_on = True
                self.create_alert("Simulated drowsiness detection")
                
            elif elapsed_time > 5:
                self.current_status = "Tired" 
                self.dashboard.update_status("SIMULATION: Getting tired...")
                self.motor_on = False
                
            else:
                self.current_status = "Alert"
                self.dashboard.update_status("SIMULATION: Alert and awake")
                self.buzzer_on = False
                self.motor_on = True

    def create_alert(self, condition):
        """Create a new alert for the dashboard"""
        # Don't spam alerts - only create one per state change
        if not hasattr(self, '_last_alert_status') or self._last_alert_status != self.current_status:
            self.alert_count += 1
            alert = {
                "title": f"Drowsiness Alert #{self.alert_count:03d}",
                "username": "TestUser" if self.simulation_mode else "User", 
                "condition": condition,
                "action": "Buzzer and motor activated" if IS_RASPBERRY_PI else "Simulation alert",
                "response": "Monitoring...",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            self.new_alerts.append(alert)
            self._last_alert_status = self.current_status
            print(f"NEW ALERT: {alert['title']} - {condition}")

    def get_drowsiness_level(self):
        """Get current drowsiness status"""
        return self.current_status

    def get_battery_level(self):
        """Get current battery percentage"""
        return int(self.battery_level)
    
    def get_new_alerts(self):
        """Get and clear new alerts"""
        alerts = self.new_alerts.copy()
        self.new_alerts.clear()
        return alerts

    def stop(self):
        """Stop monitoring and cleanup"""
        self.running = False
        if IS_RASPBERRY_PI:
            GPIO.cleanup()
        print("Sensor monitor stopped")