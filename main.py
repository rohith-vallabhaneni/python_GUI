import tkinter as tk
import os
from tkinter import messagebox

# # from pylab import plot, show, xlabel, ylabel
# # from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# # from matplotlib.figure import Figure

from bankaccount import BankAccount

win = tk.Tk()
win.title("FedUni Banking")
win.geometry("440x640")
win.config(background="#eff0f1")

labelfont = ('calibri', 32, 'bold')
heading = tk.Label(win, text="FedUni Banking")
heading.config(font=labelfont, bg="#eff0f1", padx="90", pady="25")
heading.grid(row=0,column=0)


frame = tk.Frame(win)
frame.grid(row=1, column=0)
frame.config(bg='#eff0f1')

account_number_var = tk.StringVar()
account_number_entry = tk.Entry(frame, textvariable=account_number_var, width=24)
account_number_entry.focus_set()

def limitSize(*args):
    value = pin_number_var.get()
    if len(value) > 4: pin_number_var.set(value[:4])

pin_number_var = tk.StringVar()
pin_number_var.trace('w', limitSize)
account_pin_entry = tk.Entry(frame, text='PIN Number', textvariable=pin_number_var, width=24, show='*')


balance_var = tk.StringVar()
balance_var.set('Balance: $0.00')
balance_label = tk.Label(win, textvariable=balance_var)


account = BankAccount()

# ---------- Button Handlers for Login Screen ----------

def clear_details():
    account_pin_entry.delete(0,len(account_pin_entry.get()))
    account_number_entry.delete(0,len(account_number_entry.get()))

def clear_details_entry(event):
    '''Function to clear the PIN number entry when the Clear / Cancel button is clicked.'''
    clear_details()

def handle_pin_button(event):
    '''Function to add the number of the button clicked to the PIN number entry via its associated variable.''' 
    pin_length = len(account_pin_entry.get())
    if pin_length < 4:
        button_arg = event.widget['text']
        account_pin_entry.insert(pin_length,button_arg)

    

def log_in(event):
    '''Function to log in to the banking system using a known account number and PIN.'''
    global account
    global pin_number
    global account_number
    filepath = ""

    pin_number = account_pin_entry.get()
    account_number = account_number_entry.get()
    filepath = filepath+account_number
    filepath = filepath+'.txt'
    try:
        ac_file = open(filepath, 'r')
        account.account_number = ac_file.readline().strip()
        account.pin_number = ac_file.readline().strip()
        account.balance = ac_file.readline().strip()
        account.interest_rate = ac_file.readline().strip()
        if not account.pin_number == pin_number:
            messagebox.showinfo("ERROR", "Invalid PIN")
            clear_details()
            account = BankAccount()          
        else:
            transaction = ac_file.readline().strip()
            while transaction:
                account.transaction_list.append(transaction)
                transaction = ac_file.readline().strip()
            remove_all_widgets()
            create_account_screen()
            

    except IOError:
        messagebox.showinfo("ERROR", "Invalid Account Number")
        clear_details()
    

# ---------- Button Handlers for Account Screen ----------
def save_and_log_out():
    '''Function  to overwrite the account file with the current state of
    the account object (i.e. including any new transactions), remove
    all widgets and display the login screen.'''
    global account
    account.export_to_file()
    remove_all_widgets()
    create_login_screen()

    

        
        

# ---------- Utility functions ----------

def remove_all_widgets():
    '''Function to remove all the widgets from the window.'''
    global win
    global heading
    for widget in win.winfo_children():
        widget.destroy()

def read_line_from_account_file():
    '''Function to read a line from the accounts file but not the last newline character.
    Note: The account_file must be open to read from for this function to succeed.'''
    global account_file
    return account_file.readline()[0:-1]

def plot_interest_graph():
    '''Function to plot the cumulative interest for the next 12 months here.'''

    # YOUR CODE to generate the x and y lists here which will be plotted
    
    # This code to add the plots to the window is a little bit fiddly so you are provided with it.
    # Just make sure you generate a list called 'x' and a list called 'y' and the graph will be plotted correctly.
    figure = Figure(figsize=(5,2), dpi=100)
    figure.suptitle('Cumulative Interest 12 Months')
    a = figure.add_subplot(111)
    a.plot(x, y, marker='o')
    a.grid()
    
    canvas = FigureCanvasTkAgg(figure, master=win)
    canvas.draw()
    graph_widget = canvas.get_tk_widget()
    graph_widget.grid(row=4, column=0, columnspan=5, sticky='nsew')



def create_login_screen():
    '''Function to create the login screen.'''
    global heading
    detailsfont = ('calibri', 10)

    ac_details = tk.Label(frame, text="Account Number / PIN")
    ac_details.config(font=detailsfont, bg="#eff0f1")
    ac_details.config(width=18)
    ac_details.grid(row=0, column=0)
    account_number_entry.grid(row=0, column=1)
    account_pin_entry.grid(row=0, column=2)

    count=1
    for row in range(3):
        for column in range(3):
            button = tk.Button(frame, text=count)
            button.config(width=20, height=8)
            button.bind("<Button-1>", handle_pin_button)
            button.grid(row=row+1, column=column)
            count=count+1

    clear_button = tk.Button(frame, text="Cancel/Clear", command="",width=21, height=8, bd = 0)
    clear_button.config(bg='#ea0404')
    clear_button.bind("<Button-1>", clear_details_entry)
    clear_button.grid(row=4, column=0)
    button = tk.Button(frame, text="0", command="", width=20, height=8)
    button.bind("<Button-1>", handle_pin_button)
    button.grid(row=4, column=1)
    login_button = tk.Button(frame, text="Log In", width=20, height=8)
    login_button.config(bg='#1cb226')
    login_button.bind("<Button-1>", log_in)
    login_button.grid(row=4, column=2)
    

def create_account_screen():
    '''Function to create the account screen.'''
    global account
    def call_withdraw():
        try:
            amount = float(amount_entry.get())
            account.withdraw(amount)
            add_transaction("Withdrawal", str(amount))
            balance.config(text="Balance: $"+account.balance)
        except ValueError:
            messagebox.showerror("ERROR", "Insufficient funds!")
        except Exception as error:
            messagebox.showerror("ERROR", "Enter proper data")
        finally:
            amount_entry.delete(0,len(amount_entry.get()))
        
    def call_deposit():
        try:
            amount = float(amount_entry.get())
            account.deposit(amount)
            add_transaction("Deposit", str(amount))
            balance.config(text="Balance: $"+account.balance)
        except Exception as error:
            messagebox.showerror("ERROR", "Enter proper data")
        finally:
            amount_entry.delete(0,len(amount_entry.get()))

    def show_transactions():
        transaction_text_widget.config(state="normal")
        for transaction in account.transaction_list:
            transaction_text_widget.insert('end', transaction + '\n')
        transaction_text_widget.config(state="disabled")

    def add_transaction(t_type, amount):
         transaction_text_widget.config(state="normal")
         account.transaction_list.append(t_type)
         account.transaction_list.append(amount)
         transaction_text_widget.insert('end', t_type + '\n')
         transaction_text_widget.insert('end', amount + '\n')
         transaction_text_widget.config(state="disabled")


    labelfont = ('calibri', 24)
    detailsfont = ('calibri', 11)
    heading = tk.Label(win, text="FedUni Banking")
    heading.config(font=labelfont, bg="#eff0f1", padx="120")
    heading.grid(row=0, column=0)
    
    frame = tk.Frame(win)
    frame.grid(row=1, column=0)
    frame.config(bg='#eff0f1')
    account_number = tk.Label(frame, text="Account Number: "+account.account_number)
    account_number.config(font=detailsfont, bg="#eff0f1",width=20)
    account_number.grid(row=0, column=0)
    balance = tk.Label(frame, text="Balance: $"+account.balance)
    balance.config(font=detailsfont, bg="#eff0f1", width=16)
    balance.grid(row=0, column=1)
    logout_button = tk.Button(frame, text="Log Out", width=19, height=2, command=save_and_log_out)
    logout_button.config(bg='#eff0f1')
    logout_button.grid(row=0, column=2)
    amount_label = tk.Label(frame, text="Amount($)")
    amount_label.config(font=detailsfont, bg="#eff0f1")
    amount_label.config(width=16)
    amount_label.grid(row=1, column=0)
    amount_entry = tk.Entry(frame, text='Amount Entry', width=20)
    amount_entry.grid(row=1, column=1)
    
    optionsContainer = tk.Frame(frame)
    optionsContainer.grid(column = 2, row = 1)
    deposit_button = tk.Button(optionsContainer, text="Deposit", width=9, height=2, command=call_deposit)
    deposit_button.config(bg='#eff0f1')
    deposit_button.grid(row=0, column=0)
    withdraw_button = tk.Button(optionsContainer, text="Withdraw", width=9, height=2, command=call_withdraw)
    withdraw_button.config(bg='#eff0f1')
    withdraw_button.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)


    frame = tk.Frame(win)
    frame.grid(row=2, column=0)
    frame.config(bg='#eff0f1')
    global transaction_text_widget
    transaction_text_widget = tk.Text(frame, height=15, width=59, borderwidth=2, relief="sunken")
    transaction_text_widget.config(font=("calibri", 11), undo=True, wrap='word')
    transaction_text_widget.grid(row=0, column=0)
    scrollbar = tk.Scrollbar(frame, command=transaction_text_widget.yview)
    scrollbar.grid(row=0, column=1, sticky='nsew')
    transaction_text_widget['yscrollcommand'] = scrollbar.set
    show_transactions()

create_login_screen()
win.mainloop()