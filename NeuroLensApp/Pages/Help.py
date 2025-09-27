# Pages/Help.py - Fixed Help Page
from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Text, Scrollbar, PhotoImage, Entry, Frame, Label

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH.parent / "assets/help"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Help(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#3A404D")
        self.controller = controller
        
        self.setup_ui()
    
    def setup_ui(self):
        self.canvas = Canvas(self, bg="#3A404D", height=618, width=1072,
                            bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        
        self.load_static_elements()
        self.add_static_text()
        self.setup_search_entry()  # FIXED - Added search entry
        self.setup_help_content()
    
    def load_static_elements(self):
        """Load static UI elements"""
        image_files = [
            ("image_1.png", 102.0, 351.0),
            ("image_2.png", 27.0, 173.0),
            ("image_3.png", 29.0, 101.0),
            ("image_4.png", 27.0, 136.0),
            ("image_5.png", 28.0, 216.0),
            ("image_6.png", 524.0, 322.0),
            ("image_7.png", 237.0, 32.0),
            ("image_8.png", 563.0, 27.0),
            ("image_9.png", 898.0, 28.0),
            ("image_10.png", 928.0, 28.0),
            ("image_11.png", 959.0, 28.0),
            ("image_12.png", 27.0, 22.0)
        ]
        
        for filename, x, y in image_files:
            try:
                img = PhotoImage(file=relative_to_assets(filename))
                setattr(self, filename.replace('.png', ''), img)
                self.canvas.create_image(x, y, image=img)
            except:
                # Silent fallback
                pass
    
    def add_static_text(self):
        """Add static text elements"""
        # App title
        self.canvas.create_text(54.0, 8.0, anchor="nw", text="NeuroLens",
                               fill="#FFFFFF", font=("Arial", 18, "bold"))
        
        # Navigation with proper highlighting
        nav_items = [
            ("DashBoard", 91, False),
            ("Alerts", 127, False),
            ("Help/Info", 167, True),   # ACTIVE page
            ("Log Out", 207, False)
        ]
        
        for text, y, is_active in nav_items:
            color = "#4277FF" if is_active else "#FFFFFF"
            weight = "bold" if is_active else "normal"
            self.canvas.create_text(57.0, y, anchor="nw", text=text,
                                   fill=color, font=("Arial", 12, weight))
        
        # FIXED - Added proper breadcrumb like Dashboard
        self.canvas.create_text(294.0, 24.0, anchor="nw", text="Help/Info  /    User Guide",
                               fill="#FFFFFF", font=("Arial", 11))
    
    def setup_search_entry(self):
        """FIXED - Add search entry like other pages"""
        self.search_entry = Entry(
            self, bd=1, bg="#2D2D2D", fg="#999999",
            insertbackground="#FFFFFF", font=("Arial", 11)
        )
        self.search_entry.place(x=590.0, y=13.0, width=266.0, height=28.0)
        self.search_entry.insert(0, "Search help topics...")
        
        self.search_entry.bind("<FocusIn>", self.on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_search_focus_out)
        self.search_entry.bind("<KeyRelease>", self.on_search)
    
    def setup_help_content(self):
        """Setup help content with proper title"""
        # Help content frame
        content_frame = Frame(self, bg="#2A2F3A", relief="flat", bd=2)
        content_frame.place(x=300, y=100, width=500, height=450)
        
        # Header with title like other pages
        header_frame = Frame(content_frame, bg="#4277FF", height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        Label(header_frame, text="NeuroLens User Guide", 
              bg="#4277FF", fg="#FFFFFF", 
              font=("Arial", 16, "bold")).pack(pady=12)
        
        # Scrollable text content
        text_frame = Frame(content_frame, bg="#2A2F3A")
        text_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.help_text = Text(
            text_frame, wrap="word", bg="#2A2F3A", fg="#FFFFFF",
            font=("Arial", 11), relief="flat", padx=15, pady=10
        )
        
        scrollbar = Scrollbar(text_frame, command=self.help_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.help_text.config(yscrollcommand=scrollbar.set)
        self.help_text.pack(side="left", fill="both", expand=True)
        
        # Help content
        help_content = """GETTING STARTED

Welcome to NeuroLens - your drowsiness monitoring system!

DASHBOARD FEATURES
• Drowsiness Level: Shows alertness (1-5 scale)
• Battery Status: Real-time battery monitoring  
• Performance Analytics: Weekly performance trends
• Session Timer: Current session duration
• Device Connectivity: Connection status

ALERTS SYSTEM
• Real-time drowsiness detection
• Clickable alert details
• User profile information
• Export functionality

ALERT TYPES
• Eyes Closed: 3+ seconds detection
• Head Nodding: Movement detection
• Low Blink Rate: Frequency monitoring
• Micro-sleep: Brief sleep episodes

INTERACTIVE FEATURES
• Click alert titles for details
• Click usernames for profiles
• Search alerts by various criteria
• Export data to CSV format

TIPS FOR OPTIMAL USE
• Ensure good lighting conditions
• Keep sensors clean
• Take breaks when alerted
• Review alert patterns regularly

TROUBLESHOOTING
• Check device connection
• Verify sensor positioning
• Restart if needed
• Contact support for issues

SUPPORT CONTACT
Email: support@neurolens.com
Phone: +27 21 555 1234

Version: 2.0.0 (2025)"""
        
        self.help_text.insert("1.0", help_content)
        self.help_text.config(state="disabled")
    
    def on_search_focus_in(self, event):
        if self.search_entry.get() == "Search help topics...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="#FFFFFF", bg="#3A404D")
    
    def on_search_focus_out(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search help topics...")
            self.search_entry.config(fg="#999999", bg="#2D2D2D")
    
    def on_search(self, event):
        """Handle help search"""
        search_term = self.search_entry.get().lower()
        
        if search_term and search_term != "search help topics...":
            self.help_text.config(state="normal")
            self.help_text.tag_remove("search_highlight", "1.0", "end")
            self.help_text.tag_configure("search_highlight", background="#FFFF00", foreground="#000000")
            
            # Search and highlight
            start_pos = "1.0"
            match_count = 0
            
            while True:
                pos = self.help_text.search(search_term, start_pos, "end", nocase=True)
                if not pos:
                    break
                
                end_pos = f"{pos}+{len(search_term)}c"
                self.help_text.tag_add("search_highlight", pos, end_pos)
                start_pos = end_pos
                match_count += 1
            
            if match_count > 0:
                first_match = self.help_text.search(search_term, "1.0", "end", nocase=True)
                if first_match:
                    self.help_text.see(first_match)
            
            self.help_text.config(state="disabled")
        else:
            self.help_text.config(state="normal")
            self.help_text.tag_remove("search_highlight", "1.0", "end")
            self.help_text.config(state="disabled")
    
    def on_page_show(self):
        print("Help page shown")