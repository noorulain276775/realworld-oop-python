from user import LibraryMember, Admin

class LibrarySystem:
    def __init__(self):
        self.book_inventory = {}

    def run(self):
        while True:
            print('\n------ Welcome to the Library System ------')
            name = input("Enter your name: ")
            role = input("Enter your role (Admin/Member): ").strip().lower()

            if role == "admin":
                admin = Admin(name, "Admin")
                self.admin_menu(admin)

            elif role == "member":
                member = LibraryMember(name, "Member")
                self.member_menu(member)

            else:
                print("Invalid role. Please enter either 'Admin' or 'Member'.")

            cont = input("Do you want to continue using the system? (yes/no): ").strip().lower()
            if cont != "yes":
                print("Exiting system... Goodbye!")
                break

    def admin_menu(self, admin):
        while True:
            print(f"\nWelcome, {admin.name} (Admin)")
            print("1. Add Book")
            print("2. Remove Book")
            print("3. View All Books")
            print("4. View Book by ISBN")
            print("5. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                title = input("Enter book title: ")
                author = input("Enter author name: ")
                isbn = int(input("Enter ISBN: "))
                copies = int(input("Enter available copies: "))
                print(admin.add_book(title, author, isbn, copies, self.book_inventory))

            elif choice == "2":
                isbn = int(input("Enter ISBN of book to remove: "))
                print(admin.remove_book(isbn, self.book_inventory))

            elif choice == "3":
                admin.view_all_books(self.book_inventory)

            elif choice == "4":
                isbn = int(input("Enter ISBN: "))
                print(admin.view_books(isbn, self.book_inventory))

            elif choice == "5":
                print("Logging out...\n")
                break

            else:
                print("Invalid choice. Please try again.")

    def member_menu(self, member):
        while True:
            print(f"\nWelcome, {member.name} (Member)")
            print("1. View Available Books")
            print("2. Borrow Book")
            print("3. Return Book")
            print("4. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                member.view_all_available_books(self.book_inventory)

            elif choice == "2":
                isbn = int(input("Enter ISBN to borrow: "))
                print(member.borrow_book(isbn, self.book_inventory))

            elif choice == "3":
                isbn = int(input("Enter ISBN to return: "))
                print(member.return_book(isbn, self.book_inventory))

            elif choice == "4":
                print("Logging out...\n")
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main = LibrarySystem()
    main.run()
