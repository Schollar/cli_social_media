import dbhandler as dbi
import getpass as gp
db = dbi.dbInteraction()

# Getting the username and password from user as inputs, then sending them off to our user login function
# If user login function returns false we exit the program, if true we continue on with the program


def log_in():
    try:
        print('Please login to continue')
        print("Enter a username: ")
        username = input()
        print("Enter a password: ")
        password = gp.getpass()
        if(db.user_login(username, password) == False):
            exit()
        else:
            logged_in(username)
    except KeyboardInterrupt:
        print('You have quit the app!')
        exit()

# The main brains of the program. This functions takes in the user selection input and checks it, and calls the appropriate function.


def select_option(username):
    print('Please Select from the following 4 options:')
    print('1.Enter a new exploit')
    print('2.See all of your exploits')
    print('3.See other hackers exploits')
    print('4.Edit one of your exploits')
    print('5.Exit')
    selection = input('Enter a selection: ')
    try:
        if(float(selection) == 1):
            db.make_post(username)
        elif(float(selection) == 2):
            db.show_user_posts(username)
        elif(float(selection) == 3):
            db.show_other_posts(username)
        elif(float(selection) == 4):
            db.modify_post(username)
        elif(float(selection) == 5):
            exit()
        else:
            print('You must make a valid selection!')
    except ValueError:
        print('Sorry you must pick a valid option!')

# Our programs infinite loop, once user is logged in this loops through the function above


def logged_in(username):
    while(True):
        try:
            select_option(username)

        except KeyboardInterrupt:
            print('You have quit the app!')
            exit()


# This is where the app starts, printing the message and then running the log in function
try:
    print('Welcome to Hackers R US!')
    log_in()
except KeyboardInterrupt:
    print('You have quit the app!')
    exit()
