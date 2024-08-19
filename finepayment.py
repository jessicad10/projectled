import tkinter as tk
from tkinter import ttk
import sqlite3
 
# Connect to SQLite database (or create it if it doesn't exist)
def init_db():
    conn = sqlite3.connect('fines.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        license_id TEXT NOT NULL,
        full_name TEXT NOT NULL,
        chit_no TEXT NOT NULL,
        payment_method TEXT
    )
    ''')
    conn.commit()
    conn.close()
 
def submit_payment():
    license_id = license_id_entry.get()
    full_name = full_name_entry.get()
    chit_no = chit_no_entry.get()
    payment_method = payment_method_var.get()
   
    if not (license_id and full_name and chit_no and payment_method):
        tk.messagebox.showerror("Input Error", "All fields must be filled.")
        return
    conn = sqlite3.connect('fines.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO fines (license_id, full_name, chit_no, payment_method)
    VALUES (?, ?, ?, ?)
    ''', (license_id, full_name, chit_no, payment_method))
    conn.commit()
    conn.close()
   
    tk.messagebox.showinfo("Success", "Payment submitted successfully!")
 
# Initialize database
init_db()
 
# Create the main application window
root = tk.Tk()
root.title("Fine Payment")
root.state('zoomed')  # Maximize the window to cover the full screen
root.configure(bg="#dcdcdc")  # Background color of the right side
 
# Left Frame for the menu
menu_frame = tk.Frame(root, width=250, bg="#2d4b6f")
menu_frame.pack(side="left", fill="y")
 
# Menu items (without icons)
menu_items = ["Dashboard", "Driver's pending fine", "Drivers paid fine", "Provision details"]
for item in menu_items:
    label = tk.Label(menu_frame, text=item, font=("Arial", 16), bg="#2d4b6f", fg="white", anchor="w", padx=20)
    label.pack(fill="x", pady=10)
 
# Right Frame for the fine payment form
form_frame = tk.Frame(root, bg="#dcdcdc")
form_frame.pack(side="right", expand=True, fill="both")
 
# Fine Payment Label
payment_label = tk.Label(form_frame, text="Fine Payment", font=("Arial", 24), bg="#dcdcdc", anchor="w")
payment_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")
 
# Form fields
fields = ["License ID", "Drivers full name", "Chit no"]
field_entries = {}
for i, field in enumerate(fields):
    label = tk.Label(form_frame, text=field, font=("Arial", 14), bg="#dcdcdc", anchor="w")
    label.grid(row=i+1, column=0, padx=20, pady=10, sticky="w")
   
    entry = ttk.Entry(form_frame, width=50, font=("Arial", 14))
    entry.grid(row=i+1, column=1, padx=20, pady=10)
    field_entries[field] = entry
 
license_id_entry = field_entries["License ID"]
full_name_entry = field_entries["Drivers full name"]
chit_no_entry = field_entries["Chit no"]
# Payment Options Label
payment_option_label = tk.Label(form_frame, text="Payment option", font=("Arial", 14), bg="#dcdcdc", anchor="w")
payment_option_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
 
# Payment Options
options_frame = tk.Frame(form_frame, bg="#dcdcdc")
options_frame.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="w")
 
payment_method_var = tk.StringVar()
 
payment_methods = ["Esewa", "Khalti"]
for i, method in enumerate(payment_methods):
    option_button = tk.Radiobutton(options_frame, text=method, variable=payment_method_var, value=method,
    font=("Arial", 14), bg="#dcdcdc", fg="#2d4b6f")
    option_button.grid(row=i, column=0, padx=10, pady=10, sticky="w")
 
# Submit Button
submit_button = tk.Button(form_frame, text="Submit Payment", font=("Arial", 14), bg="#2d4b6f", fg="white", padx=20, pady=10, command=submit_payment)
submit_button.grid(row=6, column=0, columnspan=2, pady=20)
 
root.mainloop()