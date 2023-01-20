import sqlite3
db = sqlite3.connect('spamazon_db')
cursor = db.cursor()

# Creates Book class which makes retireved data easier to handle
class Book():
    def __init__(self,id, title, author, quantity):
        self.id = id
        self.title = title
        self.author = author
        self.quantity = quantity

    def __str__(self):
        return f"{self.id:10}  {self.title:50}{self.author:25}{self.quantity:10}"    

book_list = []
table_headers = f"{'ID':10}  {'Title':50}{'Author':25}{'Quantity':10}"

# Builds "warehouse" table in database
def create(db, cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS warehouse(id INTEGER UNIQUE PRIMARY KEY, Title TEXT(50), Author Text(50), Qty INTEGER) ''')
    db.commit()
    

# Adds list of data to empty table
def populate(db, cursor):
    books = [
        (3001, "A Tale Of Two Cities", "Charles Dickens", 30),
        (3002, "Harry Potter And The Philosopher's Stone", "J.K.Rowling", 25),
        (3003, "The Lion, The Witch and The Wardrobe", "C.S.Lewis", 37),
        (3004, "The Lord Of The Rings", "J.R.R.Tolkein", 37),
        (3005, "Alice In Wonderland", "Lewis Carroll", 12)
    ]
    cursor.executemany('''INSERT OR IGNORE INTO warehouse VALUES(?,?,?,?)''', books)
    db.commit()

# checks whether user's menu choice is an available option
def menu_choice(available):
    while True:
        option = input()
        if option in available:
            return option
        else:
            print("Whoops, looks like you've made an invalid choice. Please try again.")

# checks if user input is a valid number
def get_num(message):
    while True:
        try:
            data = int(input(f"{message}"))
            return data
        except TypeError:
            print("Whoops, the data you typed is not valid, please try again.")

# pulls all data from "warehouse" table
def get_all(db, cursor):
    cursor.execute('''SELECT * FROM warehouse''')
    table_data = cursor.fetchall()
    for row in table_data:
        book = Book(row[0], row[1], row[2], row[3])
        book_list.append(book)


# prints data as readable table
def print_table(table_headers, book_list):
    print(table_headers)
    for book in book_list:
        print(book)
    book_list.clear()

# adds new data to "warehouse" table
def add_to_database(data_tuple, db, cursor):
    cursor.execute('''INSERT OR IGNORE INTO warehouse VALUES (?,?,?,?)''', data_tuple)
    db.commit()

# deletes data from table
def remove_book(id, db, cursor):
    cursor.execute(f'''DELETE FROM warehouse WHERE id = {id}''')
    db.commit()

# updates data in table
def alter_database(book_num, field, alteration, db, cursor):
    cursor.execute(f'''UPDATE warehouse SET {field} = "{alteration}" WHERE id = {book_num}''')
    db.commit()

# Searches for specific book data by title or author
def search_book(search_data, db, cursor):
    cursor.execute(f'''SELECT * FROM warehouse WHERE title LIKE \"%{search_data}\"''')
    search_item = cursor.fetchmany()

    for row in search_item:
        book = Book(row[0], row[1], row[2], row[3])
        book_list.append(book)
    

# Searches for specific book data by ID number
def search_book_id( search_data, db, cursor):
    cursor.execute(f'''SELECT * FROM warehouse WHERE id = {search_data}''')
    search_item = cursor.fetchmany()
    for row in search_item:
        book = Book(row[0], row[1], row[2], row[3])
        book_list.append(book)


# accertains whether the table "warehouse" exists then creates and populates if it doesn't
try:
    cursor.execute('''SELECT ID FROM warehouse WHERE TITLE = \"A Tale Of Two Cities\"''')
    
except sqlite3.OperationalError:
    create(db, cursor)
    populate(db, cursor)  


while True:
    print('''\n Welcome to the Spamazon Book Warehouse Management System

    Please select an option from the menu:-
    1. View all books
    2. Search books
    3. Input a new book record
    4. Edit a book record
    5. Delete a book record
    0. Exit \n''')

    option = menu_choice(["1", "2", "3", "4", "5", "0"])
    
    if option == "1":
        # gets all data from database table and prints in a readable format
        table_data = get_all(db, cursor)
        print_table(table_headers,book_list)

    elif option == "2":
        # search book
        print("""\nHow would you like to search?
        
        1. Book ID
        2. Title
        0. Return to main menu\n""")
        feature_choice = menu_choice(["1", "2", "0"])
        if feature_choice == "0":
            pass
        elif feature_choice == "1":
            search_data = get_num("Please enter the ID of the book you are searching for. \n")
            search_book_id(search_data, db, cursor)
        elif feature_choice == "2":
            
            search_data = input(f"Please enter the title of the book you are searching for.\n")
            search_book(search_data, db, cursor)
        if book_list:
            print_table(table_headers,book_list)
        else:
            print("Unable to find requested book. Please try again\n")

    elif option == "3":
        #add new book
        id = get_num("Please enter the book id: ")
        title = input("Please enter title: ")
        author = input("Please enter the author's name: ")
        qty = get_num("Please enter the quantity: ")
        add_to_database((id, title, author, qty), db, cursor)

        pass
    elif option == "4":
        book_num = get_num("Please enter the id number of the book you wish to update")
        print("""What would you like to change?
        1. Title
        2. Author
        3. Quantity
        0. Return to main menu""")
        alt_option = menu_choice(["1", "2", "3", "0"])
        if alt_option == "1":
            field = "Title"
            new_title = input("Please enter the updated title: ")
            alter_database(book_num, field, new_title, db, cursor)

        elif alt_option == "2":
            field = "Author"
            new_author = input("Please enter updated author name: ")
            alter_database(book_num, field, new_author, db, cursor)
        
        elif alt_option == "3":
            field = "Qty"
            new_quant = get_num("Please enter the new quantity: ")
            alter_database(book_num, field, new_quant, db, cursor)


        #alter book data
        pass
    elif option == "5":
        #delete book
        id = get_num("\nPlease ener the ID number of the book you wish to delete or enter '0' to return to menu.\n")
        if id == "0":
            continue
        else:
            remove_book(id, db, cursor)
        pass

    elif option == "4":
        
        #search
        pass
    elif option == "0":
        db.close()
        quit()





