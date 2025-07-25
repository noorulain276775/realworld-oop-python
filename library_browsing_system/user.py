"""
Functionalities:
1. Admin can add a book
2. Admin can remove a book
3. Admin can view all books
4. Member can view available books
5. Member can borrow a book
6. Member can return a book
7. Basic input menu for role-based access
"""

import uuid
from book import Book

class User:
    def __init__(self, name, role):
        self.name = name
        self.id = str(uuid.uuid4().int)[:5]
        self.role = role

    def __str__(self):
        return f'User name: {self.name}, ID: {self.id}, Role: {self.role}'

class Admin(User):
    def __init__(self, name, role):
        super().__init__(name, role)

    def add_book(self, title, author, isbn, available_copies, book_inventory):
        if isbn in book_inventory:
            return f"Book with ISBN {isbn} already exists."
        new_book = Book(title, author, isbn, available_copies)
        book_inventory[isbn] = new_book
        return f"Book '{title}' added successfully."

    def remove_book(self, isbn, book_inventory):
        if isbn not in book_inventory:
            return f"No book with ISBN {isbn} found."
        del book_inventory[isbn]
        return f"Book with ISBN {isbn} removed successfully."

    def view_books(self, isbn, book_inventory):
        if isbn in book_inventory:
            return str(book_inventory[isbn])
        else:
            return f"Book with ISBN {isbn} not found."

    def view_all_books(self, book_inventory):
        if not book_inventory:
            print("No books available in inventory.")
        else:
            for isbn, book in book_inventory.items():
                print(f"{isbn}: {book}")

class LibraryMember(User):
    def __init__(self, name, role):
        super().__init__(name, role)

    def view_all_available_books(self, book_inventory):
        if not book_inventory:
            print("No books available in inventory.")
        else:
            for isbn, book in book_inventory.items():
                print(f"{isbn}: {book}")

    def borrow_book(self, isbn, book_inventory):
        if isbn in book_inventory:
            book = book_inventory[isbn]
            return book.borrow_copy()
        else:
            return f"Book with ISBN {isbn} not found."

    def return_book(self, isbn, book_inventory):
        if isbn in book_inventory:
            book = book_inventory[isbn]
            return book.return_copy()
        else:
            return f"Book with ISBN {isbn} not found."
