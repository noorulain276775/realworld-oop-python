"""
Basic Functionalities
- Create Account: Initialize account with holder name, unique account number, and initial balance.
- Deposit: Add money to the account with validation for positive amounts.
- Withdraw: Subtract money ensuring no negative balances allowed.
- Check Balance: View current account balance.
- Transaction History: Keep a log of deposits and withdrawals with timestamps.

Intermediate-Level Features
- Transfer Funds: Move money between two accounts with transaction logging on both sides.
- Account Summary / Statement: Generate a detailed statement showing balance, holder info, and recent transactions.
- Unique Account Number: Auto-generated unique ID for each new account.

Extra Polish
- Close Account: Ability to close accounts and prevent further transactions.
- Lock/Unlock Account: Temporarily block account operations.
- Input Validation: Robust checks to prevent invalid input or transactions.
- Pretty Printing: Custom `__str__` method to display account info neatly.
"""

import time
import uuid


class Bank_Account:
    def __init__(self, name, initial_balance=0, closed=False, locked=False):
        self.name = name
        self.account_number = str(uuid.uuid4().int)[:13]
        self.balance = initial_balance
        self.closed = closed
        self.locked = locked
        self.transactions = []

    def deposit(self, amount):
        if self.closed:
            raise ValueError("Your account is closed, the money can not be deposited in this account")
        if self.locked:
            raise ValueError("Account is locked. Operation denied.")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount is not valid")
        
        self.balance += amount
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        transaction_history = f"{timestamp} [The amount {amount} is deposited in your account]"
        self.transactions.append(transaction_history)
        return f"Deposit of {amount} is successful, Your current balance is {self.balance:,.2f}"

    def withdraw(self, amount):
        if self.closed:
            raise ValueError("Your account is closed, the money can not be withdrawn from this account")
        if self.locked:
            raise ValueError("Account is locked. Operation denied.")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount is not valid")
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if self.balance >= amount:
            self.balance -= amount
            transaction_history = f"{timestamp} [The amount {amount} is withdrawn from your account]"
            self.transactions.append(transaction_history)
            return f"Withdrawal of {amount} is successful, Your current balance is {self.balance:,.2f}"
        else:
            transaction_history = f"{timestamp} [Failed withdrawal of {amount} — insufficient balance]"
            self.transactions.append(transaction_history)
            return "You don't have sufficient balance to make this withdrawal."

    def transfer(self, recipient_account, amount):
        if self.closed:
            raise ValueError("Your account is closed, the money can not be transferred from this account")
        if recipient_account.closed:
            raise ValueError("The recipient account is closed, the money can not be transferred here")
        if self.locked:
            raise ValueError("Account is locked. Operation denied.")
        if recipient_account.locked:
            raise ValueError("Recipient account is locked. Operation denied.")
        if recipient_account.account_number == self.account_number:
            raise ValueError("You cannot transfer money to your own account")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Please enter a valid transfer amount")
        if self.balance < amount:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.transactions.append(f"{timestamp} [Transfer of {amount} failed — insufficient balance]")
            raise ValueError("Insufficient balance for transfer")

        self.balance -= amount
        recipient_account.balance += amount
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.transactions.append(f"{timestamp} [Transferred {amount} to account {recipient_account.account_number}]")
        recipient_account.transactions.append(f"{timestamp} [Received {amount} from account {self.account_number}]")
        return f"Transfer amount {amount} completed successfully"

    def check_balance(self):
        return f"Your account balance is {self.balance}"

    def get_transaction_history(self):
        if not self.transactions:
            return "No Transactions found"
        return "\n".join(self.transactions)

    def get_account_summary(self):
        print(f"\nAccount Summary for {self.name}")
        print(f"Account Number is: {self.account_number}")
        print(f"Account balance is: {self.balance}")
        print(f"Account status: {'Closed' if self.closed else 'Open'}")
        print(f"Account lock: {'Locked' if self.locked else 'Unlocked'}")
        print(f"\nRecent Transactions")
        if not self.transactions:
            print("No transaction is found")
        else:
            for t in self.transactions[-5:]:
                print(f"- {t}")

    def close_account(self):
        self.closed = True
        return "Account has been closed"

    def lock_account(self):
        self.locked = True
        return "Account has been locked."

    def unlock_account(self):
        self.locked = False
        return "Account has been unlocked."

    def __str__(self):
        return f"Account Holder: {self.name}, Balance: {self.balance:,.2f}"


# Sample test
if __name__ == "__main__":
    acc1 = Bank_Account("Bilal", 100)
    acc2 = Bank_Account("Noor", 50)

    print(acc1.deposit(500))
    print(acc1.withdraw(1000))
    print(acc1.deposit(550))
    print(acc1.withdraw(1000))
    print(acc1.check_balance())

    print(acc1.get_transaction_history())
    print(acc2.get_transaction_history())

    print(acc1.transfer(acc2, 20))

    print(acc1.get_transaction_history())
    print(acc2.get_transaction_history())

    acc1.get_account_summary()
    acc2.get_account_summary()

    acc1.lock_account()
    acc1.get_account_summary()

    # Uncomment to test locked account deposit:
    # print(acc1.deposit(90))
