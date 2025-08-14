"""This is a Python program that will be for staff in a takeaway shop. It will 
connect with a database and allow staff to take orders, search for products, 
whilst also displaying the order details and total price and generating a 
receipt for the customer.
By: Matt Smith                                                     13/08/2025"""

# import modules
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import date

# constants
DATABASE = "database-L2DTSD-2025.db"
BG_COLOR = "#5c9ead"
LABEL_COLOR = "#236273"
WHITE = "#ffffff"

# global variables
exit = False
login = False
is_visable = "*"
Show_Password_txt = "Show Password"
menu = 2
staff_id = 0
staff_name = ""
text_color = "black"
order_id = 0
total_price = 0.0
order_no = 0
display_list = [(0, "", 0.0, "", 1)]
order_list = []
loop = False
change_price_window = False
change_amount_window = False

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
        
        if result[0][0] is None or result[0][0] <= order_id:
            # Increment the last order ID
            order_id += 1

            # Increment the last order number
            if order_no < 100:
                # Increment the last order no
                order_no += 1
            else:
                # Reset the order number if it exceeds 100
                order_no = 1
        else:
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

def order_finish(tbox_total_price, tbox_item_price, l_display_bar, 
                 tbox_order_no, R_display_bar, window_main):
    """Finish the order and display a message"""
    # Declare global variables used in the function
    global staff_id, order_id, order_no, order_list, staff_name, display_list

    # Get today's date
    today = date.today()
    total_price = 0.0  # Initialize total prices

    # Initialize the receipt string with headers
    receipt = ("-------------------- RECEIPT --------------------\n"
               f"{'Item':<20} {'Price':>10} {'Qty':>5} {'Subtotal':>10}\n------"
               "-------------------------------------------\n")

    # Loop through the order list and add each item to the receipt
    for item in order_list:
        if len(item[1]) > 20:
            # If the item name is too long, truncate it to 20 characters
            item_name = item[1][:20]
        else:
            item_name = item[1]
        receipt += (f"{item_name:<20} {item[2]:>10.2f} {item[4]:>5} "
                    f"{(item[2]*item[4]):>10.2f}\n")
        total_price += (item[2] * item[4])  # Calculate the total price

    # Format the month to ensure two digits if necessary
    if today.month < 10:
        today_month = f"0{today.month}"
    else:
        today_month = today.month

    # Add the total price and order details to the receipt
        
    receipt += ("-------------------------------------------------\n"
                f"{'Total:':<35} ${total_price:>10.2f}\n------------------------"
                f"-------------------------\n{'Order id':<6} "
                f"{'Order number':>21} {'Name':>6} {'Date':>8}\n---------------"
                f"----------------------------------\n{order_id:<23} "
                f"{order_no:<6} {staff_name:<7}{today.day}/"
                f"{today_month}/{today.year}\n--------------------------"
                "-----------------------")

    # Display the receipt and ask for confirmation to finish the order
    finish = messagebox.askokcancel("Contue", "Is this order correct?\nIf you "
                                    "click 'OK' the order will be finished."
                                    f"\n\n{receipt}")

    if finish == True:
        # Finish the order and insert it into the database
        with sqlite3.connect(DATABASE) as d_b:
            cursor = d_b.cursor()
            # Use a parameterized query to insert the order into the orders table
            qrl = """INSERT INTO [order] (order_id, total_price, order_num, 
            staff_id, order_receipt) VALUES (?, ?, ?, ?, ?);"""
            cursor.execute(qrl, (order_id, round(total_price, 2), order_no, staff_id, 
                                 receipt))
            d_b.commit()

        # Reset the order details for the next order
        order_id_no_make()
        display_list = [(0, "", 0.0, "", 1)]
        order_list = []
        total_price = 0.0

        # Update the UI with the reset order details
        update_details(tbox_total_price, tbox_item_price, l_display_bar, 
                    tbox_order_no, R_display_bar, window_main)

        # Show a message indicating the order has been finished
        messagebox.showinfo("Order Finished", "Your order has been finished.")

def update_details(tbox_total_price, tbox_item_price, l_display_bar, 
tbox_order_no, R_display_bar, window_main):
    """Update the order details"""
    # update the total price text box
    total_price = 0.0
    for i in range(len(order_list)):
        i -= 1 
        total_price += order_list[i][2] * order_list[i][4]
    tbox_total_price.config(state='normal')
    tbox_total_price.delete('1.0', tk.END)
    tbox_total_price.insert(tk.END, f"${round(total_price, 2)}")
    tbox_total_price.config(state='disabled')

    # update the item price text box
    global display_list
    tbox_item_price.config(state='normal')
    tbox_item_price.delete('1.0', tk.END)
    tbox_item_price.insert(tk.END, f"${display_list[0][2] * display_list[0][4]}")
    tbox_item_price.config(state='disabled')

    # update the display bar text box
    l_display_bar.config(state='normal')
    l_display_bar.delete('1.0', tk.END)
    l_display_bar.insert(tk.END, display_list[0][1])
    l_display_bar.config(state='disabled')

    global order_no
    # update the order number text box
    tbox_order_no.config(state='normal')
    tbox_order_no.delete('1.0', tk.END)
    tbox_order_no.insert(tk.END, order_no)
    tbox_order_no.config(state='disabled')

    # update the right desplay text box
    R_display_bar.config(state='normal')
    R_display_bar.delete('1.0', tk.END)
    R_display_bar.insert(tk.END, "")
    R_display_bar.config(state='disabled')

    global menu, loop
    if menu ==2 and loop == True:
        # if the menu is 2 and loop is true, restart the main window
        window_main.destroy()
        main_menu()
        loop = False

def add_order_list():
    """Update the order list"""
    global order_list, display_list
    # add the product to the order list
    order_list.append(display_list[0])

def button_text(row,column):
    """Get the text for the keypad buttons"""
    # Connect to the database and fetch the text for the keypad button
    with sqlite3.connect(DATABASE) as d_b:
        cursor = d_b.cursor()
        # Query to get the text for the button based on its row and column
        qrl = f"""SELECT text FROM key_pad WHERE row = {row} AND column = {column};"""
        cursor.execute(qrl)
        result = cursor.fetchall()
    # Return the text for the button
    return result[0][0]

def item_text(row,column):
    """Get the text for the item grid buttons"""	
    # Connect to the database to fetch the product name for the item grid button
    with sqlite3.connect(DATABASE) as d_b:
        cursor = d_b.cursor()
        # Query to get the product name based on its row and column
        qrl = f"""SELECT product_name FROM products WHERE row = {row} AND column = {column};"""
        cursor.execute(qrl)
        result = cursor.fetchall()
    # Return the product name for the button
    return result[0][0]

def change_price(price_entry, window, tbox_total_price, tbox_item_price, 
l_display_bar, tbox_order_no, R_display_bar, window_main):
    """Change the price of the product"""
    # Check if the price entry is valid
    if not price_entry.get().isdigit():
        error_message("Please enter a valid price.")
        return
    new_price = float(price_entry.get())
    # Update the global variable display_list with the new price
    global display_list
    # Convert the new price to decimal format
    decamial = new_price / (10**2)
    # Update the product details in display_list with the new price
    display_list = [(display_list[0][0], display_list[0][1], decamial, 
    display_list[0][3], display_list[0][4])]
    # Refresh the UI to reflect the updated price
    update_details(tbox_total_price, tbox_item_price, l_display_bar, 
    tbox_order_no, R_display_bar, window_main)
    # Close the price change window
    window.destroy()
    global change_price_window
    change_price_window = False  # Reset the change price window flag

def exit_select_window(select_window, selected_product, tbox_total_price, 
tbox_item_price, l_display_bar, tbox_order_no, R_display_bar, window_main):
    """Exit the selection window and update the display bar with the selected product"""
    global display_list
    product = selected_product.get()
    with sqlite3.connect(DATABASE) as d_b:
        cursor = d_b.cursor()
        # Search for the product in the database using the selected product name
        qrl = f"""SELECT product_plu, product_name, product_price, 
        product_catogory FROM products WHERE search_name == 
        '{product.upper()}';"""
        cursor.execute(qrl)
        result = cursor.fetchall()
        if len(result) == 1:
            # If the product is found, update the display bar with its details
            display_list = [(result[0][0], result[0][1], result[0][2], 
            result[0][3], result[0][4])]
            update_details(tbox_total_price, tbox_item_price, l_display_bar, 
            tbox_order_no, R_display_bar, window_main)
        else:
            # Display an error message if the product is not found or an issue occurs
            error_message("An error has occurred. Please try again.")
    # Close the selection window
    select_window.destroy()

def selection_window(result, tbox_total_price, tbox_item_price, l_display_bar, 
tbox_order_no, R_display_bar, window_main):
    """Create a selection window to select a product"""
    global display_list
    # create the selection window
    select_window = tk.Tk()
    select_window.title("Select Product")
    select_window.geometry("500x150")
    select_window.config(bg=BG_COLOR)
    select_window.resizable(width=False, height=False)
    # create the dropdown to display the products and select one
    selected_product = tk.StringVar(select_window, result[0][1])
    product_names = [item[1] for item in result]
    product_dropdown = tk.OptionMenu(select_window, selected_product, 
    *product_names)
    product_dropdown.pack(pady=10)
    # create the select button
    select_button = tk.Button(select_window, text="Select", cursor="hand2", 
                              command=lambda: exit_select_window(select_window, 
                              selected_product, tbox_total_price, 
                              tbox_item_price, l_display_bar, tbox_order_no, 
                              R_display_bar, window_main))
    select_button.pack(pady=5)
    
def search_product(search_entry, search_window, tbox_total_price, 
tbox_item_price, l_display_bar, tbox_order_no, R_display_bar, window_main):
    """Search for a product by name"""
    global display_list
    with sqlite3.connect(DATABASE) as d_b:
        cursor = d_b.cursor()
        # Search for the product in the database using a case-insensitive partial match
        qrl = f"""SELECT product_plu, product_name, product_price, 
        product_catogory FROM products WHERE search_name LIKE 
        '%{search_entry.get().upper()}%';"""
        cursor.execute(qrl)
        result = cursor.fetchall()
        
        if len(result) > 1:
            # If multiple products are found, open the selection window
            selection_window(result, tbox_total_price, tbox_item_price, 
                             l_display_bar, tbox_order_no, R_display_bar, 
                             window_main)
        elif len(result) > 10:
            # If the search is too broad, display an error message
            error_message("Search too broad. Please be more specific.")
        elif len(result) == 1:
            # If exactly one product is found, update the display bar
            display_list = [(result[0][0], result[0][1], result[0][2], 
            result[0][3], 1)]
            update_details(tbox_total_price, tbox_item_price, l_display_bar, 
            tbox_order_no, R_display_bar, window_main)
        else:
            # If no products are found, display an error message
            error_message("No products found with that name.")
    
    # Close the search window
    search_window.destroy()

def times_price(item_amount, window, tbox_total_price, tbox_item_price, 
l_display_bar, tbox_order_no, R_display_bar, window_main):
    """Change the price of the product"""
    global display_list
    # Check if the item amount is valid
    if item_amount <= 1:
        error_message("Please enter a valid amount.")
    else:
        # Update the display_list with the new item amount
        display_list = [(display_list[0][0], display_list[0][1], display_list[0][2], 
        display_list[0][3], item_amount)]
        update_details(tbox_total_price, tbox_item_price, l_display_bar, 
        tbox_order_no, R_display_bar, window_main)
    window.destroy()
    global change_amount_window
    change_amount_window = False  # Reset the change amount window flag

def on_button_click(i, j, window, tbox_total_price, tbox_item_price, 
l_display_bar, tbox_order_no, R_display_bar, window_main):
    """Handle button click events"""
    global display_list, loop
    # get the button details from the database
    text = button_text(i, j)
    if text == "Menu":
        # change the menu
        window.destroy()
        menu_changer()
    elif text == "c":
        # clear the display bar
        display_list = [(0, "", 0.0, "product_catogory", 1)]
        update_details(tbox_total_price, tbox_item_price, l_display_bar, 
        tbox_order_no, R_display_bar, window_main)
    elif text == "PLU":
        # get the product details from the database
        plu = R_display_bar.get("1.0", tk.END).strip()
        # get the product details from the database using the plu
        try:
            with sqlite3.connect(DATABASE) as d_b:
                cursor = d_b.cursor()
                qrl = f"""SELECT product_name, product_price, product_catogory 
                FROM products WHERE product_plu = {plu};"""
                cursor.execute(qrl)
                result = cursor.fetchall()
                display_list = [(plu, result[0][0], result[0][1], result[0][2], 
                1)]
        except:
            error_message("product not found")
        # update the display bar
        update_details(tbox_total_price, tbox_item_price, l_display_bar, 
            tbox_order_no, R_display_bar, window_main)
    elif text == "Add to order":
        # check if a product is selected
        if display_list[0][0] == 0:
            error_message("Please select a product first.")
            return
        # add the product to the order list
        add_order_list()
        # update the total price
        global total_price
        total_price += (display_list[0][2] * display_list[0][4])
        total_price = round(total_price, 2)
        # update the display bar
        display_list = [(0, "", 0.0, "product_catogory", 1)]
        loop = True
        update_details(tbox_total_price, tbox_item_price, l_display_bar, 
        tbox_order_no, R_display_bar, window_main)
    elif text == "Sign out":
        # sign out the user
        global exit
        window.destroy()
        sign_in()
    elif text == "Change price":
        # Check if the change price window is already open
        global change_price_window
        if change_price_window == True:
            # If the change price window is already open, close it
            error_message("The change price window is already open.")
            change_price_window = False
            return
        else:
            # Set the change price window flag to True
            change_price_window = True
        # change the price of the product
        price_window = tk.Tk()
        price_window.title("Change Price Window")
        price_window.geometry("150x150")
        price_window.config(bg=BG_COLOR)
        price_window.resizable(width=False, height=False)
        # create the price change window
        price_label = tk.Label(master=price_window, text="New Price", 
        bg=BG_COLOR, fg=text_color, font=('Arial', 12, "bold"))
        price_label.pack(pady=10)
        # create the entry for the new price
        validate_command = price_window.register(lambda p: p.isdigit())
        price_entry = tk.Entry(master=price_window, width=10, validate="key", 
        validatecommand=(validate_command, '%P'))
        price_entry.pack(pady=5)
        # create the change button
        change_button = tk.Button(master=price_window, text="Change", 
                                  cursor="hand2", command=lambda: 
                                  change_price(price_entry, 
                                               price_window, tbox_total_price, 
                                               tbox_item_price, l_display_bar, 
                                               tbox_order_no, R_display_bar, 
                                               window_main))
        change_button.pack(pady=5)
        price_window.mainloop()
    elif text == "search":
        # seaerch for a product by Name
        search_window = tk.Tk()
        search_window.title("Search Product")
        search_window.geometry("300x150")
        search_window.config(bg=BG_COLOR)
        search_window.resizable(width=False, height=False)
        # create the search window
        search_label = tk.Label(master=search_window, text="Search by Name", 
        bg=BG_COLOR, fg=text_color, font=('Arial', 12, "bold"))
        search_label.pack(pady=10)
        search_entry = tk.Entry(master=search_window, width=30)
        search_entry.pack(pady=5)
        search_button = tk.Button(master=search_window, text="Search", 
                                  cursor="hand2", command=lambda: 
                                  search_product(search_entry, search_window, 
                                                 tbox_total_price, 
                                                 tbox_item_price, l_display_bar, 
                                                 tbox_order_no, R_display_bar, 
                                                 window_main))
        search_button.pack(pady=5)
    elif text == "x":
        # Check if the change amount window is already open
        global change_amount_window
        if change_amount_window == True:
            # If the change amount window is already open, close it
            error_message("The change price window is already open.")
            change_amount_window = False
            return
        else:
            # Set the change amount window flag to True
            change_amount_window = True
        # change the amount of the product
        times_window = tk.Tk()
        times_window.title("Change times Window")
        times_window.geometry("150x150")
        times_window.config(bg=BG_COLOR)
        times_window.resizable(width=False, height=False)
        # create the times change window
        times_label = tk.Label(master=times_window, text="how many items", 
        bg=BG_COLOR, fg=text_color, font=('Arial', 12, "bold"))
        times_label.pack(pady=10)
        # create the entry for the new times
        validate_command = times_window.register(lambda p: p.isdigit())
        times_entry = tk.Entry(master=times_window, width=10, validate="key", 
        validatecommand=(validate_command, '%P'))
        times_entry.pack(pady=5)
        # create the change button
        change_button = tk.Button(master=times_window, text="Change", 
                                  cursor="hand2", command=lambda: 
                                  times_price(int(times_entry.get()), 
                                               times_window, tbox_total_price, 
                                               tbox_item_price, l_display_bar, 
                                               tbox_order_no, R_display_bar, 
                                               window_main))
        change_button.pack(pady=5)
        times_window.mainloop()
    elif text.isdigit():
        # if the button is a digit, add it to the display bar
        current_text = R_display_bar.get("1.0", tk.END).strip()
        new_text = current_text + text
        R_display_bar.config(state='normal')
        R_display_bar.delete('1.0', tk.END)
        R_display_bar.insert(tk.END, new_text)
        R_display_bar.config(state='disabled')

def on_item_grid_click(row, column, tbox_total_price, tbox_item_price, 
l_display_bar, tbox_order_no, R_display_bar,window_main):
    """Handle item grid button click events"""
    global display_list
    # get the product details from the database
    with sqlite3.connect(DATABASE) as d_b:
        # get the product details for a specific row and column
        cursor = d_b.cursor()
        qrl = f"""SELECT product_plu, product_name, product_price, 
        product_catogory FROM products WHERE row = {row} and Column = 
        {column};"""
        cursor.execute(qrl)
        result = cursor.fetchall()
        display_list = [(result[0][0], result[0][1], result[0][2], result[0][3], 
        1)]
    
    # update the display bar
    update_details(tbox_total_price, tbox_item_price, l_display_bar, 
    tbox_order_no, R_display_bar, window_main)

def key_pad(window, tbox_total_price, tbox_item_price, l_display_bar, 
tbox_order_no, R_display_bar, window_main):
    """display the keypad"""
    # Create the keypad frame
    rframe = tk.Frame(master=window, bg=BG_COLOR)
    rframe.place(x=650, y=15, width=350, height=600)
    # Create the label for the keypad
    for i in range(6):
        for j in range(3):
            # Create a frame for each button in the keypad
            frame = tk.Frame(master=rframe, relief=tk.RAISED, borderwidth=1, 
                             bg="WHITE")
            frame.grid(row=i,column=j,padx=8,pady=8)
            text = button_text(i,j)
            # Create a button for each button in the keypad
            button = tk.Button(master=frame, text=text, cursor="hand2", 
                               width=11, height=4, command=lambda i=i,j=j,
                               window=window, tbox_total_price=tbox_total_price, 
                               tbox_item_price=tbox_item_price, 
                               l_display_bar=l_display_bar, 
                               tbox_order_no=tbox_order_no, 
                               R_display_bar=R_display_bar: 
                               on_button_click(i, j, window, tbox_total_price, 
                                               tbox_item_price, l_display_bar, 
                                               tbox_order_no, R_display_bar, 
                                               window_main))
            button.pack()
    # Create the exit button
    button_finish = tk.Button(master=window, text="Finish order", 
                              cursor="hand2", command=lambda:order_finish(
                                  tbox_total_price, tbox_item_price, 
                                  l_display_bar, tbox_order_no, R_display_bar, 
                                  window_main))
    button_finish.place(x=640, y=570, width=350, height=30)

def item_grid(window, tbox_total_price, tbox_item_price, l_display_bar, 
tbox_order_no, R_display_bar, window_main):
    """display the Item grid"""
    # Create the item grid frame
    dframe = tk.Frame(master=window, bg=BG_COLOR)
    dframe.place(x=25, y=170, width=550, height=420)
    for i in range(5):
        for j in range(4):
            # Create a frame for each button in the item grid
            frame = tk.Frame(master=dframe, relief=tk.RAISED, borderwidth=1, 
                             bg="WHITE")
            frame.grid(row=i,column=j,padx=15,pady=5)
            text = item_text(i,j)
            button = tk.Button(master=frame, text=text, cursor="hand2", 
                               width=13, height=4, command=lambda i=i,j=j,
                               tbox_total_price=tbox_total_price, 
                               tbox_item_price=tbox_item_price, 
                               l_display_bar=l_display_bar, 
                               tbox_order_no=tbox_order_no, 
                               R_display_bar=R_display_bar:
                               on_item_grid_click(i, j, tbox_total_price, 
                                                  tbox_item_price, 
                                                  l_display_bar, tbox_order_no, 
                                                  R_display_bar, window_main))
            button.pack()

def selected_product_grid_button(i, tbox_total_price, tbox_item_price, 
l_display_bar, tbox_order_no, R_display_bar, window_main):
    """code for the selected product grid buttons"""
    global order_list, loop
    # Get the selected product from the order list
    order_list.pop(i)
    loop = True
    update_details(tbox_total_price, tbox_item_price, l_display_bar, 
    tbox_order_no, R_display_bar, window_main)

def selected_products(lframe, tbox_total_price, tbox_item_price, l_display_bar, 
tbox_order_no, R_display_bar, window_main):
    """Display the most recent selected products in a item grid"""
    global order_list
    # Sort the order list by price in descending order
    top_list = order_list[:18]
    if len(top_list) != 0:
        # Create a frame to display the selected products
        lbframe = tk.Frame(master=lframe, bg=BG_COLOR)
        lbframe.place(x=25, y=170, width=550, height=420)
        for i in range(len(top_list)):
            row = i // 3  # Determine the row
            col = i % 3   # Determine the column
            frame = tk.Frame(master=lbframe, relief=tk.RAISED, borderwidth=1, 
                             bg="WHITE")
            frame.grid(row=row,column=col,padx=8,pady=8)
            # Create a label for each selected product
            if len(top_list[i][1]) > 20:
                # If the item name is too long, cut it to 20 characters
                item_name = top_list[i][1][:20]
            else:
                item_name = top_list[i][1]
            # Create a button for each selected product
            button = tk.Button(master=frame, text=item_name, width=14, 
                               height=2, bg=WHITE, fg=text_color, 
                               font=('Arial', 12, "bold"), command=lambda i=i: 
                               selected_product_grid_button
                               (i, tbox_total_price, tbox_item_price, 
                                l_display_bar, tbox_order_no, R_display_bar, 
                                window_main))
            button.pack()

def main_menu():
    """Display the main menu"""
    global exit, text_color
    while exit == False:
        # Create the mian menu window
        window_main = tk.Tk()
        window_main.title("Login Window")
        window_main.geometry("1000x650")
        window_main.config(bg=BG_COLOR)
        window_main.resizable(width=False, height=False)
        
        # create the left menu frame
        lframe = tk.Frame(master=window_main,bg="WHITE")
        lframe.place(x=15,y=15,width=600,height=620)
        lb_total_price = tk.Label(master=lframe, text="Total Price", 
                                  font=('Arial',12,"bold"), fg=text_color, 
                                  bg=WHITE)
        lb_item_price = tk.Label(master=lframe, text="Item Price", 
                                 font=('Arial',12,"bold"), fg=text_color, 
                                 bg=WHITE)
        lb_order_no = tk.Label(master=lframe, text="Order No", 
                               font=('Arial',12,"bold"), fg=text_color, 
                               bg=WHITE)
        tbox_total_price = tk.Text(master=lframe, width=18, height=2, 
                                   state="disabled", borderwidth=2, bg=BG_COLOR)
        tbox_item_price = tk.Text(master=lframe, width=18, height=2, 
                                  state="disabled", borderwidth=2, bg=BG_COLOR)
        tbox_order_no = tk.Text(master=lframe, width=18, height=2, 
                                state="disabled", borderwidth=2, bg=BG_COLOR)
        R_display_bar = tk.Text(master=lframe, width=22, height=2, 
                                state="disabled", borderwidth=2, bg=BG_COLOR)
        l_display_bar = tk.Text(master=lframe, width=45, height=2, 
                                state="disabled", borderwidth=2, bg=BG_COLOR)
        
        # Create the right menu frame
        key_pad(window_main, tbox_total_price, tbox_item_price, l_display_bar, 
        tbox_order_no, R_display_bar, window_main)

        # Create the item grid frame
        selected_products(lframe, tbox_total_price, tbox_item_price, 
        l_display_bar, tbox_order_no, R_display_bar, window_main)
        
        # place all the widgets in the frame
        lb_total_price.place(x=50,y=15)
        lb_item_price.place(x=240,y=15)
        lb_order_no.place(x=440,y=15)
        tbox_total_price.place(x=15,y=50)
        tbox_item_price.place(x=210,y=50)
        tbox_order_no.place(x=405,y=50)
        R_display_bar.place(x=380,y=100)
        l_display_bar.place(x=15,y=100)

        # update the order details
        global loop
        loop = False
        update_details(tbox_total_price, tbox_item_price, l_display_bar, 
        tbox_order_no, R_display_bar, window_main)

        window_main.mainloop()

        if exit == False:
            # exit the program if the user clicks the exit button
            exit = messagebox.askokcancel("Exit", 
            "Are you sure you want to exit?")
        else:
            # exit the program if the user clicks the exit button
            break

def sub_menu():
    """Display the sub menu"""
    global exit, text_color
    while exit == False:
        # Create the sub menu window
        window = tk.Tk()
        window.title("sub menu Window")
        window.geometry("1000x650")
        window.config(bg=BG_COLOR)
        window.resizable(width=False, height=False)
        
        # create the left menu frame
        lframe = tk.Frame(master=window,bg="WHITE")
        lframe.place(x=15,y=15,width=600,height=620)
        lb_total_price = tk.Label(master=lframe, text="Total Price", 
                                  font=('Arial',12,"bold"), fg=text_color, 
                                  bg=WHITE)
        lb_item_price = tk.Label(master=lframe, text="Item Price", 
                                 font=('Arial',12,"bold"), fg=text_color, 
                                 bg=WHITE)
        lb_order_no = tk.Label(master=lframe, text="Order No", 
                               font=('Arial',12,"bold"), fg=text_color, 
                               bg=WHITE)
        tbox_total_price = tk.Text(master=lframe, width=18, height=2, 
                                   state="disabled", borderwidth=2, bg=BG_COLOR)
        tbox_item_price = tk.Text(master=lframe, width=18, height=2, 
                                  state="disabled", borderwidth=2, bg=BG_COLOR)
        tbox_order_no = tk.Text(master=lframe, width=18, height=2, 
                                state="disabled", borderwidth=2, bg=BG_COLOR)
        R_display_bar = tk.Text(master=lframe, width=22, height=2, 
                                state="disabled", borderwidth=2, bg=BG_COLOR)
        l_display_bar = tk.Text(master=lframe, width=45, height=2, 
                                state="disabled", borderwidth=2, bg=BG_COLOR)

        # Create the right menu frame
        key_pad(window, tbox_total_price, tbox_item_price, l_display_bar, 
        tbox_order_no, R_display_bar, window)

        # Create the item grid frame
        item_grid(window, tbox_total_price, tbox_item_price, l_display_bar, 
        tbox_order_no, R_display_bar, window)
        
        # place all the widgets in the frame
        lb_total_price.place(x=50,y=15)
        lb_item_price.place(x=240,y=15)
        lb_order_no.place(x=440,y=15)
        tbox_total_price.place(x=15,y=50)
        tbox_item_price.place(x=210,y=50)
        tbox_order_no.place(x=405,y=50)
        R_display_bar.place(x=380,y=100)
        l_display_bar.place(x=15,y=100)

        # update the order details
        update_details(tbox_total_price, tbox_item_price, l_display_bar, 
        tbox_order_no, R_display_bar, window)

        window.mainloop()

        if exit == False:
            # exit the program if the user clicks the exit button
            exit = messagebox.askokcancel("Exit", 
            "Are you sure you want to exit?")
        else:
            # exit the program if the user has alredy clicked the exit button
            break

def show_password(password_entry):
    """show and hide the password"""
    global is_visable, Show_Password_txt
    # toggle the visibility of the password entry field
    if is_visable == "*":
        is_visable = ""
        password_entry.config(show=is_visable)
        Show_Password_txt = "Hide Password"
    else:
        is_visable = "*"
        password_entry.config(show=is_visable)
        Show_Password_txt = "Show Password"

def menu_changer():
    """switch the menu"""
    global menu
    # Check the current menu state and switch to the appropriate menu
    if menu == 1:
        # call the main menu
        menu = 2
        main_menu()
    else:
        #call the sub menu
        menu = 1
        sub_menu()

def check_login(username_entry, password_entry, window):
    """Check if the username and password are correct"""
    global login, staff_id, staff_name
    # connect to the database
    with sqlite3.connect(DATABASE) as d_b:
        
        # Check if the username and password are correct
        cursor = d_b.cursor()
        qrl = f"""SELECT name FROM Staff WHERE username = 
        "{username_entry.get()}" AND password = "{password_entry.get()}";"""
        cursor.execute(qrl)
        results = cursor.fetchall()
        if not results == []:
            messagebox.showinfo("Login", 
                                f"Login successful! \n Welcome {results[0][0]}")
            
            # get the staff id and name from the database
            qrl = f"""SELECT staff_id, name FROM Staff WHERE username = 
            "{username_entry.get()}" AND password = "{password_entry.get()}";"""
            cursor.execute(qrl)
            results = cursor.fetchall()
            staff_id = results[0][0]
            staff_name = results[0][1]

            # close the login window
            window.destroy()
            login = True
        else:
            messagebox.showerror("Login", "Invalid username or password.")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

def sign_in():
    """Sign in the user"""
    global login, exit, is_visable, Show_Password_txt
    login = False
    # login window
    while login == False:
        # Create the login window
        window = tk.Tk()
        window.title("Login Window")
        window.geometry("1000x650")
        window.config(bg=BG_COLOR)
        window.resizable(width=False, height=False)

        # Create the mian Frame
        frame = tk.Frame(master=window, bg=LABEL_COLOR)
        frame.place(x=200, y=25, width=600, height=600)

        # Create the login feilds
        username_label = tk.Label(frame, text="Username", 
                                  font=('Arial',15,"bold"), bg=LABEL_COLOR) 
        username_entry = tk.Entry(frame, width=75)
        password_label = tk.Label(frame, text="Password", 
                                  font=('Arial',15,"bold"), bg=LABEL_COLOR)
        password_entry = tk.Entry(frame, show=is_visable, width=75)
        username_entry.place(x=25, y=130)
        username_label.place(x=50, y=100)
        password_entry.place(x=25, y=230)
        password_label.place(x=50, y=200)

        # show password button
        show_password_b = tk.Button(frame, text=Show_Password_txt, cursor="hand2", 
                                  font=('Arial', 12), bg=WHITE, 
                                  command=lambda password_entry=password_entry: 
                                  show_password(password_entry))
        show_password_b.place(x=350, y=300)

        # Create the login button
        login_button = tk.Button(frame, text="sign in", cursor="hand2",
                                 font=('Arial', 15,"bold"), bg=WHITE, 
                                 width=10, height=2, command=lambda 
                                 username_entry=username_entry, 
                                 password_entry=password_entry, window=window:
                                 check_login(username_entry, password_entry, 
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
        order_id_no_make()

        # call the menu changer
        menu_changer()

while __name__ == "__main__":
    """run the program"""
    # start the login process
    sign_in()
    
    break
