"""
Bank Account System Demo
This script demonstrates all the features of the BankAccount system.
Run this to see the system in action!
"""

from bank import Bank_Account
import time

def print_separator():
    print("=" * 60)

def demo_basic_operations():
    """Demonstrate basic banking operations"""
    print("\n BASIC BANKING OPERATIONS DEMO")
    print_separator()
    
    # Create accounts
    print("Creating bank accounts...")
    alice = Bank_Account("Alice Johnson", 1000)
    bob = Bank_Account("Bob Smith", 500)
    
    print(f"{alice}")
    print(f"{bob}")
    
    # Demonstrate deposits
    print("\n DEPOSIT OPERATIONS:")
    print(alice.deposit(250))
    print(bob.deposit(100))
    
    # Demonstrate withdrawals
    print("\n WITHDRAWAL OPERATIONS:")
    print(alice.withdraw(300))
    print(bob.withdraw(200))
    
    # Check balances
    print("\n BALANCE CHECK:")
    print(alice.check_balance())
    print(bob.check_balance())
    
    return alice, bob

def demo_transfer_operations(account1, account2):
    """Demonstrate transfer operations"""
    print("\n TRANSFER OPERATIONS DEMO")
    print_separator()
    
    print("Before transfer:")
    print(f"   {account1}")
    print(f"   {account2}")
    
    # Perform transfer
    print(f"\nTransferring $150 from {account1.name} to {account2.name}...")
    result = account1.transfer(account2, 150)
    print(f" {result}")
    
    print("\nAfter transfer:")
    print(f"   {account1}")
    print(f"   {account2}")

def demo_transaction_history(account1, account2):
    """Demonstrate transaction history"""
    print("\n TRANSACTION HISTORY DEMO")
    print_separator()
    
    print(f" {account1.name}'s Transaction History:")
    print(account1.get_transaction_history())
    
    print(f"\n {account2.name}'s Transaction History:")
    print(account2.get_transaction_history())

def demo_account_management(account1, account2):
    """Demonstrate account management features"""
    print("\n ACCOUNT MANAGEMENT DEMO")
    print_separator()
    
    # Show account summaries
    print("Account Summaries:")
    account1.get_account_summary()
    print()
    account2.get_account_summary()
    
    # Demonstrate account locking
    print(f"\n Locking {account1.name}'s account...")
    print(account1.lock_account())
    
    # Try to perform operations on locked account
    print(f"\n Attempting to deposit to locked account...")
    try:
        account1.deposit(100)
    except ValueError as e:
        print(f"   Error: {e}")
    
    # Unlock account
    print(f"\n Unlocking {account1.name}'s account...")
    print(account1.unlock_account())
    
    # Try deposit again
    print(f"\n Attempting to deposit to unlocked account...")
    print(account1.deposit(100))

def demo_error_handling():
    """Demonstrate error handling"""
    print("\n ERROR HANDLING DEMO")
    print_separator()
    
    test_account = Bank_Account("Test User", 100)
    
    print("Testing invalid deposit amounts:")
    try:
        test_account.deposit(-50)
    except ValueError as e:
        print(f"    Error: {e}")
    
    try:
        test_account.deposit("invalid")
    except ValueError as e:
        print(f"    Error: {e}")
    
    print("\nTesting insufficient balance withdrawal:")
    try:
        test_account.withdraw(1000)
    except:
        print("    Withdrawal failed due to insufficient balance")
    
    print("\nTesting transfer to self:")
    try:
        test_account.transfer(test_account, 50)
    except ValueError as e:
        print(f"    Error: {e}")

def demo_account_closing():
    """Demonstrate account closing functionality"""
    print("\n ACCOUNT CLOSING DEMO")
    print_separator()
    
    closing_account = Bank_Account("Closing User", 200)
    print(f"Created account: {closing_account}")
    
    # Close the account
    print(f"\nClosing {closing_account.name}'s account...")
    print(closing_account.close_account())
    
    # Try to perform operations on closed account
    print(f"\n Attempting to deposit to closed account...")
    try:
        closing_account.deposit(100)
    except ValueError as e:
        print(f"   Error: {e}")
    
    print(f"\n Attempting to withdraw from closed account...")
    try:
        closing_account.withdraw(50)
    except ValueError as e:
        print(f"   Error: {e}")

def interactive_demo():
    """Interactive demo where user can try operations"""
    print("\n INTERACTIVE DEMO")
    print_separator()
    
    print("Create your own account and try the features!")
    name = input("Enter account holder name: ")
    initial_balance = float(input("Enter initial balance: "))
    
    user_account = Bank_Account(name, initial_balance)
    print(f" Account created: {user_account}")
    
    while True:
        print("\nChoose an operation:")
        print("1. Deposit")
        print("2. Withdraw") 
        print("3. Check Balance")
        print("4. View Transaction History")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            amount = float(input("Enter deposit amount: "))
            try:
                print(user_account.deposit(amount))
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "2":
            amount = float(input("Enter withdrawal amount: "))
            try:
                print(user_account.withdraw(amount))
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "3":
            print(user_account.check_balance())
        
        elif choice == "4":
            print("\nTransaction History:")
            print(user_account.get_transaction_history())
        
        elif choice == "5":
            print("Exiting interactive demo...")
            break
        
        else:
            print("Invalid choice. Please try again.")

def main():
    """Main demo function"""
    print(" WELCOME TO THE BANK ACCOUNT SYSTEM DEMO!")
    print("This demo showcases all the features of our OOP-based banking system.")
    print_separator()
    
    # Run all demo sections
    alice, bob = demo_basic_operations()
    demo_transfer_operations(alice, bob)
    demo_transaction_history(alice, bob)
    demo_account_management(alice, bob)
    demo_error_handling()
    demo_account_closing()
    
    # Interactive demo
    interactive_demo()
    
    print("\n Demo completed! Thanks for exploring the Bank Account System.")
    print("This project demonstrates:")
    print("   • Object-Oriented Programming principles")
    print("   • Encapsulation and data hiding")
    print("   • Error handling and validation")
    print("   • Real-world banking logic")
    print("   • Clean, maintainable code structure")

if __name__ == "__main__":
    main()
