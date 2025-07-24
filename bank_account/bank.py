"""
Basic Functionalities
- **Create Account:** Initialize account with holder name, unique account number, and initial balance.
- **Deposit:** Add money to the account with validation for positive amounts.
- **Withdraw:** Subtract money ensuring no negative balances allowed.
- **Check Balance:** View current account balance.
- **Transaction History:** Keep a log of deposits and withdrawals with timestamps.
"""
import time

class Bank_Account:
    current_time = time.time()
    def __init__(self, name, account_number, initial_balance=0):
        self.name = name
        self.account_number = account_number
        self.balance = initial_balance
        self.transactions = []

    def deposit(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount is not valid")
        self.balance += amount
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        transaction_history = f"{timestamp} [The amount {amount} is deposited in your account]"
        self.transactions.append(transaction_history)
        return f"Deposit of {amount} is successful, Your current balance is {self.balance:,.2f}"
    
    def withdraw(self, amount):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount can not be negative")
        if self.balance >= amount:
            self.balance -= amount
            transaction_history = f"{timestamp} [The amount {amount} is withdrawn from your account]"
            self.transactions.append(transaction_history)
            return f"Withdrawal of {amount} is successful, Your current balance is {self.balance:,.2f}"
        else:
            transaction_history = f"{timestamp} [Failed withdrawal of {amount} — insufficient balance]"
            self.transactions.append(transaction_history)
            return f"You don't have sufficient balance to make this withdrawal."
    
    def check_balance(self):
        return f'Your account balance is {self.balance}'
    
    def get_transaction_history(self):
        return self.transactions
    
    def __str__(self):
        return f"Account Holder: {self.name}, Balance: {self.balance:,.2f}"
    

acc1 = Bank_Account("Bilal", 10241235681123, 0 )
print(acc1)
print(acc1.deposit(500))
print(acc1.withdraw(1000))
print(acc1.deposit(550))
print(acc1.withdraw(1000))
print(acc1.check_balance())
print(acc1.get_transaction_history())

