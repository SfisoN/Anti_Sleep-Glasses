import tkinter as tk
from Pages.DashBoard import Dashboard
from Pages.Alerts import Alerts
from Pages.Help import Help
from sensor_monitor import SensorMonitor

class NeuroLensApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1200x699")
        self.window.title("NeuroLens")
        self.window.configure(bg="#D0DFFF")
        self.window.resizable(False, False)
        
        # Container frame for all pages
        self.container = tk.Frame(self.window, width=1200, height=699)
        self.container.pack(fill="both", expand=True)
        
        # Dictionary to store pages
        self.pages = {}
        
        # Initialize pages
        for PageClass in (Dashboard, Alerts, Help):
            page = PageClass(self.container, self)
            self.pages[PageClass.__name__] = page
            page.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.setup_sidebar()
        
        # Show Dashboard by default
        self.show_page('Dashboard')
    
    def setup_sidebar(self):
        # Create sidebar buttons with consistent styling
        sidebar_buttons = [
            ("Dashboard", 91),
            ("Alerts", 147), 
            ("Help/Info", 205),
            ("Log Out", 450)
        ]
        
        for text, y_pos in sidebar_buttons:
            page_name = text.replace("/Info", "").replace(" ", "")  # Convert "Help/Info" to "Help"
            if text == "Log Out":
                command = self.logout
            else:
                # Use a closure to capture the page_name correctly
                command = (lambda p: lambda: self.show_page(p))(page_name)
                
            btn = tk.Button(
                self.window, 
                text=text, 
               bg="#f6f9ff", 
               fg="#B9C0DE", 
                bd=0,
                font=("SFProRounded Regular", 15),
                cursor="hand2",
                #activebackground="#C0CFEE",
                activeforeground="#1657FF",
                command=command
            )
            btn.place(x=53, y=y_pos)
    
    def show_page(self, page_name):
        """Show the specified page"""
        if page_name in self.pages:
            self.pages[page_name].tkraise()
        else:
            print(f"Page {page_name} not found!")
    
    def logout(self):
        """Handle logout functionality"""
        result = tk.messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            self.window.quit()
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = NeuroLensApp()
    app.run()