import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import requests
import json


def canteen_table():
    table_window = tk.Toplevel(window)
    table_window.title("All canteens")
    table = ttk.Treeview(table_window, columns=("ID", "Name", "Location", "time_open", "time_closed"), show="headings")
    table.heading("ID", text="ID")
    table.heading("Name", text="Name")
    table.heading("Location", text="Location")
    table.heading("time_open", text="Opens at")
    table.heading("time_closed", text="Closes at")
    table.pack()

    r = requests.get("http://127.0.0.1:5000/canteens")
    data = json.loads(r.text)
    for item in data:
        id = item["ID"]
        name = item["Name"]
        location = item["Location"]
        time_open = item["time_open"]
        time_closed = item["time_closed"]
        table.insert(parent="", index="end", values=(id, name, location, time_open, time_closed))


def sort_by_working_hours():
    # Logic for sorting canteens by working hours
    try:
        from_entry_time = datetime.strptime(from_entry.get(), "%H:%M")
        to_entry_time = datetime.strptime(to_entry.get(), "%H:%M")
    except ValueError:
        messagebox.showwarning(title="Error", message="Please enter a valid time format (HH:mm)!")
        return False

    table_window = tk.Toplevel(window)
    table_window.title("Canteens filtered by time")
    table = ttk.Treeview(table_window, columns=("ID", "Name", "Location", "time_open", "time_closed"), show="headings")
    table.heading("ID", text="ID")
    table.heading("Name", text="Name")
    table.heading("Location", text="Location")
    table.heading("time_open", text="Opens at")
    table.heading("time_closed", text="Closes at")
    table.pack()

    r = requests.get(f"http://127.0.0.1:5000/canteens/{from_entry.get()}-{to_entry.get()}")
    data = json.loads(r.text)
    for item in data:
        id = item["ID"]
        name = item["Name"]
        location = item["Location"]
        time_open = item["time_open"]
        time_closed = item["time_closed"]
        table.insert(parent="", index="end", values=(id, name, location, time_open, time_closed))


def add_new_canteen():
    # Logic for adding a new canteen
    name = name_entry.get()
    location = location_entry.get()
    time_open = opens_at_entry.get()
    time_closed = closes_at_entry.get()
    if name and location and time_open and time_closed:
        try:
            from_entry_time = datetime.strptime(opens_at_entry.get(), "%H:%M")
            to_entry_time = datetime.strptime(closes_at_entry.get(), "%H:%M")
        except ValueError:
            messagebox.showwarning(title="Error", message="Please enter a valid time format (HH:mm)!")
            return False

        payload = {"Name": name, "Location": location, "time_open": time_open, "time_closed": time_closed}
        r = requests.post("http://127.0.0.1:5000/canteens", json=payload)
        messagebox.showinfo(title="Info", message=json.loads(r.text)["Message"])
        if json.loads(r.text)["Message"] == "Canteen added successfully!":
            name_entry.delete(0, tk.END)
            location_entry.delete(0, tk.END)
            opens_at_entry.delete(0, tk.END)
            closes_at_entry.delete(0, tk.END)
    else:
        messagebox.showwarning(title="Error", message="Please fill all the entry fields!")
        return False


def edit_canteen():
    # Logic for editing a canteen
    id = id_edit_entry.get()
    name = name_edit_entry.get()
    location = location_edit_entry.get()
    time_open = opens_at_edit_entry.get()
    time_closed = closes_at_edit_entry.get()
    if id and name and location and time_open and time_closed:
        try:
            from_entry_time = datetime.strptime(opens_at_edit_entry.get(), "%H:%M")
            to_entry_time = datetime.strptime(closes_at_edit_entry.get(), "%H:%M")
        except ValueError:
            messagebox.showwarning(title="Error", message="Please enter a valid time format (HH:mm)!")
            return False

        payload = {"Name": name, "Location": location, "time_open": time_open, "time_closed": time_closed}
        r = requests.put(f"http://127.0.0.1:5000/canteens/{id}", json=payload)
        messagebox.showinfo(title="Info", message=json.loads(r.text)["Message"])
        if json.loads(r.text)["Message"] == "Canteen updated successfully!":
            id_edit_entry.delete(0, tk.END)
            name_edit_entry.delete(0, tk.END)
            location_edit_entry.delete(0, tk.END)
            opens_at_edit_entry.delete(0, tk.END)
            closes_at_edit_entry.delete(0, tk.END)
    else:
        messagebox.showwarning(title="Error", message="Please fill all the entry fields!")
        return False


def delete_canteen():
    # Logic for deleting a canteen
    id = delete_entry.get()

    if id:
        r = requests.delete(f"http://127.0.0.1:5000/canteens/{id}")
        messagebox.showinfo(title="Info", message=json.loads(r.text)["Message"])
        if json.loads(r.text)["Message"] == "Canteen deleted successfully!":
            delete_entry.delete(0, tk.END)
    else:
        messagebox.showwarning(title="Error", message="Please fill all the entry fields!")


window = tk.Tk()
window.title("University canteen database")
width = 700
height = 400
x = window.winfo_screenwidth() // 2 - width // 2
y = window.winfo_screenheight() // 2 - height // 2
window.geometry(f"{width}x{height}+{x}+{y}")

# Create buttons
btn_all_canteens = tk.Button(window, text="All canteens", command=canteen_table)
btn_sort_by_working_hours = tk.Button(window, text="Sort by working hours", command=sort_by_working_hours)
btn_add_new_canteen = tk.Button(window, text="Add new canteen", command=add_new_canteen)
btn_edit_canteen = tk.Button(window, text="Edit canteen", command=edit_canteen)
btn_delete_canteen = tk.Button(window, text="Delete canteen", command=delete_canteen)

# Arrange buttons
btn_all_canteens.grid(row=0, column=0, sticky='ew')
btn_sort_by_working_hours.grid(row=0, column=1, sticky='ew')
btn_add_new_canteen.grid(row=0, column=2, sticky='ew')
btn_edit_canteen.grid(row=0, column=3, sticky='ew')
btn_delete_canteen.grid(row=0, column=4, sticky='ew')

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=1)
window.columnconfigure(4, weight=1)
# window.rowconfigure(0, weight=1)
# window.rowconfigure(1, weight=1)
# window.rowconfigure(2, weight=1)
# window.rowconfigure(3, weight=1)
# window.rowconfigure(4, weight=1)
# window.rowconfigure(5, weight=1)
# window.rowconfigure(6, weight=1)
# window.rowconfigure(7, weight=1)
# window.rowconfigure(8, weight=1)
# window.rowconfigure(9, weight=1)
# window.rowconfigure(10, weight=1)

# Create and arrange labels and entry fields for 'Sort by working hours'
from_label = tk.Label(window, text="From:")
from_label.grid(row=1, column=1)
from_entry = tk.Entry(window)
from_entry.grid(row=2, column=1)

to_label = tk.Label(window, text="To:")
to_label.grid(row=3, column=1)
to_entry = tk.Entry(window)
to_entry.grid(row=4, column=1)

# Create and arrange labels and entry fields for 'Add new canteen'
name_label = tk.Label(window, text="Name:")
name_label.grid(row=1, column=2)
name_entry = tk.Entry(window)
name_entry.grid(row=2, column=2)

location_label = tk.Label(window, text="Location:")
location_label.grid(row=3, column=2)
location_entry = tk.Entry(window)
location_entry.grid(row=4, column=2)

opens_at_label = tk.Label(window, text="Opens at:")
opens_at_label.grid(row=5, column=2)
opens_at_entry = tk.Entry(window)
opens_at_entry.grid(row=6, column=2)

closes_at_label = tk.Label(window, text="Closes at:")
closes_at_label.grid(row=7, column=2)
closes_at_entry = tk.Entry(window)
closes_at_entry.grid(row=8, column=2)

# Create and arrange labels and entry fields for 'Edit canteen'
id_edit_label = tk.Label(window, text="ID:")
id_edit_label.grid(row=1, column=3)
id_edit_entry = tk.Entry(window)
id_edit_entry.grid(row=2, column=3)

name_edit_label = tk.Label(window, text="Name:")
name_edit_label.grid(row=3, column=3)
name_edit_entry = tk.Entry(window)
name_edit_entry.grid(row=4, column=3)

location_edit_label = tk.Label(window, text="Location:")
location_edit_label.grid(row=5, column=3)
location_edit_entry = tk.Entry(window)
location_edit_entry.grid(row=6, column=3)

opens_at_edit_label = tk.Label(window, text="Opens at:")
opens_at_edit_label.grid(row=7, column=3)
opens_at_edit_entry = tk.Entry(window)
opens_at_edit_entry.grid(row=8, column=3)

closes_at_edit_label = tk.Label(window, text="Closes at:")
closes_at_edit_label.grid(row=9, column=3)
closes_at_edit_entry = tk.Entry(window)
closes_at_edit_entry.grid(row=10, column=3)

# Create and arrange labels and entry fields for 'Delete canteen'
delete_label = tk.Label(window, text="ID:")
delete_label.grid(row=1, column=4)
delete_entry = tk.Entry(window)
delete_entry.grid(row=2, column=4)

window.mainloop()
