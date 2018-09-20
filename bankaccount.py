from tkinter import messagebox

class BankAccount():
    
    def __init__(self):
        '''Constructor to set account_number to '0', pin_number to an empty string,
           balance to 0.0, interest_rate to 0.0 and transaction_list to an empty list.'''
        self.account_number = 0
        self.pin_number = None
        self.balance = 0.0
        self.interest_rate = 0.0
        self.transaction_list = []

   
    def deposit(self, amount):
        '''Function to deposit an amount to the account balance. Raises an
           exception if it receives a value that cannot be cast to float.'''
        balance = float(self.balance)
        balance+=amount
        self.balance = str(balance)
        print(self.balance)

    def withdraw(self, amount):
        '''Function to withdraw an amount from the account balance. Raises an
           exception if it receives a value that cannot be cast to float. Raises
           an exception if the amount to withdraw is greater than the available
           funds in the account.'''
        balance = float(self.balance)
        if balance > amount:
            balance-=amount
            self.balance = str(balance)
            print(self.balance)
        else:
            raise ValueError('Insufficient funds!')

        
        
    def get_transaction_string(self):
        '''Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or "Withdrawal" on
           the first line, and then the amount deposited or withdrawn on the next line.'''
        return self.transaction_list


    def export_to_file(self):
        '''Function to overwrite the account text file with the current account
           details. Account number, pin number, balance and interest (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function.'''
        filepath = ""
        filepath = filepath+self.account_number
        filepath = filepath+'.txt'
        ac_file = open(filepath, 'w+')
        ac_file.write(self.account_number + '\n')
        ac_file.write(self.pin_number + '\n')
        ac_file.write(self.balance + '\n')
        ac_file.write(self.interest_rate + '\n')
        for transaction in self.transaction_list:
            ac_file.write(transaction + '\n')
        ac_file.close()