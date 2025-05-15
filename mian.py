"""This is a simple Python program that will make staff at a takeaway place be 
able to make orders with ese and be able to see the order number, item price and
total price.
By: Matt Smith                                                     08/05/2025"""

# import modules
import tkinter as tk
from tkinter import messagebox
import sqlite3

# constants
DATABASE = "database-L2DTSD-2025.db"

# global variables
bg_color = "#5c9ead"
label_color = "#236273"
white = "#ffffff"
exit = False
is_visable = "*"

# functions
def error_message(msg):
    """Display an error message."""
    messagebox.showerror("Error", msg)

def show_password():
    """show the password"""
    global is_visable
    if is_visable == "*":
        is_visable = ""
        password_entry.config(show=is_visable)
        show_password.config(text="Hide Password")
    else:
        is_visable = "*"
        password_entry.config(show=is_visable)
        show_password.config(text="Show Password")

def login():
    """Check if the username and password are correct."""
    with sqlite3.connect(DATABASE) as d_b:
        print(username_entry.get())
        print(password_entry.get())
        cursor = d_b.cursor()
        qrl = f"""SELECT name FROM staff WHERE username = "{username_entry.get()}" 
        AND password = "{password_entry.get()}";"""
        cursor.execute(qrl)
        results = cursor.fetchall()
        print(results)
        if not results == []:
            messagebox.showinfo("Login", "Login successful!")
            window.destroy()
            # Call the main function here
        else:
            messagebox.showerror("Login", "Invalid username or password.")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

# login window
while exit == False:
    while True:
        try:
            # Connect to the database
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            break
        except sqlite3.Error as e:
            error_message(f"Database connection error: {e}")
            break

    # Create the login window
    window = tk.Tk()
    window.title("Login Window")
    window.geometry("1000x650")
    window.config(bg=bg_color)
    window.resizable(width=False, height=False)

    # Create the mian Frame
    frame = tk.Frame(master=window, bg=label_color)
    frame.place(x=200, y=25, width=600, height=600)

    # show password button
    show_password = tk.Button(frame, text="Show Password", font=('Arial', 12), 
                              bg=white, command=show_password)
    show_password.place(x=350, y=300)

    # Create the login feilds
    username_label = tk.Label(frame, text="Username", font=('Arial',15,"bold"), 
                              bg=label_color) 
    username_entry = tk.Entry(frame, width=75)
    password_label = tk.Label(frame, text="Password", font=('Arial',15,"bold"), 
                              bg=label_color)
    password_entry = tk.Entry(frame, show=is_visable, width=75)
    username_entry.place(x=25, y=130)
    username_label.place(x=50, y=100)
    password_entry.place(x=25, y=230)
    password_label.place(x=50, y=200)
    
    # Create the login button
    login_button = tk.Button(frame, text="login", font=('Arial', 15,"bold"), 
                             bg=white, width=10, height=2, command=login)
    login_button.place(x=225, y=400)
    window.mainloop()

    # exit the program if the user clicks the exit button
    exit = messagebox.askokcancel("Exit", "Are you sure you want to exit?")
