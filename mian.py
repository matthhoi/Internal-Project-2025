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
Show_Password = "Show Password"
menu = 2
staff_id = 0
text_color = "black"
order_id = 0
total_price = 0.0
order_no = 0
deplay_list = [(0, "", 0.0, "", 0)]
order_list = []

# functions
def error_message(msg):
    """Display an error message"""
    messagebox.showerror("Error", msg)

def order_id_no_make():
    """Generate a new order ID/order number"""
    global order_id, order_no
    with sqlite3.connect(DATABASE) as d_b:
        cursor = d_b.cursor()
        # Get the last order ID/no from the database
        qrl = """SELECT MAX(order_id), order_num FROM [order];"""
        cursor.execute(qrl)
        result = cursor.fetchall()
        
        # Increment the last order ID
        if result[0][0] is None:
            # Start from 1 if no orders exist
            order_id = 1
        else:
            # Increment the last order ID
            order_id = result[0][0] + 1

        # Increment the last order number
        if result[0][1] is None:
            # Start from 1 if no orders exist
            order_no = 1
        elif result[0][1] < 100:
            # Increment the last order no
            order_no = result[0][1] + 1
        else:
            # Reset the order number if it exceeds 100
            order_no = 1
        return order_id, order_no

def order_finish():
    """Finish the order and display a message"""
    global staff_id, order_id, total_price, order_no
    with sqlite3.connect(DATABASE) as d_b:
        cursor = d_b.cursor()
        # Insert the order into the orders table
        qrl = f"""INSERT INTO [order] VALUES ({order_id}, {total_price}, 
        {order_no}, {staff_id});"""
        cursor.execute(qrl)
        d_b.commit()
    # Reset the order details
    order_id_no_make()
    messagebox.showinfo("Order Finished", "Your order has been finished.")

def update_details(tbox_total_price, tbox_item_price, l_desplay_bar, 
tbox_order_no, R_desplay_bar):
    """Update the order details"""
    # update the total price text box
    global total_price
    tbox_total_price.config(state='normal')
    tbox_total_price.delete('1.0', tk.END)
    tbox_total_price.insert(tk.END, f"${total_price}")
    tbox_total_price.config(state='disabled')

    # update the item price text box
    global deplay_list
    tbox_item_price.config(state='normal')
    tbox_item_price.delete('1.0', tk.END)
    tbox_item_price.insert(tk.END, f"${deplay_list[0][2]}")
    tbox_item_price.config(state='disabled')

    # update the display bar text box
    l_desplay_bar.config(state='normal')
    l_desplay_bar.delete('1.0', tk.END)
    l_desplay_bar.insert(tk.END, deplay_list[0][1])
    l_desplay_bar.config(state='disabled')

    global order_no
    # update the order number text box
    tbox_order_no.config(state='normal')
    tbox_order_no.delete('1.0', tk.END)
    tbox_order_no.insert(tk.END, order_no)
    tbox_order_no.config(state='disabled')

    # update the right desplay text box
    R_desplay_bar.config(state='normal')
    R_desplay_bar.delete('1.0', tk.END)
    R_desplay_bar.insert(tk.END, "")
    R_desplay_bar.config(state='disabled')

def add_order_list():
    """update the order list"""
    global order_list, deplay_list
    # add the product to the order list
    order_list.append(deplay_list[0])

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

def change_price(new_price, window, tbox_total_price, tbox_item_price, 
l_desplay_bar, tbox_order_no, R_desplay_bar):
    """Change the price of the product"""
    global deplay_list
    decamial = new_price / (10**2)
    deplay_list = [(deplay_list[0][0], deplay_list[0][1], decamial, 
    deplay_list[0][3], deplay_list[0][4])]
    update_details(tbox_total_price, tbox_item_price, l_desplay_bar, 
    tbox_order_no, R_desplay_bar)
    window.destroy()

def on_button_click(row, column, window, tbox_total_price, tbox_item_price, 
l_desplay_bar, tbox_order_no, R_desplay_bar):
    """Handle button click events"""
    global deplay_list
    # get the button details from the database
    text = button_text(row, column)

    if text == "Menu":
        # change the menu
        window.destroy()
        menu_chager()
    elif text == "c":
        # clear the display bar
        deplay_list = [(0, "", 0.0, "product_catogory", 0)]
        update_details(tbox_total_price, tbox_item_price, l_desplay_bar, 
        tbox_order_no, R_desplay_bar)
    elif text == "PLU":
        # get the product details from the database
        plu = R_desplay_bar.get("1.0", tk.END).strip()
        # get the product details from the database
        try:
            with sqlite3.connect(DATABASE) as d_b:
                cursor = d_b.cursor()
                qrl = f"""SELECT product_name, product_price, product_catogory 
                FROM products WHERE product_plu = {plu};"""
                cursor.execute(qrl)
                result = cursor.fetchall()
                deplay_list = [(plu, result[0][0], result[0][1], result[0][2], 
                1)]
        except:
            error_message("ptoduct not found")
        # update the display bar
        update_details(tbox_total_price, tbox_item_price, l_desplay_bar, 
            tbox_order_no, R_desplay_bar)
    elif text == "Add to order":
        # add the product to the order list
        add_order_list()
        # update the total price
        global total_price
        total_price += deplay_list[0][2]
        total_price = round(total_price, 2)
        # update the display bar
        deplay_list = [(0, "", 0.0, "product_catogory", 0)]
        update_details(tbox_total_price, tbox_item_price, l_desplay_bar, 
        tbox_order_no, R_desplay_bar)
    elif text == "Sign out":
        # sign out the user
        global exit
        window.destroy()
        sign_in()
    elif text == "Change price":
        # change the price of the product
        price_window = tk.Tk()
        price_window.title("Change Price Window")
        price_window.geometry("150x150")
        price_window.config(bg=bg_color)
        price_window.resizable(width=False, height=False)

        price_label = tk.Label(master=price_window, text="New Price", 
        bg=bg_color, fg=text_color, font=('Arial', 12, "bold"))
        price_label.pack(pady=10)

        validate_command = price_window.register(lambda p: p.isdigit())
        price_entry = tk.Entry(master=price_window, width=10, validate="key", 
        validatecommand=(validate_command, '%P'))
        price_entry.pack(pady=5)

        change_button = tk.Button(master=price_window, text="Change", 
        cursor="hand2", command=lambda: change_price(float(price_entry.get()), 
        price_window, tbox_total_price, tbox_item_price, l_desplay_bar, 
        tbox_order_no, R_desplay_bar))
        change_button.pack(pady=5)
        price_window.mainloop()

def on_item_grid_click(row, column, tbox_total_price, tbox_item_price, 
l_desplay_bar, tbox_order_no, R_desplay_bar):
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
        deplay_list = [(result[0][0], result[0][1], result[0][2], result[0][3], 
        1)]
    
    # update the display bar
    update_details(tbox_total_price, tbox_item_price, l_desplay_bar, 
    tbox_order_no, R_desplay_bar)

def key_pad(window, tbox_total_price, tbox_item_price, l_desplay_bar, 
tbox_order_no, R_desplay_bar):
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
                               window=window, tbox_total_price=tbox_total_price, 
                               tbox_item_price=tbox_item_price, 
                               l_desplay_bar=l_desplay_bar, 
                               tbox_order_no=tbox_order_no, 
                               R_desplay_bar=R_desplay_bar: 
                               on_button_click(i, j, window, tbox_total_price, 
                                               tbox_item_price, l_desplay_bar, 
                                               tbox_order_no, R_desplay_bar))
            button.pack()
    button_finish = tk.Button(master=window, text="Finish order", 
                              cursor="hand2", command=order_finish)
    button_finish.place(x=640, y=570, width=350, height=30)

def item_grid(window, tbox_total_price, tbox_item_price, l_desplay_bar, 
tbox_order_no, R_desplay_bar):
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
                               tbox_total_price=tbox_total_price, 
                               tbox_item_price=tbox_item_price, 
                               l_desplay_bar=l_desplay_bar, 
                               tbox_order_no=tbox_order_no, 
                               R_desplay_bar=R_desplay_bar: 
                               on_item_grid_click(i, j, tbox_total_price, 
                                                  tbox_item_price, 
                                                  l_desplay_bar, tbox_order_no, 
                                                  R_desplay_bar))
            button.pack()

def main_menu():
    """Display the main menu"""
    global exit, bg_color, label_color, white, text_color
    while exit == False:
        # Create the mian menu window
        window = tk.Tk()
        window.title("Login Window")
        window.geometry("1000x650")
        window.config(bg=bg_color)
        window.resizable(width=False, height=False)
        
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
        
        # Create the right menu frame
        key_pad(window, tbox_total_price, tbox_item_price, l_desplay_bar, 
        tbox_order_no, R_desplay_bar)
        
        # place all the widgets in the frame
        lb_total_price.place(x=50,y=15)
        lb_item_price.place(x=240,y=15)
        lb_order_no.place(x=440,y=15)
        tbox_total_price.place(x=15,y=50)
        tbox_item_price.place(x=210,y=50)
        tbox_order_no.place(x=405,y=50)
        R_desplay_bar.place(x=380,y=100)
        l_desplay_bar.place(x=15,y=100)

        # update the order details
        update_details(tbox_total_price, tbox_item_price, l_desplay_bar, 
        tbox_order_no, R_desplay_bar)

        window.mainloop()

        if exit == False:
            # exit the program if the user clicks the exit button
            exit = messagebox.askokcancel("Exit", 
            "Are you sure you want to exit?")
        else:
            # exit the program if the user clicks the exit button
            break

def sub_menu():
    """Display the sub menu"""
    global exit, bg_color, label_color, white, text_color
    while exit == False:
        # Create the sub menu window
        window = tk.Tk()
        window.title("Login Window")
        window.geometry("1000x650")
        window.config(bg=bg_color)
        window.resizable(width=False, height=False)
        
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

        # Create the right menu frame
        key_pad(window, tbox_total_price, tbox_item_price, l_desplay_bar, 
        tbox_order_no, R_desplay_bar)

        item_grid(window, tbox_total_price, tbox_item_price, l_desplay_bar, 
        tbox_order_no, R_desplay_bar)
        
        # place all the widgets in the frame
        lb_total_price.place(x=50,y=15)
        lb_item_price.place(x=240,y=15)
        lb_order_no.place(x=440,y=15)
        tbox_total_price.place(x=15,y=50)
        tbox_item_price.place(x=210,y=50)
        tbox_order_no.place(x=405,y=50)
        R_desplay_bar.place(x=380,y=100)
        l_desplay_bar.place(x=15,y=100)

        # update the order details
        update_details(tbox_total_price, tbox_item_price, l_desplay_bar, 
        tbox_order_no, R_desplay_bar)

        window.mainloop()

        if exit == False:
            # exit the program if the user clicks the exit button
            exit = messagebox.askokcancel("Exit", 
            "Are you sure you want to exit?")
        else:
            # exit the program if the user has alredy clicked the exit button
            break

def show_password(password_entry):
    """show the password"""
    global is_visable, Show_Password
    if is_visable == "*":
        is_visable = ""
        password_entry.config(show=is_visable)
        Show_Password = "Hide Password"
    else:
        is_visable = "*"
        password_entry.config(show=is_visable)
        Show_Password = "Show Password"

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

def cheek_login(username_entry, password_entry, window):
    """Check if the username and password are correct"""
    global login, staff_id
    with sqlite3.connect(DATABASE) as d_b:
        
        # Check if the username and password are correct
        cursor = d_b.cursor()
        qrl = f"""SELECT name FROM staff WHERE username = 
        "{username_entry.get()}" AND password = "{password_entry.get()}";"""
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

def sign_in():
    """Sign in the user"""
    global login, exit, is_visable
    login = False
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

        # show password button
        show_password_b = tk.Button(frame, text=Show_Password, cursor="hand2", 
                                  font=('Arial', 12), bg=white, 
                                  command=lambda password_entry=password_entry: 
                                  show_password(password_entry))
        show_password_b.place(x=350, y=300)

        # Create the login button
        login_button = tk.Button(frame, text="sign in", cursor="hand2",
                                 font=('Arial', 15,"bold"), bg=white, 
                                 width=10, height=2, command=lambda 
                                 username_entry=username_entry, 
                                 password_entry=password_entry, window=window:
                                 cheek_login(username_entry, password_entry, 
                                             window))
        login_button.place(x=225, y=400)
        window.mainloop()

        if login == False:
            # exit the program if the user clicks the exit button
            exit = messagebox.askokcancel("Exit", 
            "Are you sure you want to exit?")
            login = exit
        
    while True:
        if exit == True:
            break
        global order_id, order_no
        # generate a new order ID and order number
        order_id, order_no = order_id_no_make()

        # call the menu changer
        menu_chager()

while __name__ == "__main__":
    """run the program"""
    # start the login process
    sign_in()
    
    break
