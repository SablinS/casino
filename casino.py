import sqlite3
import random

class Casino:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.initialize_db()

    def initialize_db(self):
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                name VARCHAR(30),
                age INTEGER(3),
                gender INTEGER NOT NULL DEFAULT 1,
                balance INTEGER NOT NULL DEFAULT 2000,
                login VARCHAR(15),
                password VARCHAR(20));
            CREATE TABLE IF NOT EXISTS casino(
                name Varchar(30),
                description TEXT(300),
                balance BIGINT NOT NULL DEFAULT 10000)
            """
            cursor.executescript(query)
            data = cursor.execute("SELECT * FROM casino").fetchone()
            if data is None:
                cursor.execute("INSERT INTO casino(name, description) VALUES(?, ?)", ["Casino", ""])
                db.commit()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def win(self, login, bet):
        with self.get_connection() as db:
            cursor = db.cursor()
            cursor.execute("UPDATE users SET balance = balance + ? WHERE login = ?", [bet, login])
            cursor.execute("UPDATE casino SET balance = balance - ?", [bet])
            db.commit()

    def lose(self, login, bet):
        with self.get_connection() as db:
            cursor = db.cursor()
            cursor.execute("UPDATE users SET balance = balance - ? WHERE login = ?", [bet, login])
            cursor.execute("UPDATE casino SET balance = balance + ?", [bet])
            db.commit()

    def play_casino(self, login, bet, guess):
        with self.get_connection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT balance FROM users WHERE login = ?", [login])
            balance = int(cursor.fetchone()[0])

            cursor.execute("SELECT balance FROM casino")
            casino_balance = int(cursor.fetchone()[0])

            if bet <= balance and casino_balance >= bet:
                a, b = random.randint(1, 100), random.randint(1, 100)
                if (guess == "<" and a < b) or (guess == ">" and a > b) or (guess == "=" and a == b):
                    self.win(login, bet)
                    return True, a, b
                else:
                    self.lose(login, bet)
                    return False, a, b
            else:
                return None, balance, casino_balance

    def log_in(self, login, password):
        with self.get_connection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT login FROM users WHERE login = ?", [login])
            if cursor.fetchone() is None:
                return False, "Login does not exist."
            else:
                cursor.execute("SELECT password FROM users WHERE login = ?", [login])
                if cursor.fetchone()[0] != password:
                    return False, "Password is incorrect."
                else:
                    return True, "Logged in successfully."

    def reg(self, name, age, gender, login, password):
        if int(age) < 18:
            return False, "You must be at least 18 years old to register."
        
        with self.get_connection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT login FROM users WHERE login = ?", [login])
            if cursor.fetchone() is None:
                cursor.execute("""INSERT INTO users(name, age, gender, login, password)
                                   VALUES(?, ?, ?, ?, ?)""",
                                [name, age, gender, login, password])
                db.commit()
                return True, "Registration successful."
            else:
                return False, "Login already exists."
