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
menu = 2
staff_id = 0
text_color = "black"
order_id = 0
total_price = 0.0
order_no = 0

# functions
def error_message(msg):
    """Display an error message"""
    messagebox.showerror("Error", msg)

def order_finish():
    """Finish the order and display a message"""
    global staff_id, order_id, total_price, order_no
    with sqlite3.connect(DATABASE) as d_b:
        cursor = d_b.cursor()
        # Insert the order into the orders table
        qrl = f"""INSERT INTO [order] VALUES ({staff_id}, {total_price}, 
        {order_id}, {order_no});"""
        cursor.execute(qrl)
        d_b.commit()
    messagebox.showinfo("Order Finished", "Your order has been finished.")

def button_text(row,column):
    """Get the text for the keypad buttons"""
    with sqlite3.connect(DATABASE) as d_b:
        cursor = d_b.cursor()
        qrl = f"""SELECT text FROM key_pad where row = {row} and Column = 
        {column};"""
        cursor.execute(qrl)
        result = cursor.fetchall()
    return result[0][0]

def item_text(row,column):
    """Get the text for the item grid buttons"""	
    with sqlite3.connect(DATABASE) as d_b:
        cursor = d_b.cursor()
        qrl = f"""SELECT product_name FROM products where row = {row} and 
        Column = {column};"""
        cursor.execute(qrl)
        result = cursor.fetchall()
    return result[0][0]

def on_button_click(row, column, window):
    """Handle button click events"""
    messagebox.showinfo("Button Clicked", f"Row {row}, Column {column}")

def on_item_grid_click(row, column, lb_total_price, lb_item_price):
    """Handle item grid button click events"""
    global deplay_list
    # get the product details from the database
    with sqlite3.connect(DATABASE) as d_b:
        cursor = d_b.cursor()
        qrl = f"""SELECT product_plu, product_name, product_price, 
        product_catogory FROM products WHERE row = {row} and Column = 
        {column};"""
        cursor.execute(qrl)
        result = cursor.fetchall()
        deplay_list = result
    
    # update the display bar
    total_price_update(lb_total_price)
    item_price_update(lb_item_price)

def key_pad(window):
    """display the keypad"""
    global bg_color, label_color, white
    rframe = tk.Frame(master=window, bg=bg_color)
    rframe.place(x=650, y=15, width=350, height=600)

    for i in range(6):
        for j in range(3):
            frame = tk.Frame(master=rframe, relief=tk.RAISED, borderwidth=1, 
                             bg="white")
            frame.grid(row=i,column=j,padx=8,pady=8)
            text = button_text(i,j)
            button = tk.Button(master=frame, text=text, cursor="hand2", 
                               width=11, height=4, command=lambda i=i,j=j,
                               window=window: on_button_click(i, j, window))
            button.pack()
    button_finish = tk.Button(master=window, text="Finish order", 
                              cursor="hand2", command=order_finish)
    button_finish.place(x=640, y=570, width=350, height=30)

def item_grid(window, lb_total_price, lb_item_price):
    """display the keypad"""
    global bg_color, label_color, white
    dframe = tk.Frame(master=window, bg=bg_color)
    dframe.place(x=25, y=170, width=550, height=420)
    for i in range(5):
        for j in range(4):
            frame = tk.Frame(master=dframe, relief=tk.RAISED, borderwidth=1, 
                             bg="white")
            frame.grid(row=i,column=j,padx=15,pady=5)
            text = item_text(i,j)
            button = tk.Button(master=frame, text=text, cursor="hand2", 
                               width=13, height=4, command=lambda i=i,j=j,
                               lb_total_price=lb_total_price, 
                               lb_item_price=lb_item_price: on_item_grid_click(
                                i, j, lb_total_price, lb_item_price))
            button.pack()

def main_menu():
    """Display the main menu"""
    global exit
    while exit == False:
        # Create the main menu window
        window = tk.Tk()
        window.title("Login Window")
        window.geometry("1000x650")
        window.config(bg=bg_color)
        window.resizable(width=False, height=False)

        # Create the right menu frame
        key_pad(window)

        # create the left menu frame
        lframe = tk.Frame(master=window, bg=label_color)

        window.mainloop()

        # exit the program if the user clicks the exit button
        exit = messagebox.askokcancel("Exit", "Are you sure you want to exit?")

def sub_menu():
    """Display the sub menu"""
    global exit, bg_color, label_color, white, text_color
    while exit == False:
        # Create the main menu window
        window = tk.Tk()
        window.title("Login Window")
        window.geometry("1000x650")
        window.config(bg=bg_color)
        window.resizable(width=False, height=False)

        # Create the right menu frame
        key_pad(window, lb_total_price, lb_item_price)

        # create the left menu frame
        lframe = tk.Frame(master=window,bg="white")
        lframe.place(x=15,y=15,width=600,height=620)
        lb_total_price = tk.Label(master=lframe, text="Total Price", 
                                  font=('Arial',12,"bold"), fg=text_color, 
                                  bg=white)
        lb_item_price = tk.Label(master=lframe, text="Item Price", 
                                 font=('Arial',12,"bold"), fg=text_color, 
                                 bg=white)
        lb_order_no = tk.Label(master=lframe, text="Order No", 
                               font=('Arial',12,"bold"), fg=text_color, 
                               bg=white)
        tbox_total_price = tk.Text(master=lframe, width=18, height=2, 
                                   state="disabled", borderwidth=2, bg=bg_color)
        tbox_item_price = tk.Text(master=lframe, width=18, height=2, 
                                  state="disabled", borderwidth=2, bg=bg_color)
        tbox_order_no = tk.Text(master=lframe, width=18, height=2, 
                                state="disabled", borderwidth=2, bg=bg_color)
        R_desplay_bar = tk.Text(master=lframe, width=22, height=2, 
                                state="disabled", borderwidth=2, bg=bg_color)
        l_desplay_bar = tk.Text(master=lframe, width=45, height=2, 
                                state="disabled", borderwidth=2, bg=bg_color)
        
        item_grid(window, lb_total_price, lb_item_price)
        
        # place all the widgets in the frame
        lb_total_price.place(x=50,y=15)
        lb_item_price.place(x=240,y=15)
        lb_order_no.place(x=440,y=15)
        tbox_total_price.place(x=15,y=50)
        tbox_item_price.place(x=210,y=50)
        tbox_order_no.place(x=405,y=50)
        R_desplay_bar.place(x=380,y=100)
        l_desplay_bar.place(x=15,y=100)

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
    """Check if the username and password are correct"""
    global login, staff_id
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
            
            # get the staff id
            qrl = f"""SELECT staff_id FROM staff WHERE username = 
            "{username_entry.get()}" AND password = "{password_entry.get()}";"""
            cursor.execute(qrl)
            results = cursor.fetchall()
            staff_id = results[0][0]

            # close the login window
            window.destroy()
            login = True
        else:
            messagebox.showerror("Login", "Invalid username or password.")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

while __name__ == "__main__":
    """Create the login window"""
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
