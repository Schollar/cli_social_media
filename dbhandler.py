import dbcreds
import mariadb as db


class dbInteraction:
    # Connect function that starts a DB connection and creates a cursor
    def db_connect(self):
        conn = None
        cursor = None
        try:
            conn = db.connect(user=dbcreds.user, password=dbcreds.password,
                              host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
        except db.OperationalError:
            print('Something is wrong with the DB')
        except:
            print('Something went wrong connecting to the DB')
        return conn, cursor
# Disconnect function that takes in the conn and cursor and attempts to close both

    def db_disconnect(self, conn, cursor):
        try:
            cursor.close()
        except:
            print('Error closing cursor')
        try:
            conn.close()
        except:
            print('Error closing connection')
# User login function. Takes in a username and password, runs a select query to see if any Username and pw in DB match. If they do return true, if not false.

    def user_login(self, username, password):
        user = None
        conn, cursor = self.db_connect()
        try:
            cursor.execute(
                "SELECT * FROM hackers WHERE alias =? and password =?", [username, password])
            user = cursor.fetchone()
        except db.OperationalError:
            print('Something is wrong with the db!')
        except db.ProgrammingError:
            print('Error running DB query')
        self.db_disconnect(conn, cursor)
        if(user == None):
            print("Invalid username or password!")
            return False
        else:
            print(f'Welcome ', user[1])
            return True
# Function that takes in the username, and runs a select query to find all posts that DO  belong to user.

    def show_user_posts(self, username):
        posts = []
        conn, cursor = self.db_connect()
        try:
            cursor.execute(
                "select exploits.id, content from exploits inner join hackers on exploits.user_id = hackers.id where alias =?", [username])
            posts = cursor.fetchall()
        except:
            print('Oh no something happened getting your posts.')
        self.db_disconnect(conn, cursor)
        for post in posts:
            print(post[0], '.', post[1])
        return posts
# Function takes in a username, runs a select query to get the userID from username, and then takes in user input as new post content.
# Then run a insert query to insert user input into DB as a new post

    def make_post(self, username):
        userid = None
        try:
            content = input('Write your exploit:')
            conn, cursor = self.db_connect()
            cursor.execute(
                "select id from hackers where alias =?", [username, ])
            user = cursor.fetchone()
            userid = user[0]
            cursor.execute(
                "INSERT INTO exploits(content, user_id) VALUES(?, ?)", [content, userid])
            conn.commit()
        except:
            print('Something happened with making your post. Please try again.')
        self.db_disconnect(conn, cursor)
 # Function that takes in the username, and runs a select query to find all posts that DO NOT belong to user.

    def show_other_posts(self, username):
        posts = []
        conn, cursor = self.db_connect()
        try:
            cursor.execute(
                "select exploits.id, content, alias from exploits inner join hackers on exploits.user_id = hackers.id where alias !=?", [username])
            posts = cursor.fetchall()
        except:
            print('Oh no something happened getting the other users postss.')
        self.db_disconnect(conn, cursor)
        for post in posts:
            print(post[2], ': ', post[1])
        return posts
# Function takes in a username, runs our show user posts function to show the posts of this user, takes in user input for what post they want to edit
# Also takes in user input of new content for the post being edited, and finally runs a update query to update the post content

    def modify_post(self, username):
        self.show_user_posts(username)
        try:
            selection = int(input(
                'Input postId number of the exploit you want to edit:'))
            new_content = input('Write your new post: ')
            conn, cursor = self.db_connect()
            cursor.execute(
                "UPDATE exploits SET content = ? WHERE exploits.id = ?", [new_content, selection])
            conn.commit()
        except:
            print('Oh no something happened updating the post')

        self.db_disconnect(conn, cursor)
