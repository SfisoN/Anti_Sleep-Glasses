
````markdown
# NeuroLens - Anti-Sleep Glasses Dashboard

A comprehensive desktop application for monitoring drowsiness and managing anti-sleep smart glasses data in real-time.

## 🚀 Quick Start

```bash
python App.py
````

## 📁 Project Structure

```
NeuroLens/
│
├── App.py                 # Main application entry point
├── Pages/                 # Application pages/screens
│   ├── DashBoard.py       # Main dashboard with real-time data
│   ├── Alerts.py          # Alerts management and history
│   └── Help.py            # Help and user guide
├── Assets/                # UI Assets and images
│   ├── Dashboard/         # Dashboard page assets
│   │   ├── image_1.png to image_30.png
│   │   └── entry_1.png
│   └── Alerts/            # Alerts page assets
│       ├── image_1.png to image_16.png
│       ├── entry_1.png
│       └── button_1.png
|___Sensor.py
└── README.md              # This file
```

## 🔧 Current Application Features

### 🏠 **App.py (Main Controller)**

**Current State:** ✅ Functional

* **Purpose:** Main application window and navigation controller
* **Features:**

  * Window management (1200x699 resolution)
  * Page navigation between Dashboard, Alerts, and Help
  * Sidebar navigation with consistent styling
  * Logout functionality with confirmation

**Key Components:**

```python
class NeuroLensApp:
    - window: Main tkinter window
    - container: Frame container for all pages
    - pages: Dictionary storing page instances
    - sidebar buttons: Navigation interface
```

---

### 📊 **DashBoard.py (Main Dashboard)**

**Current State:** ⚠️ Partially Functional (Missing IoT Integration)

**Current Features:**

* Real-time drowsiness level display
* Battery percentage monitoring
* Recent activity timeline
* Statistical charts (pie chart for drowsiness breakdown)
* Monthly trends (line chart)
* User activity rankings
* Dynamic logout counter

**TODO / Missing Features:**

```python
# Data Sources Needed:
self.drowsiness_level = "Drowsy"     # TODO: Connect to IoT glasses
self.battery_percentage = 78         # TODO: Get from glasses battery
activities = [
    "Drowsiness Detected 14:52 pm",  # TODO: Get from glasses
    "Blinked 23/min at 14:12pm",     # TODO: Get from glasses sensor
]
```

**Charts & Analytics:**

* Matplotlib integration for data visualization
* Pie chart: Drowsiness event breakdown
* Line chart: Monthly trend analysis
* Statistics: Alert accuracy, weekly trends

---

### ⚠️ **Alerts.py (Alert Management)**

**Current State:** ✅ Mostly Functional

**Features:**

* Alert history display (sample data provided)
* Search functionality for filtering alerts
* CSV export capability
* Alert categorization (Drowsiness, Blink Rate, Micro-sleep)

**Sample Alert Data Structure:**

```python
{
    "title": "Drowsiness Alert #001",
    "username": "John Doe",
    "condition": "Eyes closed for 3+ seconds", 
    "action": "Audio alarm triggered",
    "response": "User acknowledged",
    "date": "2025-01-15 14:52"
}
```

**Known Issues:**

* ❌ Sidebar alignment with icons
* ❌ Export button text not visible
* ⚠️ Search function logs to console (needs UI feedback)

---

### ❓ **Help.py (User Guide)**

**Current State:** ⚠️ Needs Improvement

**Current Features:**

* User guide content display
* Scrollable text area
* Consistent navigation elements

**Known Issues:**

* ❌ Scrollbar not properly sized
* ❌ Background inconsistent with other pages
* ❌ Content positioning issues

---

## 🔧 Technical Requirements

### Dependencies

```python
# Built-in Python modules
import tkinter as tk
from tkinter import Canvas, Entry, PhotoImage, Button, messagebox, filedialog
import csv
from datetime import datetime
from pathlib import Path

# External dependencies (install via pip)
pip install matplotlib
pip install numpy
```

### System Requirements

* Python 3.7+
* Windows/macOS/Linux

---

## 🛠️ Current Issues & Fixes Needed

### High Priority


### Medium Priority

4. **Settings Dropdown Functionality**

   * Add click handler for settings icon
   * Suggested settings: Sensitivity, Volume, Vibration, Battery Saver, Auto-Sleep, Calibration

5. **Sidebar Collapse Feature**

   * Add hamburger menu to collapse/expand sidebar
   * Benefit: More screen space for content

---

## 🔌 IoT Integration Points

### Hardware Connections (planned)

```python
class GlassesInterface:
    def get_drowsiness_level(): ...
    def get_battery_level(): ...
    def get_blink_rate(): ...
    def get_head_position(): ...
    def send_alert(alert_type): ...
```

### Data Flow

```
Smart Glasses → Bluetooth/WiFi → Python App → SQLite DB → UI Display
                                     ↓
                               Real-time Updates
                                     ↓
                              Dashboard Charts/Alerts
```

---

## 🎨 UI/UX Suggestions

### Short Term

* Responsive design
* Dark mode toggle
* Page animations
* Real-time WebSocket updates
* System tray notifications

### Long Term

* Analytics dashboard (weekly/monthly reports)
* Multi-user profiles
* Customizable alert thresholds
* Export (PDF, JSON, Excel)
* Cloud sync

---

## 🚀 Development Roadmap

**Phase 1 (Week 1): Bug Fixes**

* Sidebar alignment ✅
* Export button text ✅
* Help page layout ✅
* Settings dropdown ✅

**Phase 2 (Week 2-3): Hardware Integration**

* Bluetooth/WiFi connection 🔄
* Real-time data streaming 🔄
* Alert system 🔄
* Battery monitoring 🔄

---

## 📞 Support & Documentation

### Developers

* Inline code comments
* Meaningful variable names
* Error handling for hardware

### Users

* Help system in `Help.py`
* Tooltips for UI elements
* User manual (planned)

---

## 🏃‍♂️ Running the Application

### Development Mode

```bash
# Clone/download the project
cd NeuroLens

# Install dependencies  
pip install matplotlib numpy

# Run the application
python App.py
```

### Production Deployment

```bash
# Create executable
pip install pyinstaller
pyinstaller --windowed --onefile App.py

# Or build installer
pip install cx_Freeze
# Create setup.py and build
```

---

**Version:** 1.0.0 (September 2025)
**Maintainer:** NeuroLens Development Team
**Status:** Development Phase

```

---


