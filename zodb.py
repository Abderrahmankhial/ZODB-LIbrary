from hashlib import md5
import os
from time import sleep
import ZODB, ZODB.FileStorage, transaction, persistent,ZODB.config
from art import tprint
import persistent
import persistent.list

'''
structure of the database
{
    book_name ,availability ,barrowed  by who //can be added only by the librarian
    users: (username,passwd) //can be added by both
}
functions:
    borrowBook(book_name)
    returnBook(book_name) #todo add way to ensure that the returned book does exist in the database
    displayAvailableBooks() #todo add way to display all books or the ones that are available
    login(username,passwd)#* good
    signup(username,passwd)#*good
    gui()#todo try and make it in window 
    add_object(obj)#! needs to be tweaked
    whoami()#todo add way to choose between librarian and student preferd to be in sign up precedure
    

Algorithm:
    1-choose between student or librarian
    2-if etudiant
        2.1-choose between borrow or return can display available books
    3-if librarian

'''
class Library: 
    def __init__(self, list_Of_Books,list_of_users):
        self.availableBooks = list_Of_Books
        self.list_of_users =list_of_users
    #display only the bookes that are true in available

    def displayAvailableBooks(self):
        return self.availableBooks
    def get_users(self):
        return self.list_of_users
    #display only the  name and type of users
    def displayUsers(self):
        for user in self.list_of_users:
            print(user)
    def borrowBook(self, bookName,con) :
        x=0
        for book in con:
            if bookName==book[0] and book[1]=="true":
                print("i entered")
                x=True
        
        if x:
            print("You have now borrowed the book")
            
            inter=con
            for i in range(len(inter)):
                if bookName==inter[i][0]:
                    inter[i]=(bookName,"false")
            print("inter",inter)
            connection.root()["available"] = inter
            self.availableBooks=inter
            transaction.commit()
            return True
        else:
            print("Sorry, the book is already borrowed")
            return False
    def returnBook(self, bookName,con):
        x=0
        for book in con:
            if bookName==book[0] and book[1]=="false":
                print("i entered")
                x=True
        
        if x:
            print("Thanks for returning the book")
            
            inter=con
            for i in range(len(inter)):
                if bookName==inter[i][0]:
                    inter[i]=(bookName,"true")
            print("inter",inter)
        else:
            print("Sorry, the book is already returned")
            return False

storage = ZODB.FileStorage.FileStorage('zodb.db')
db = ZODB.DB(storage) #*db = ZODB.DB(None) # Create an in-memory database.
connection = db.open() # Open a connection to the database.
try:
        book_list = Library([connection.root()["available"]],[connection.root()["users"]])
except(KeyError):
        book_list = Library([],[("admin",md5("admin".encode()).hexdigest(),"librarian")])
        connection.root()["available"] = book_list.displayAvailableBooks()
        connection.root()["users"] = book_list.get_users()
        transaction.commit()
        
def add_book(book_name):
    #check if the user is a librarian
    if connection.root()["users"][0][2] == "librarian":
        inter=list(connection.root()["available"])
        inter.append((book_name,"true"))
        connection.root()["available"] = inter
        book_list.displayAvailableBooks().append((book_name,"true"))
        transaction.commit()
        print("Book added")
        return True



def gui():
    tprint("Library for Students",font="slant")
    print("1. Borrow a book")
    print("2. Return a book")
    print("3. Display all books")
    print("4. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        book_list.borrowBook(input("Enter the name of the book you want to borrow: "),connection.root()["available"])
        gui()
    elif choice == "2":
        book_list.returnBook(input("Enter the name of the book you want to return: "),connection.root()["available"])
        gui()
    elif choice == "3":
        print(book_list.displayAvailableBooks())
        gui()
    elif choice == "4":
        exit()
    else:
        print("Invalid choice")
    gui()
def whoami():
    tprint("Choose",font="slant")
    print("1-Librarien")
    print("2-Etudiant")
    choise=int(input())
    if choise ==1:
        gui()
    if choise ==2:
        pass
    else:
        pass
def gui_lib():
    tprint("Library for Librarien",font="slant")
    print("1. Add a book")
    print("2. View all athe users")
    print("3. Display all books")
    print("4. Exit")
    try:
        choice = input("Enter your choice: ")
        if choice == "1":
            add_book(input("Enter the name of the book you want to add: "))
        elif choice == "2":
           print( book_list.displayUsers())
        elif choice == "3":
            print(book_list.displayAvailableBooks())
        elif choice == "4":
            exit()

        else:
            print("Invalid choice")
        gui_lib()
    except(KeyboardInterrupt):
        print("\n Goodbye")
        exit()

def login():
    
    tprint("Login",font="slant")
    
    username=input("Enter your username: ")
    if " "in username:
        print("Username can't contain spaces")
        login()
    passwd=input("Enter your password: ")
    
    
    for i in range(len(book_list.get_users())):

        for j in book_list.get_users()[i]:
            if (md5(passwd.encode()).hexdigest()==j[1]) and j[0]==username:
                connection.root()["log"]=username
                transaction.commit()
                if j[2]=="librarian":
                    gui_lib()
                elif j[2]=="student":
                    gui()
            else:
                pass
    print("Wrong username or password")
    login()            
                
def signup():
    role=["librarian","student"]
    tprint("Signup",font="slant")
    try:
        type=int(input("Who are you : 1-Librarian 2-Student: "))
    except(ValueError):
        print("Invalid choice")
        signup()
    username=input("Enter your username: ")
    if " "in username:
        print("Username can't contain spaces")
        login()
    passwd=input("Enter your password: ")
    passwd_conf=input("Confirm your password: ")
    for i in connection.root()["users"]:
        if username==i[0]:
            print("Username already taken")
            signup()
    if passwd==passwd_conf:
        inter=list(connection.root()["users"])
        inter.append((username,md5(passwd.encode()).hexdigest(),role[int(type)-1]))
        connection.root()["users"] = inter
        book_list.get_users().append((username,md5(passwd.encode()).hexdigest(),role[int(type)-1]))
        transaction.commit()
        tprint("Welcome",font="blocks")
        tprint("you can now login",font="random")
        
        sleep(3)
        login()     
    else:
        print("Passwords don't match")
        signup()
print(book_list.get_users())
x="slm"
while(x!="exit"):
    tprint("Welcome",font="slant")
    tprint("to",font="slant")
    tprint("Library",font="slant")
    try:
        x=input("1-Login\n2-Signup\n")
        if x=="1":
            login()
        elif x=="2":
            signup()
        if x=="exit":
            exit()
        else:
            print("Invalid choice")
    except(KeyboardInterrupt):
        print("\n Goodbye")
        exit()
