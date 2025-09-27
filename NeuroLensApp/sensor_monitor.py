# sensor_monitor.py - Enhanced Sensor Monitor with Dynamic Updates
import threading
import time
import platform
import random
from datetime import datetime

# Check if we're on Raspberry Pi
IS_RASPBERRY_PI = platform.machine() in ('armv7l', 'aarch64')

if IS_RASPBERRY_PI:
    try:
        import RPi.GPIO as GPIO
        print("Running on Raspberry Pi - using real GPIO")
    except ImportError:
        IS_RASPBERRY_PI = False
        GPIO = None
        print("RPi.GPIO not available - using simulation mode")
else:
    print("Running on Windows/other - using simulation mode")

class SensorMonitor(threading.Thread):
    def __init__(self, dashboard=None, sensor_pin=2, motor_pin=8, buzzer_pin=9):
        super().__init__(daemon=True)
        self.dashboard = dashboard
        self.sensor_pin = sensor_pin
        self.motor_pin = motor_pin  
        self.buzzer_pin = buzzer_pin
        self.last_trigger_time = time.time()
        self.running = True
        
        # Enhanced data tracking
        self.battery_level = 85.0
        self.current_status = 3  # 1-5 scale (1=drowsy, 5=alert)
        self.alert_count = 0
        self.new_alerts = []
        self.blink_count = 0
        self.session_start = time.time()
        
        # Performance metrics
        self.performance_metrics = {
            'total_alerts': 0,
            'response_rate': 85.0,
            'avg_response_time': 2.5,
            'false_positives': 3
        }
        
        # Simulation variables
        self.simulation_mode = not IS_RASPBERRY_PI
        self.sim_cycle = 0
        self.last_alert_time = 0
        
        # Alert patterns for realistic simulation
        self.alert_conditions = [
            "Eyes closed for 3+ seconds",
            "Head nodding detected", 
            "Low blink rate: 8/min",
            "Micro-sleep episode detected",
            "Sustained attention drift",
            "Eyelid droop detected",
            "Head tilt angle exceeded"
        ]
        
        self.user_responses = [
            "User acknowledged",
            "User took break", 
            "No response",
            "User alert",
            "Session paused",
            "User active"
        ]

        # Setup hardware or simulation
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
        """Setup simulation for testing"""
        print("Simulation mode: Generating realistic sensor data")
        self.motor_on = True
        self.buzzer_on = False

    def run(self):
        """Main sensor monitoring loop"""
        while self.running:
            try:
                if IS_RASPBERRY_PI:
                    self.run_real_hardware()
                else:
                    self.run_enhanced_simulation()
                
                # Update metrics
                self.update_system_metrics()
                
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Sensor monitoring error: {e}")
                time.sleep(1)

    def run_real_hardware(self):
        """Monitor real hardware sensors"""
        sensor_state = GPIO.input(self.sensor_pin)
        
        if sensor_state == GPIO.LOW:  # Eyes closed
            self.handle_eyes_closed()
        else:  # Eyes open
            self.handle_eyes_open()

    def run_enhanced_simulation(self):
        """Enhanced simulation with realistic patterns"""
        self.sim_cycle += 1
        
        # Realistic drowsiness patterns
        if self.sim_cycle % 200 == 0:  # Major state change every ~20 seconds
            # Simulate drowsiness episode
            self.current_status = random.choice([1, 2])  # Drowsy states
            self.create_realistic_alert()
            
        elif self.sim_cycle % 100 == 0:  # Minor state change every ~10 seconds
            # Gradual state changes
            if self.current_status <= 2:
                self.current_status = min(5, self.current_status + random.randint(1, 2))
            else:
                self.current_status = max(1, self.current_status + random.randint(-1, 1))
                
        # Simulate blink counting
        if self.sim_cycle % 30 == 0:  # Every 3 seconds
            self.blink_count += random.randint(1, 3)
        
        # Battery drain simulation
        if self.sim_cycle % 1000 == 0:  # Every ~100 seconds
            self.battery_level = max(15.0, self.battery_level - random.uniform(0.5, 2.0))
            if self.battery_level < 20:
                self.create_battery_alert()

    def handle_eyes_closed(self):
        """Handle eyes closed detection"""
        current_time = time.time()
        closed_duration = current_time - self.last_trigger_time
        
        if closed_duration > 3.0:  # Critical threshold
            self.current_status = 1
            self.trigger_alert("Eyes closed for 3+ seconds - Critical drowsiness")
            self.activate_all_alerts()
            
        elif closed_duration > 2.0:  # Warning threshold
            self.current_status = 2
            self.activate_vibration()
            
        elif closed_duration > 1.0:  # Caution
            self.current_status = 3

    def handle_eyes_open(self):
        """Handle eyes open detection"""
        self.last_trigger_time = time.time()
        self.current_status = min(5, self.current_status + 1)  # Improve status
        self.deactivate_alerts()

    def create_realistic_alert(self):
        """Create realistic alert with proper formatting"""
        current_time = time.time()
        
        # Don't spam alerts
        if current_time - self.last_alert_time < 5:
            return
            
        self.alert_count += 1
        self.last_alert_time = current_time
        
        alert = {
            "id": f"A{self.alert_count:03d}",
            "title": f"Drowsiness Alert #{self.alert_count:03d}",
            "user": "Current User",
            "condition": random.choice(self.alert_conditions),
            "action": self.get_alert_action(),
            "response": random.choice(self.user_responses),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "battery": f"{self.battery_level:.1f}%",
            "status": self.current_status,
            "session_time": self.get_session_duration()
        }
        
        self.new_alerts.append(alert)
        self.performance_metrics['total_alerts'] += 1
        
        print(f"ALERT GENERATED: {alert['condition']} (Status: {self.current_status})")

    def create_battery_alert(self):
        """Create battery-specific alert"""
        if self.battery_level < 20:
            battery_alert = {
                "id": f"B{self.alert_count:03d}",
                "title": "Low Battery Warning",
                "user": "System",
                "condition": f"Battery level critically low: {self.battery_level:.1f}%",
                "action": "Battery warning notification sent",
                "response": "Charge device immediately",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "battery": f"{self.battery_level:.1f}%",
                "status": "critical"
            }
            
            self.new_alerts.append(battery_alert)
            print(f"BATTERY ALERT: {self.battery_level:.1f}%")

    def get_alert_action(self):
        """Generate appropriate alert action based on status"""
        actions = {
            1: "Emergency alert - Buzzer + Vibration + Visual",
            2: "High priority - Buzzer + Vibration", 
            3: "Standard alert - Vibration only",
            4: "Low priority - Visual notification",
            5: "Information only - Status update"
        }
        return actions.get(self.current_status, "Alert notification sent")

    def get_session_duration(self):
        """Get current session duration"""
        duration = time.time() - self.session_start
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        return f"{hours}H{minutes:02d}m"

    def update_system_metrics(self):
        """Update system performance metrics"""
        # Simulate performance changes
        if random.random() < 0.01:  # 1% chance per cycle
            self.performance_metrics['response_rate'] += random.uniform(-2, 3)
            self.performance_metrics['response_rate'] = max(70, min(100, self.performance_metrics['response_rate']))
            
            self.performance_metrics['avg_response_time'] += random.uniform(-0.5, 0.5)  
            self.performance_metrics['avg_response_time'] = max(1.0, min(5.0, self.performance_metrics['avg_response_time']))

    def activate_all_alerts(self):
        """Activate all alert mechanisms"""
        if IS_RASPBERRY_PI:
            GPIO.output(self.buzzer_pin, GPIO.HIGH)
            GPIO.output(self.motor_pin, GPIO.LOW)  # Active low
        else:
            self.buzzer_on = True
            self.motor_on = False
            print("🚨 FULL ALERT ACTIVATED: Buzzer + Vibration")

    def activate_vibration(self):
        """Activate vibration only"""
        if IS_RASPBERRY_PI:
            GPIO.output(self.motor_pin, GPIO.LOW)
        else:
            self.motor_on = False
            print("📳 Vibration alert activated")

    def deactivate_alerts(self):
        """Deactivate all alert mechanisms"""
        if IS_RASPBERRY_PI:
            GPIO.output(self.buzzer_pin, GPIO.LOW)
            GPIO.output(self.motor_pin, GPIO.HIGH)
        else:
            self.buzzer_on = False
            self.motor_on = True

    def trigger_alert(self, message):
        """Trigger alert with logging"""
        if self.dashboard and hasattr(self.dashboard, 'update_status'):
            self.dashboard.update_status(message)
        print(f"ALERT: {message}")

    def get_dashboard_data(self):
        """Get comprehensive data for dashboard"""
        session_duration = time.time() - self.session_start
        
        return {
            "battery_level": max(0, self.battery_level),
            "current_status": self.current_status,
            "alert_count": self.alert_count,
            "new_alerts": self.new_alerts.copy(),
            "blink_count": self.blink_count,
            "session_duration": session_duration,
            "performance_metrics": self.performance_metrics.copy(),
            "connectivity_status": True,  # Simulated - replace with real check
            "last_update": datetime.now().isoformat()
        }

    def get_alerts_data(self):
        """Get alerts specifically formatted for alerts page"""
        return [
            {
                "title": alert.get("title", "Alert"),
                "user": alert.get("user", "Unknown"),
                "condition": alert.get("condition", "Unknown condition"),
                "action": alert.get("action", "Alert sent"),
                "response": alert.get("response", "Pending"),
                "date": alert.get("date", datetime.now().strftime("%Y-%m-%d %H:%M")),
                "live": True
            }
            for alert in self.new_alerts
        ]

    def clear_alerts(self):
        """Clear processed alerts"""
        cleared_count = len(self.new_alerts)
        self.new_alerts = []
        if cleared_count > 0:
            print(f"Cleared {cleared_count} processed alerts")

    def get_performance_history(self):
        """Get performance data for charts"""
        # Generate realistic performance history
        base_performance = self.performance_metrics['response_rate']
        history = []
        
        for i in range(7):  # Last 7 data points
            variation = random.uniform(-5, 5)
            value = max(70, min(100, base_performance + variation))
            history.append(int(value))
        
        return history

    def reset_session(self):
        """Reset session data"""
        self.session_start = time.time()
        self.blink_count = 0
        self.alert_count = 0
        self.new_alerts = []
        print("Session data reset")

    def stop(self):
        """Stop the monitoring thread"""
        self.running = False
        self.deactivate_alerts()
        
        if IS_RASPBERRY_PI and GPIO:
            GPIO.cleanup()
        
        print("Sensor monitor stopped and cleaned up")

# Test functionality when run directly
if __name__ == "__main__":
    print("Testing NeuroLens Sensor Monitor...")
    
    monitor = SensorMonitor()
    monitor.start()
    
    try:
        # Test for 30 seconds
        for i in range(30):
            data = monitor.get_dashboard_data()
            print(f"[{i+1:2d}] Status: {data['current_status']} | "
                  f"Battery: {data['battery_level']:.1f}% | "
                  f"Alerts: {data['alert_count']} | "
                  f"Blinks: {data['blink_count']}")
            
            # Clear alerts periodically
            if i % 10 == 0:
                monitor.clear_alerts()
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    
    finally:
        monitor.stop()
        print("Test completed")