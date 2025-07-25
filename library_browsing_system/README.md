# Library Browsing System — OOP Mini Project for Beginners

### What is this?
This is a beginner-friendly mini project made in **Python** to understand **Object-Oriented Programming (OOP)** concepts like:

- **Encapsulation**
- **Inheritance**
- **Abstraction (light touch)**
- **Object Reusability**

Built entirely using classes and objects to simulate a **library management system** where users can borrow and return books.
This is a **Command Line Interface (CLI)** based system (no GUI, just simple interactive terminal input/output for beginners who wants to learn)

---

## Who is this for?
- Beginners trying to learn how OOP works.
- Anyone who wants to build a **hands-on project** to understand core concepts.

---

## Functionalities Covered

### User Roles
- **Admin (Inherited from User)**
  - Add a book to the system
  - Remove a book
  - View all books

- **Library Member (Inherited from User)**
  - Browse all books
  - Borrow a book
  - Return a book

---

### Book Info (Encapsulated)
Each book has:
- `title`
- `author`
- `ISBN`
- `available_copies`

The book details are hidden (private attributes), and access is controlled via getter methods.

---

## OOP Concepts Applied

| Concept         | Applied In                                             |
|-----------------|--------------------------------------------------------|
| **Encapsulation** | `Book` class has private attributes and uses getters/setters |
| **Inheritance**   | `Admin` and `LibraryMember` inherit from `User` class        |
| **Abstraction**   | System hides internal implementation from user roles        |
| **Polymorphism**  | Optional: you can extend same method names for different roles |

---

## How to Run

1. Clone the repo  
   ```bash
   git clone https://github.com/noor-ul-ain-ibrahim/library-browsing-system.git
   cd library-browsing-system

2. Run the Python file
    ```bash
    python main.py

3. Follow the menu options in terminal.

## Contributions
This project is primarily for personal portfolio and learning.
Feel free to open issues or submit pull requests if you want to add features or improvements!

## Connect with Me
Follow me on LinkedIn for more projects and updates:
https://www.linkedin.com/in/noor-ul-ain-ibrahim-0782a213a/
