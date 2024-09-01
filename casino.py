import sqlite3
import random

class Casino:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.initialize_db()

    def update(self, login, bet, success, db , cursor):
        modify_user = '+' if success else '-'
        modify_casino = '-' if success else '+'
        try:
            cursor.execute(f"UPDATE users SET balance = balance {modify_user} ? WHERE login = ?", [bet, login])
            cursor.execute(f"UPDATE casino SET balance = balance {modify_casino} ?", [bet])
            db.commit()
        except sqlite3.Error as err:
            print(" ошибка: ", err)
        finally: 
            print('Работа завершина')
            cursor.close()
            db.close()

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
        try:
            return sqlite3.connect(self.db_name)
        except sqlite3.Error as err:
            print(" ошибка: ", err)
        finally: 
            print('Работа завершина')

    def play_casino(self, login, bet, guess):
        try:
            db = sqlite3.connect("database.db")
            cursor = db.cursor()
            cursor.execute("SELECT balance FROM users WHERE login = ?", [login])
            balance = int(cursor.fetchone()[0])
            print(f"Баланс игрока: {balance}")
            cursor.execute("SELECT balance FROM casino")
            casino_balance = int(cursor.fetchone()[0])
            print(f"Баланс казино: {casino_balance}")
            if bet <= balance and casino_balance >= bet:
                a,b = random.randint(1,100), random.randint(1,100)
                if any([guess == "<" and a < b, guess == ">" and a > b, guess == "=" and a == b]):
                    self.update(login, bet, True, db , cursor)
                    return True, a,b
                else:
                    self.update(login, bet, False, db , cursor)
                    return False, a,b
            else:
                return None,None,None

        except sqlite3.Error as err:
            print(" ошибка: ", err)
        finally: 
            print('Работа завершина')
            db.close()

    def log_in(self, login, password):
        try:
            db = sqlite3.connect("database.db")
            cursor = db.cursor()
            cursor.execute("SELECT login FROM users WHERE login = ?", [login])
            if cursor.fetchone() is None:
                return False, "Undefind login"
            else:
                cursor.execute("SELECT password FROM users WHERE password = ?", [password])
                if cursor.fetchone() is None:
                    return False, "invalid password"
                else:
                    return True, "welcome"
        except sqlite3.Error as err:
            print(" ошибка: ", err)
        finally:
            print('Работа завершина')
            cursor.close()
            db.close()
    def reg(self, name, age, gender, login, password):
        if  int(age) >= 18:
            try:
                db = sqlite3.connect("database.db")
                cursor = db.cursor()
                cursor.execute("SELECT login FROM users WHERE login = ?", [login])
                if cursor.fetchone() is None:
                    print("Вы успешно зарегистрировались")
                    cursor.execute("""INSERT INTO users(name, age, gender, login, password)
                    VALUES(?, ?, ?, ?, ?)
                    """, [name,age,gender,login,password])
                    db.commit()
                    return True, "Success"
                else:
                    return False, "Login is invalid"
            except sqlite3.Error as err:
                print(" ошибка: ", err)
            finally:
                print('Работа завершина')
                cursor.close()
                db.close()
        else:
            return False, "Age is invalid"      

    def print_db(self):
        print("start")
        try:
            with self.get_connection() as db:
                cursor = db.cursor()
                for data in cursor.execute("SELECT * FROM users"):
                    print(data)
        except sqlite3.Error as err:
            print(" ошибка: ", err)
        finally: 
            print('Работа завершина')
            cursor.close()
            db.close()