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
login = False
is_visable = "*"
menu = 1

# functions
def error_message(msg):
    """Display an error message."""
    messagebox.showerror("Error", msg)

def main_menu():
    """Display the main menu."""
    global exit
    while exit == False:
        # Create the main menu window
        window = tk.Tk()
        window.title("Login Window")
        window.geometry("1000x650")
        window.config(bg=bg_color)
        window.resizable(width=False, height=False)
        window.mainloop()

        # exit the program if the user clicks the exit button
        exit = messagebox.askokcancel("Exit", "Are you sure you want to exit?")

def sub_menu():
    """Display the sub menu."""
    global exit
    while exit == False:
        # Create the main menu window
        window = tk.Tk()
        window.title("Login Window")
        window.geometry("1000x650")
        window.config(bg=bg_color)
        window.resizable(width=False, height=False)
        window.mainloop()

        # exit the program if the user clicks the exit button
        exit = messagebox.askokcancel("Exit", "Are you sure you want to exit?")

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

def menu_chager():
    """Change the menu"""
    global menu
    if menu == 1:
        # call the main menu
        menu = 2
        main_menu()
    else:
        #call the sub menu
        menu = 1
        sub_menu()

def cheek_login():
    """Check if the username and password are correct."""
    global login
    with sqlite3.connect(DATABASE) as d_b:
        # Check if the username and password are correct
        cursor = d_b.cursor()
        qrl = f"""SELECT name FROM staff WHERE username = "{username_entry.get()}" 
        AND password = "{password_entry.get()}";"""
        cursor.execute(qrl)
        results = cursor.fetchall()
        if not results == []:
            messagebox.showinfo("Login", 
                                f"Login successful! \n Welcome {results[0][0]}")
            window.destroy()
            login = True
        else:
            messagebox.showerror("Login", "Invalid username or password.")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

while __name__ == "__main__":
    """Create the login window."""
    # login window
    while login == False:
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
        show_password = tk.Button(frame, text="Show Password", 
                                  font=('Arial', 12), bg=white, 
                                  command=show_password)
        show_password.place(x=350, y=300)

        # Create the login feilds
        username_label = tk.Label(frame, text="Username", 
                                  font=('Arial',15,"bold"), bg=label_color) 
        username_entry = tk.Entry(frame, width=75)
        password_label = tk.Label(frame, text="Password", 
                                  font=('Arial',15,"bold"), bg=label_color)
        password_entry = tk.Entry(frame, show=is_visable, width=75)
        username_entry.place(x=25, y=130)
        username_label.place(x=50, y=100)
        password_entry.place(x=25, y=230)
        password_label.place(x=50, y=200)
            
        # Create the login button
        login_button = tk.Button(frame, text="login", 
                                 font=('Arial', 15,"bold"), bg=white, 
                                 width=10, height=2, command=cheek_login)
        login_button.place(x=225, y=400)
        window.mainloop()

        if login == False:
            # exit the program if the user clicks the exit button
            exit = messagebox.askokcancel("Exit", "Are you sure you want to exit?")
            login = exit
    
    while True:
        if exit == True:
            break
        # call the menu changer
        menu_chager()

    break