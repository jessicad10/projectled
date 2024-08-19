import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime, timedelta
 
# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('traffic_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS drivers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        license_number TEXT NOT NULL UNIQUE,
        registration_date DATE NOT NULL
    )
    ''')
    conn.commit()
    conn.close()
 
# Database functions
def add_driver(name, license_number, registration_date):
    conn = sqlite3.connect('traffic_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO drivers (name, license_number, registration_date)
    VALUES (?, ?, ?)
    ''', (name, license_number, registration_date))
    conn.commit()
    conn.close()
def get_all_drivers():
    conn = sqlite3.connect('traffic_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM drivers')
    drivers = cursor.fetchall()
    conn.close()
    return drivers
 
def get_drivers_by_date_range(start_date, end_date):
    conn = sqlite3.connect('traffic_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM drivers
    WHERE registration_date BETWEEN ? AND ?
    ''', (start_date, end_date))
    drivers = cursor.fetchall()
    conn.close()
    return drivers
 
# Tkinter setup
def update_driver_list(drivers):
    # Clear existing content
    for widget in content_frame.winfo_children():
        widget.destroy()
   
    # Display driver data
    for i, driver in enumerate(drivers):
        text = f"ID: {driver[0]}\nName: {driver[1]}\nLicense: {driver[2]}\nDate: {driver[3]}"
        label = tk.Label(content_frame, text=text, bg="#f1f1f1", font=("Arial", 12), anchor="w", padx=10)
        label.grid(row=i, column=0, sticky="w", pady=5)

def show_registered_drivers():
    drivers = get_all_drivers()
    update_driver_list(drivers)
        
def show_last_month_registered():
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    drivers = get_drivers_by_date_range(start_date, end_date)
    update_driver_list(drivers)
 
def show_last_year_registered():
    end_date = datetime.now().date()
    start_date = end_date.replace(year=end_date.year - 1)
    drivers = get_drivers_by_date_range(start_date, end_date)
    update_driver_list(drivers)
 
# Initialize the database
init_db()
 
# Tkinter root window
root = tk.Tk()
root.title("Dashboard")
root.state('zoomed')  # Maximize the window to cover the full screen
root.configure(bg="#f1f1f1")  # Background color of the right side
 
# Left Frame for the menu
menu_frame = tk.Frame(root, width=250, bg="#2d4b6f")
menu_frame.pack(side="left", fill="y")
# Menu items (without icons)
menu_items = ["Dashboard", "Add driver", "View driver"]
 
for item in menu_items:
    label = tk.Label(menu_frame, text=item, font=("Arial", 16), bg="#2d4b6f", fg="white", anchor="w", padx=20)
    label.pack(fill="x", pady=10)
 
# Right Frame for the content
content_frame = tk.Frame(root, bg="#f1f1f1")
content_frame.pack(side="right", expand=True, fill="both", padx=50, pady=50)
 
# Buttons in the content area
button_data = [
    {"text": "Registered Driver", "bg": "#c26d42", "command": show_registered_drivers},
    {"text": "Last month registered", "bg": "#ba4a46", "command": show_last_month_registered},
    {"text": "Last year registered", "bg": "#86b8a1", "command": show_last_year_registered}
]
 
for i, data in enumerate(button_data):
    button = tk.Button(content_frame, text=data["text"], font=("Arial", 14), bg=data["bg"], fg="white", width=20, height=10, command=data["command"])
    button.grid(row=0, column=i, padx=20, pady=20)
 
root.mainloop()

 