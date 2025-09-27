# app.py - Enhanced Main Application Entry Point
import tkinter as tk
from tkinter import messagebox
from Pages.DashBoard import Dashboard
from Pages.Alerts import Alerts  #
from Pages.Help import Help
from sensor_monitor import SensorMonitor

class NeuroLensApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1072x618")
        self.window.title("NeuroLens - Drowsiness Monitor")
        self.window.configure(bg="#3A404D")
        self.window.resizable(False, False)
        
        # Initialize sensor monitor
        try:
            self.sensor_monitor = SensorMonitor()
            self.sensor_monitor.start()
            print("Sensor monitor initialized successfully")
        except Exception as e:
            print(f"Sensor monitor initialization failed: {e}")
            self.sensor_monitor = None
        
        # Session tracking
        self.session_count = 0
        self.current_page = None
        
        # Container frame for all pages
        self.container = tk.Frame(self.window, width=1072, height=618, bg="#3A404D")
        self.container.pack(fill="both", expand=True)
        
        # Dictionary to store pages
        self.pages = {}
        
        # Initialize pages
        self.initialize_pages()
        
        # Setup navigation
        self.setup_navigation()
        
        # Show Dashboard by default
        self.show_page('Dashboard')
        
        # Setup window close handler
        self.window.protocol("WM_DELETE_WINDOW", self.on_window_close)
    
    def initialize_pages(self):
        """Initialize all application pages"""
        page_classes = [
            ('Dashboard', Dashboard),
            ('Alerts', Alerts),   # Make sure Alerts.py exists and contains class Alerts
            ('Help', Help)
        ]
        
        for page_name, PageClass in page_classes:
            try:
                page = PageClass(self.container, self)
                self.pages[page_name] = page
                page.place(x=0, y=0, relwidth=1, relheight=1)
                print(f"✓ {page_name} page initialized")
            except Exception as e:
                print(f"✗ Error initializing {page_name}: {e}")
    
    def setup_navigation(self):
        """Setup navigation buttons styled as text links"""
        nav_buttons = [
            (30, 81, 150, 25, 'Dashboard'),
            (30, 117, 150, 25, 'Alerts'),
            (30, 157, 150, 25, 'Help'),
            (30, 197, 150, 25, self.logout)
        ]
        
        for x, y, width, height, target in nav_buttons:
            if callable(target):
                btn = tk.Button(
                    self.window, text="Logout", bg="#3A404D", fg="white",
                    bd=0, cursor="hand2", font=("Arial", 10, "underline"),
                    command=target, relief="flat",
                    activebackground="#3A404D", activeforeground="white"
                )
            else:
                btn = tk.Button(
                    self.window, text=target, bg="#3A404D", fg="white",
                    bd=0, cursor="hand2", font=("Arial", 10, "underline"),
                    command=lambda p=target: self.show_page(p),
                    relief="flat",
                    activebackground="#3A404D", activeforeground="white"
                )
            
            btn.place(x=x, y=y, width=width, height=height)
    
    def show_page(self, page_name):
        """Show the specified page"""
        print(f"Attempting to show page: {page_name}")
        print(f"Available pages: {list(self.pages.keys())}")
        
        if page_name in self.pages:
            # Hide all pages first
            for name, page in self.pages.items():
                page.place_forget()
                print(f"Hid page: {name}")
            
            # Show selected page
            current_page = self.pages[page_name]
            current_page.place(x=0, y=0, relwidth=1, relheight=1)
            current_page.tkraise()
            
            # Update current page reference
            self.current_page = page_name
            
            # Call page-specific show handler if available
            if hasattr(current_page, 'on_page_show'):
                try:
                    current_page.on_page_show()
                except Exception as e:
                    print(f"Error calling on_page_show for {page_name}: {e}")
            
            print(f"✓ Successfully navigated to {page_name} page")
            
            # Update window title based on current page
            page_titles = {
                'Dashboard': 'NeuroLens - Dashboard',
                'Alerts': 'NeuroLens - Alerts Monitor', 
                'Help': 'NeuroLens - Help & Support'
            }
            self.window.title(page_titles.get(page_name, 'NeuroLens'))
            
        else:
            print(f"❌ Page '{page_name}' not found in pages dictionary!")
            print(f"Available pages: {list(self.pages.keys())}")
            messagebox.showerror("Navigation Error", 
                f"Page '{page_name}' could not be found.\n\n"
                f"Available pages: {', '.join(self.pages.keys())}")
    
    def logout(self):
        """Handle logout functionality with confirmation"""
        try:
            result = messagebox.askyesno(
                "Confirm Logout", 
                "Are you sure you want to logout?\n\nThis will:\n"
                "• Stop sensor monitoring\n"
                "• Save current session data\n"
                "• Close the application",
                icon="question"
            )
            
            if result:
                # Increment session count
                self.session_count += 1
                
                # Update dashboard session count if available
                if 'Dashboard' in self.pages:
                    dashboard = self.pages['Dashboard']
                    if hasattr(dashboard, 'increment_logout_count'):
                        dashboard.increment_logout_count()
                
                # Stop sensor monitor
                if self.sensor_monitor:
                    try:
                        self.sensor_monitor.stop()
                        print("Sensor monitor stopped")
                    except Exception as e:
                        print(f"Error stopping sensor monitor: {e}")
                
                # Show logout confirmation
                messagebox.showinfo("Logout Complete", 
                    "✓ Session ended successfully\n"
                    "✓ Data saved\n"
                    "✓ Sensor monitoring stopped")
                
                # Close application
                self.window.quit()
                
        except Exception as e:
            print(f"Logout error: {e}")
            messagebox.showerror("Logout Error", f"An error occurred during logout:\n{str(e)}")
    
    def on_window_close(self):
        """Handle window close event"""
        try:
            result = messagebox.askyesno(
                "Exit NeuroLens",
                "Are you sure you want to exit?\n\n"
                "This will stop all monitoring and close the application.",
                icon="question"
            )
            
            if result:
                # Stop sensor monitor
                if self.sensor_monitor:
                    try:
                        self.sensor_monitor.stop()
                        print("Sensor monitor stopped on exit")
                    except:
                        pass
                
                # Cleanup any page resources
                for page in self.pages.values():
                    if hasattr(page, 'cleanup'):
                        try:
                            page.cleanup()
                        except:
                            pass
                
                self.window.destroy()
                
        except Exception as e:
            print(f"Window close error: {e}")
            # Force close if error
            self.window.destroy()
    
    def get_sensor_data(self):
        """Get current sensor data for pages"""
        if self.sensor_monitor:
            try:
                return self.sensor_monitor.get_dashboard_data()
            except Exception as e:
                print(f"Sensor data error: {e}")
                return None
        return None
    
    def add_alert_to_alerts_page(self, alert_data):
        """Add an alert to the alerts page"""
        try:
            if 'Alerts' in self.pages:
                alerts_page = self.pages['Alerts']
                if hasattr(alerts_page, 'add_live_alert'):
                    alerts_page.add_live_alert(alert_data)
                    print(f"Alert added to Alerts page: {alert_data.get('title', 'Unknown')}")
        except Exception as e:
            print(f"Error adding alert to alerts page: {e}")
    
    def run(self):
        """Start the application main loop"""
        try:
            print("🚀 Starting NeuroLens Application...")
            print(f"📊 Pages loaded: {list(self.pages.keys())}")
            print(f"🔌 Sensor monitor: {'Active' if self.sensor_monitor else 'Inactive'}")
            print("✅ Application ready")
            
            # Start the main event loop
            self.window.mainloop()
            
        except Exception as e:
            print(f"❌ Application error: {e}")
            messagebox.showerror("Application Error", 
                f"A critical error occurred:\n\n{str(e)}\n\nThe application will close.")
        
        finally:
            # Cleanup on exit
            if self.sensor_monitor:
                try:
                    self.sensor_monitor.stop()
                    print("Cleanup: Sensor monitor stopped")
                except:
                    pass
            
            print("👋 NeuroLens Application closed")

def main():
    """Main entry point with error handling"""
    try:
        # Create and run the application
        app = NeuroLensApp()
        app.run()
        
    except Exception as e:
        print(f"💥 Critical application error: {e}")
        
        # Show error dialog if possible
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            messagebox.showerror("Critical Error", 
                f"NeuroLens failed to start:\n\n{str(e)}\n\n"
                "Please check your system requirements and try again.")
            root.destroy()
        except:
            pass
    
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
    
    finally:
        print("🔄 Application shutdown complete")

if __name__ == "__main__":
    main()
