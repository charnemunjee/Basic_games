import sqlite3

# create 'shelf' database
db = sqlite3.connect('shelf.db')
cursor = db.cursor()

# create database table 'shelf'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS shelf (
    id INTEGER PRIMARY KEY, title TEXT, 
    authorID INTEGER CHAR(4), qty INTEGER
    )''')

# create database table called 'author'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS author (
    id INTEGER PRIMARY KEY, 
    name TEXT, 
    country TEXT
    )''')

db.commit()

def fill_author_info():
    """
    This function fills the 'author' table with
    information about the authors of the books
    in the shelf table
    """
    author_info = [(1290, 'Charles Dickens', 'England'),
                   (8937, 'J.K. Rowling', 'England'),
                   (2356, 'C.S. Lewis', 'Ireland'),
                   (6380, 'J.R.R. Tolkien', 'South Africa'),
                   (5620, 'Lewis Carroll', 'England')]
    cursor.executemany('''INSERT OR IGNORE INTO author (
        id, name, country) VALUES (?,?,?)''', author_info)
    db.commit()


def fill_shelf():
    """This function fills the 'shelf' table with books"""
    book_shelf_input = [
        (3001, 'A Tale of Two Cities', 1290, 30),
        (3002, 'Harry Potter and the Philosopher\'s Stone', 8937, 40),
        (3003, ' The Lion the Witch and the Wardrobe', 2356, 25),
        (3004, 'The Lord of the Rings', 6380, 37),
        (3005, 'Alice\'s Adventures in Wonderland', 5620, 12)
    ]
    cursor.executemany('''INSERT OR IGNORE INTO shelf (
    id, title, authorID, qty) VALUES (?,?,?, ?)''', book_shelf_input)
    db.commit()


def add_book():
    """This function adds information about a book and its
    author to the 'shelf' and 'author' database tables.
    The function asks the user to input the following:
    book name, author, country of author, quantity of books,
    author id
    """
    # assigns the new book a book_id
    cursor.execute("SELECT * FROM shelf")
    row_count = len(cursor.fetchall())
    book_id = row_count + 1 + 3000

    # asks user to input book and author information
    name_input = input('Enter book name: ')
    qty_input = input('Enter quantity: ')
    author_name = input('Enter author name: ')
    author_country = input('Enter author country: ')

    # checks if the author already exists in the
    # 'author' database table
    existing_author = cursor.execute(
        "SELECT id FROM author WHERE name = ? AND country = ?",
        (author_name, author_country)).fetchone()

    # if author already exists in the database, then author ID is
    # set to existing ID in the database to avoid duplicates
    if len(existing_author) == 0:
        author_id_input = input('Enter author ID: ')
    else:
        author_id_input = existing_author[0]

    # input information int the 'shelf' database table
    book_shelf_input = [(book_id, name_input, author_id_input, qty_input)]
    cursor.executemany('''INSERT OR IGNORE INTO shelf (
        id, title, authorID, qty) VALUES (?,?,?,?)''', book_shelf_input)
    db.commit()

    # input information in author database table
    author_input = [(author_id_input, author_name, author_country)]
    cursor.executemany('''INSERT OR IGNORE INTO author (
            id, name, country) VALUES (?,?,?)''', author_input)
    db.commit()


def show_shelf():
    """
    This function prints the contents of the 'shelf' table
    """
    book_shelf = cursor.execute("SELECT * FROM shelf")
    print('Here are the books in your shelf:')
    for row in book_shelf:
        print("---------------------------------------------------------")
        print(f'ID: {row[0]}')
        print(f'title: {row[1]}')
        print(f'author id: {row[2]}')
        print(f'quantity: {row[3]}\n')


def view_book_details():
    """
    This function prints the book title,
    author and country of author for each book
    """
    shelf_information = cursor.execute(
        """SELECT shelf.title, author.name, author.country 
        FROM shelf LEFT JOIN author 
        ON shelf.authorID = author.id""")

    for row in shelf_information:
        print("---------------------------------------------------------")
        print(f'title: {row[0]}')
        print(f'author: {row[1]}')
        print(f'country: {row[2]}\n')


def update_book():
    """
    This function prints the books that are available
    and asks the user to select which book and what
    they want to update. This function allows the
    user to update the quantity, title or author
    or return to the main menu

    """
    show_shelf()
    book_to_update = input('id: ')

    continue_update = True
    while continue_update:
        item_to_change = input('Enter item to change: \n'
                               'q - quantity: \n'
                               't - title: \n'
                               'a - author ID\n'
                               'm - main_menu')
        if item_to_change == 'q':
            new_quantity = int(input('Enter new quantity: '))
            cursor.execute("UPDATE shelf SET qty = ? WHERE id = ?",
                           (new_quantity, book_to_update))
            db.commit()
        elif item_to_change == 'a':
            new_author_id = str(input('Enter new author ID: '))
            cursor.execute("UPDATE shelf SET authorID = ? WHERE id = ?",
                           (new_author_id, book_to_update))
            db.commit()
        elif item_to_change == 't':
            new_title = str(input('Enter new title: '))
            cursor.execute("UPDATE shelf SET title = ? WHERE id = ?",
                           (new_title, book_to_update))
            db.commit()
        elif item_to_change == 'm':
            continue_update = False
        else:
            continue_update = False


def delete_book():
    """
    This function prints the books on the shelf database, asks the user
    for the ID of the book that they would like to
    delete and proceeds to delete the book from the shelf database
    """
    show_shelf()
    id_to_delete = int(input('id: '))
    cursor.execute("DELETE FROM shelf WHERE id = ?",
                   (id_to_delete,))
    db.commit()


def search_book():
    """
    This function searches the shelf database for
    books for a book title and prints the book id,
    the title, author ID and quantity of that book
    """
    title_input = input('Enter book title: ')
    try:
        search_results = cursor.execute(
            "SELECT * FROM shelf WHERE title = ?",
            (title_input,)).fetchall()
        if len(search_results) == 0:
            print("No books found\n")
        else:
            for i in range(len(search_results)):
                print("---------------------------------------------")
                print(
                    f'id: {search_results[i][0]}\n'
                    f'title: {search_results[i][1]}\n'
                    f'authorID: {search_results[i][2]}\n'
                    f'quantity: {search_results[i][3]}\n'
                )
    except sqlite3.Error as error:
        print(error)


fill_author_info()   # create and fill the author table
fill_shelf()    # create and fill the shelf table

# This while loop asks the user what they would
# like to do and calls the specific function
while True:
    user_instruct = input('Welcome to the library. '
                          'What would you like to do?\n'
                          '1 - Enter book\n'
                          '2 - Update book\n'
                          '3 - Delete book\n'
                          '4 - Search book\n'
                          '5 - View details of books\n'
                          '0 - Exit\n')

    if user_instruct == '1':
        add_book()
    elif user_instruct == '2':
        update_book()
    elif user_instruct == '3':
        delete_book()
    elif user_instruct == '4':
        search_book()
    elif user_instruct == '5':
        view_book_details()
    elif user_instruct == '0':
        exit()
