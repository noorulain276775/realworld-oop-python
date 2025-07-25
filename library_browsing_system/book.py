"""
Book class
Represents a single book in the library.

Encapsulated Attributes:
[title, author, isbn, available_copies]

Methods:
Getters for each detail (e.g. get_title())
borrow_copy()
return_copy()
"""

class Book:
    def __init__(self, title, author, isbn, available_copies):
        self.__title = title
        self.__author = author
        self.__isbn = isbn
        self.__available_copies = available_copies

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_isbn(self):
        return self.__isbn

    def get_available_copies(self):
        return self.__available_copies

    def borrow_copy(self):
        if self.__available_copies > 0:
            self.__available_copies -= 1
            return "Book issued successfully!"
        else:
            return "Book is currently out of stock."

    def return_copy(self):
        self.__available_copies += 1
        return "Book returned successfully!"

    def __str__(self):
        return f"{self.__title} by {self.__author} (ISBN: {self.__isbn}) - Copies: {self.__available_copies}"
