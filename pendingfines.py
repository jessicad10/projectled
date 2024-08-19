from tkinter import ttk, messagebox
import sqlite3
import tkinter as tk
 
# Initialize the database
def initialize_db():
    conn = sqlite3.connect('fines.db')
    cursor = conn.cursor()
   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pending_fines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chit_no TEXT,
            provision TEXT,
            vehicle_no TEXT,
            issue_date TEXT,
            fine_amount REAL
        )
    ''')
   
    conn.commit()
    conn.close()
 
initialize_db()
# Database operations
def add_fine(chit_no, provision, vehicle_no, issue_date, fine_amount):
    conn = sqlite3.connect('fines.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pending_fines (chit_no, provision, vehicle_no, issue_date, fine_amount)
        VALUES (?, ?, ?, ?, ?)
    ''', (chit_no, provision, vehicle_no, issue_date, fine_amount))
    conn.commit()
    conn.close()
 
def fetch_all_fines():
    conn = sqlite3.connect('fines.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pending_fines')
    rows = cursor.fetchall()
    conn.close()
    return rows
 
def update_fine(id, chit_no, provision, vehicle_no, issue_date, fine_amount):
    conn = sqlite3.connect('fines.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE pending_fines
                   SET chit_no = ?, provision = ?, vehicle_no = ?, issue_date = ?, fine_amount = ?
        WHERE id = ?
    ''', (chit_no, provision, vehicle_no, issue_date, fine_amount, id))
    conn.commit()
    conn.close()
 
def delete_fine(id):
    conn = sqlite3.connect('fines.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pending_fines WHERE id = ?', (id,))
    conn.commit()
    conn.close()
 
# Tkinter application
def populate_treeview():
    for row in tree.get_children():
        tree.delete(row)
   
    # Insert a blank row for spacing
    tree.insert("", "end", values=("", "", "", "", "", ""))
   
    fines = fetch_all_fines()
    for fine in fines:
        tree.insert("", "end", values=fine[1:])
 
def add_new_fine():
    # Open a dialog or form to get user input (example values here)
    add_fine("123", "Provision X", "ABC123", "2024-08-01", 150.0)
    populate_treeview()
    messagebox.showinfo("Success", "Fine added successfully")
 
def handle_payment():
    # Implement payment logic here
    messagebox.showinfo("Payment", "Payment functionality is not implemented yet")
 
def on_treeview_select(event):
    selected_item = tree.selection()
    if selected_item:
        item_id = tree.item(selected_item)['values'][0]  # Assuming the ID is in the first column
         # Implement update or delete functionality as needed
        messagebox.showinfo("Info", f"Selected item ID: {item_id}")
 
# Create the main application window
root = tk.Tk()
root.title("Driver's Pending Fine")
root.geometry("1024x600")
root.configure(bg='#e8eaed')
 
# Define colors
side_menu_bg = "#2b4560"
header_bg = "#2b4573"
content_bg = "#e8eaed"
button_bg = "#5a6cae"
text_color = "#000000"
 
# Create the sidebar frame
side_menu = tk.Frame(root, bg=side_menu_bg, width=200)
side_menu.pack(side="left", fill="y")
 
# Sidebar buttons
dashboard_button = tk.Button(side_menu, text="Dashboard", font=("Arial", 12), fg="#ffffff", bg=side_menu_bg, anchor="w", padx=10, pady=10, bd=0)
dashboard_button.pack(fill="x")
pending_fine_button = tk.Button(side_menu, text="Driver's pending fine", font=("Arial", 12), fg="#ffffff", bg=side_menu_bg, anchor="w", padx=10, pady=10, bd=0)
pending_fine_button.pack(fill="x")
 
paid_fine_button = tk.Button(side_menu, text="Drivers paid fine", font=("Arial", 12), fg="#ffffff", bg=side_menu_bg, anchor="w", padx=10, pady=10, bd=0)
paid_fine_button.pack(fill="x")
 
provision_details_button = tk.Button(side_menu, text="Provision details", font=("Arial", 12), fg="#ffffff", bg=side_menu_bg, anchor="w", padx=10, pady=10, bd=0)
provision_details_button.pack(fill="x")
 
# Create the header frame
header = tk.Frame(root, bg=header_bg, height=50)
header.pack(side="top", fill="x")
 
header_label = tk.Label(header, text="Driver's Pending Fine", font=("Arial", 20), fg=text_color, bg=header_bg)
header_label.pack(pady=10)
 
# Create the breadcrumb frame
breadcrumb = tk.Frame(root, bg=content_bg, height=30)
breadcrumb.pack(side="top", fill="x")
breadcrumb_label = tk.Label(breadcrumb, text="Dashboard/ Driver's Pending Fine", font=("Arial", 10), fg=text_color, bg=content_bg)
breadcrumb_label.pack(pady=5, padx=10, anchor="w")
 
# Create the content frame
content = tk.Frame(root, bg=content_bg)
content.pack(side="top", fill="both", expand=True, padx=20, pady=10)
 
# Define columns
columns = ("id", "chit_no", "provision", "vehicle_no", "issue_date", "fine_amount")
 
# Create Treeview widget
tree = ttk.Treeview(content, columns=columns, show='headings', height=15)
tree.pack(fill="both", expand=True)
tree.bind("<ButtonRelease-1>", on_treeview_select)
 
# Define headings
tree.heading("id", text="ID")
tree.heading("chit_no", text="Chit no")
tree.heading("provision", text="Provision")
tree.heading("vehicle_no", text="Vehicle no")
tree.heading("issue_date", text="Issue date")
tree.heading("fine_amount", text="Fine amount")
# Define column width
tree.column("id", width=50)
tree.column("chit_no", width=100)
tree.column("provision", width=150)
tree.column("vehicle_no", width=150)
tree.column("issue_date", width=150)
tree.column("fine_amount", width=150)
 
# Populate Treeview with data from the database
populate_treeview()
 
# Add a placeholder button for "FINE Payment"
payment_button = tk.Button(content, text="FINE Payment", font=("Arial", 12), fg="#ffffff", bg=button_bg, padx=10, pady=5, command=handle_payment)
payment_button.pack(pady=20)
 
# Style Treeview to show gridlines
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 10), foreground="black", background="lightgrey")
style.configure("Treeview", font=("Arial", 10), rowheight=25, borderwidth=1, relief="solid")
style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])  # Remove borders
 
# Run the application
root.mainloop() 