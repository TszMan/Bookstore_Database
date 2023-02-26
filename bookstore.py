import sqlite3
db = sqlite3.connect('ebookstore')
cursor = db.cursor()

#Create a table named books if it doesn't exist
list_of_tables = cursor.execute(
    '''SELECT name FROM sqlite_schema WHERE type='table' AND name='books'; '''
).fetchall()
if list_of_tables == []:
    cursor.execute('''
        CREATE TABLE books(id INTEGER PRIMARY KEY, title TEXT,
                       	author TEXT, qty INTEGER)
        ''')
    id_list = [3001,3002,3003,3004,3005]
    title_list = ['A Tale of Two Cities','''Harry Potter and the Philosopher's Stone''',
    'The Lion, the Witch and the Wardrobe','The Lord of the Rings','Alice in Wonderland']
    author_list = ['Charles Dickens','J.K. Rowling','C. S. Lewis','J.R.R Tolkien','Lewis Carroll']
    qty_list = [30,40,25,37,12]

    for i in range(0,5):    
        id = id_list[i]
        title = title_list[i]
        author = author_list[i]
        qty = qty_list[i]
        cursor.execute('''INSERT INTO books(id, title, author, qty)
                    VALUES(?,?,?,?)''', (id, title, author, qty))
    db.commit()

#===Function Definition===

#function to ask user to enter id according to selected action and check if the id exists, return an existing id
def id_input(action):
    cursor = db.cursor()
    check = 0
    while check == 0:
        if action == "2": 
            input_id = int(input("Please enter id of the book you want to update: "))
        elif action == "3":
            input_id = int(input("Please enter id of the book you want to delete: "))
        else:
            input_id = int(input("Please enter id of the book you want to search: "))
        cursor.execute("SELECT count(*) FROM books WHERE id = ?", (input_id,))
        check=cursor.fetchone()[0]
        if check == 0:
            print("There is no record with this id, please enter again.")
    db.commit()
    return input_id

#function to ask user to enter all attributs for the new record and insert to table accordingly
def enter_book(id, title, author, qty):
    cursor = db.cursor()
    cursor.execute('''INSERT INTO books(id, title, author, qty)
                VALUES(?,?,?,?)''', (id, title, author, qty))
    db.commit()

#fuction to ask user to enter attribute according to which they want to update and update table accordingly
def update_book(update_id, info_select, new_info):
    cursor = db.cursor()
    if info_select == "a":
        cursor.execute('''
        UPDATE books SET title = ? WHERE id = ?
        ''', (new_info,update_id)
        )
        db.commit()
    elif info_select == "b":
        cursor.execute('''
        UPDATE books SET author = ? WHERE id = ?
        ''', (new_info,update_id)
        )
    else:
        cursor.execute('''
        UPDATE books SET qty = ? WHERE id = ?
        ''', (int(new_info),update_id)
        )
    db.commit()

#function to delete the record from the table according to id entered by user
def delete_book(delete_id):
    cursor = db.cursor()
    cursor.execute('''
    DELETE FROM books WHERE id = ?
    ''', (delete_id,)
    )
    db.commit()

#function to select from the table and print the record according to id entered bu user
def search_book(search_id):
    cursor = db.cursor()
    cursor.execute('''
    SELECT id, title, author, qty FROM books WHERE id = ?
    ''',(search_id,)
    )
    for row in cursor:
        print('id:{0} title:{1} author:{2} qty:{3}'.format(row[0],row[1],row[2],row[3]))
    db.commit()    

#User's action
action = ""

while action != "0":
    action = input('''Select one of the following Options below:
    1. Enter book
    2. Update book
    3. Delete book
    4. Search books
    0. Exit
    : ''')

    if action == "1":
        new_id = int(input("Please enter id of the new book: "))
        new_title = input("Please enter title of the new book: ")
        new_author = input("Please enter author of the new book: ")
        new_qty = int(input("Please enter quantity of the new book: "))
        enter_book(new_id, new_title, new_author, new_qty)
        print("The book has been added to the database.")
    
    elif action == "2":
        update_id = id_input(action)
        new_info = ""
        while new_info == "":
            info_select = input('''Please enter the information you want to update: 
            a. Title
            b. Author
            c. Quantity
            ''').lower()
            if info_select == "a":
                new_info = input("Please enter new title of the book: ")
            elif info_select == "b":
                new_info = input("Please enter new author of the book: ")
            elif info_select == "c":
                new_info = input("Please enter new quantity of the book: ")
            else:
                print("You have entered invalid selection, please enter again.")
        update_book(update_id, info_select, new_info)
        print("The book's record in the database ahs been updated.")
    
    elif action == "3":
        delete_id = id_input(action)
        delete_book(delete_id)
        print("The book has been deleted from the database.")
    
    elif action == "4":
        search_id = id_input(action)
        search_book(search_id)
    
    elif action == "0":
        print("Thanks and goodbye.")
    
    else:
        print("You have entered an invalid action, please try again!")