################
# Name: Samten Thinlay
#Department: Electrical
#Std ID: 02230073
################
#References
#@https://chat.openai.com/
#https://gemini.google.com/app/812c11c8a061ca97?hl=en-GB
################


import random # when creating a bank account, will generate a unique and random account number and password
import os # checks to see if the file "accounts.txt" is present by connecting to the operating system.

ACCOUNTS_FILE = "accounts.txt" # It is a contant that holds filename which contains account information 


class Account: # description of an account class
    def __init__(self, account_number, password, account_type, balance=0.0): # creates an account using the parameters provided, including the account type, password, and initial balance, which is optional.number of accounts = number of accounts
        self.account_number = account_number
        self.password = password
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount): # provides a feature for adding funds to an account called deposit
        self.balance += amount
        return self.balance  # gives back the total amount

    def withdraw(self, amount): # describes the process for taking money out of the account
        if amount > self.balance:
            raise ValueError("Insufficient funds.") # if there is insufficient funds, raise an error
        self.balance -= amount
        return self.balance # refunds the remaining sum after the withdrawal


class PersonalAccount(Account): # the "Personal account" subclass's base class is called
    def __init__(self, account_number, password, balance=0.0):
        super().__init__(account_number, password, "Personal", balance) # utilizes the constructor of the base class

class BusinessAccount(Account): # the "Business account" subclass's base class is called
    def __init__(self, account_number, password, balance=0.0):
        super().__init__(account_number, password, "Business", balance) # uses the constructor of the base class

# Defined as bank classes
class Bank:
    def __init__(self): #  sets up a "Bank" object initially
        self.accounts = self.load_accounts() # To load already-existing accounts from a file into the self.accounts dictionary, load_accounts is called

    def load_accounts(self):
        accounts = {}
        if os.path.exists(ACCOUNTS_FILE): # verifies the existence of the file
            with open(ACCOUNTS_FILE, 'r') as file: # opens the ACCOUNTS_FILE and reads the account data
                for line in file:
                    account_number, password, account_type, balance = line.strip().split(',') 
                    balance = float(balance) # accepted decimal points using float
                    # uses the "account_type" function to create a personal or commercial account.
                    if account_type == "Personal":
                        accounts[account_number] = PersonalAccount(account_number, password, balance)
                    elif account_type == "Business":
                        accounts[account_number] = BusinessAccount(account_number, password, balance)
        return accounts

    def save_accounts(self):
        with open(ACCOUNTS_FILE, 'w') as file: # Keep the accounts file updated with the current status
            for account in self.accounts.values(): # The file has a line containing the data for each account
                file.write(f"{account.account_number},{account.password},{account.account_type},{account.balance}\n")

    def create_account(self, account_type): # Create a password-protected account number
        account_number = str(random.randint(1000000000, 9999999999)) # Produces a random account number for the digit 10 using random
        password = str(random.randint(1000, 9999)) # generates a four-digit account password at random
        # based on the chosen account type, create a new account
        if account_type == "Personal":
            account = PersonalAccount(account_number, password)
        elif account_type == "Business":
            account = BusinessAccount(account_number, password)
        else:
            raise ValueError("Invalid account type.") # indicate "Invalid account type" if the selected account is neither of them
        self.accounts[account_number] = account # save the newly created account to the file
        self.save_accounts()
        return account_number, password # provide the password for the account

    def login(self, account_number, password): # Enter your password and account number to log in
        account = self.accounts.get(account_number)
        if account and account.password == password: # verifies that the password entered matches the account's exit, and if so, it provides the account objects.
            return account
        return None # if doesn't give any 


    def delete_account(self, account_number): # remove the newly created account 
            if account_number in self.accounts: 
                del self.accounts[account_number] # erase from the dictionary the removed account
                self.save_accounts() # save the modified account in the document
                return True # True in the event that an account is erased
            return False # False if there is no account

    def transfer(self, from_account, to_account_number, amount): # Verifies if the recipient's account has departed
            if to_account_number not in self.accounts:
                raise ValueError("Receiving account does not exist.") # returns the supplied string if it doesn't exit
            from_account.withdraw(amount) #  indicate how much is to be transferred
            self.accounts[to_account_number].deposit(amount) # transfer the money to the designated account
            self.save_accounts() #  store the revised account in a file


# Primary purpose for executing the program
def main():
    bank = Bank() # Set up a fresh Bank object
    while True:
        print("\n--- Bank Application ---")
        print("1. Open Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ") # getting the user's selection from the three alternatives above
        if choice == '1': # putting the code into practice for new account opening
            account_type = input("Enter account type (Personal/Business): ") 
            account_number, password = bank.create_account(account_type)
            print(f"Account created. Account Number: {account_number}, Password: {password}")
        elif choice == '2': # Enter the account number and password to access a previously created account
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            account = bank.login(account_number, password)
            if account: # "Login successful" is displayed if the account number and password match those of an existent account
                print("Login successful.")
                while True: # provides the user with the following option
                    print("\n--- Account Menu ---")
                    print("1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Transfer")
                    print("5. Delete Account")
                    print("6. Logout")
                    choice = input("Enter choice: ") # requesting user preference
                    if choice == '1':
                        print(f"Balance: {account.balance}") #  verifying the balance of an account
                    elif choice == '2':
                        amount = float(input("Enter amount to deposit: ")) # adding money to the account
                        account.deposit(amount)
                        bank.save_accounts()# to the account file, save the changed account
                        print(f"Deposited {amount}. New Balance: {account.balance}")# shows the updated balance following the fund deposit
                    elif choice == '3':
                        amount = float(input("Enter amount to withdraw: "))# take money out of the current account
                        try:
                            account.withdraw(amount)# sum to be withdrawn
                            bank.save_accounts()
                            print(f"Withdrawn {amount}. New Balance: {account.balance}")# provides the remaining amount after withdrawal
                        except ValueError as e: # value error if there is not enough money
                            print(e)
                    elif choice == '4':# moving money to a different account
                        to_account_number = input("Enter destination account number: ")#  requests the targeted account number
                        amount = float(input("Enter amount to transfer: "))# sum that has to be transferred
                        try:
                            bank.transfer(account, to_account_number, amount)
                            print(f"Transferred {amount} to {to_account_number}. New Balance: {account.balance}")
                        except ValueError as e:# if the account number is invalid, handle errors
                            print(e) 
                    elif choice == '5':# Eliminate the currently logged-in account
                        verification = input("Are you sure you want to delete your account? (yes/no): ")
                        if verification.lower() == 'yes':# seeking verification of the decision made
                            if bank.delete_account(account_number):
                                print("Account deleted successfully.")
                                break # once the account has been deleted, click the account menu
                            else:
                                print("Error deleting account.")
                    elif choice == '6':
                        print("Logged out.")
                        break
                    else:
                        print("Invalid choice. Try again.")
                        
            else:
                print("Invalid account number or password.") # In case the password or account number don't correspond
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")# take care of the user's incorrect selection

if __name__ == "__main__": # verifies the script is being executed directly
    main() #  carries out an application's main() function call