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

    def play_casino(self, login):
        try:
            db = sqlite3.connect("database.db")
            cursor = db.cursor()
            cursor.execute("SELECT balance FROM users WHERE login = ?", [login])
            balance = int(cursor.fetchone()[0])
            print(f"Баланс игрока: {balance}")
            cursor.execute("SELECT balance FROM casino")
            casino_balance = int(cursor.fetchone()[0])
            print(f"Баланс казино: {casino_balance}")
            bet = int(input("Введите ставку: "))
            if bet <= balance and casino_balance >= bet:
                a,b = random.randint(1,100), random.randint(1,100)
                c = input(f"{a} ? b. Введите ?(<,>,=): ")
                if any([c == "<" and a < b, c == ">" and a > b, c == "=" and a == b]):
                    print("Вы победили")
                    self.win(login,bet)
                else:
                    print("Вы проиграли") 
                    self.lose(login,bet)
            else:
                print("Недостаточно денег на балансе")
                self.log_in(login)

        except sqlite3.Error as err:
            print(" ошибка: ", err)
        finally: 
            print('Работа завершина')
            cursor.close()
            db.close()

    def enter(self):
        enter_type = input("Вы хотите зарегистрироваться(1) или войти?(2): ")
        if enter_type == "1":
            self.reg()
        elif enter_type == "2":
            self.log_in()
        else:
            pass


    def log_in(self):
        login = input("Login: ")
        password = input("Password: ")
        try:
            db = sqlite3.connect("database.db")
            cursor = db.cursor()
            cursor.execute("SELECT login FROM users WHERE login = ?", [login])
            if cursor.fetchone() is None:
                print("Такого логина нет")
                self.enter()
            else:
                cursor.execute("SELECT password FROM users WHERE password = ?", [password])
                if cursor.fetchone() is None:
                    print("Пароль неверный")
                    self.enter()
                else:
                    print('Вы вошли в систему')
                    self.play_casino(login)
        except sqlite3.Error as err:
            print(" ошибка: ", err)
        finally:
            print('Работа завершина')
            cursor.close()
            db.close()
    def reg(self):
        name = input("Name: ")
        age = input("Age: ")
        gender = input("Gender: ")
        login = input("Login: ")
        password = input("Password: ")
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
                    self.log_in()
                else:
                    print("Такой логин уже есть")
                    self.reg()
            except sqlite3.Error as err:
                print(" ошибка: ", err)
            finally:
                print('Работа завершина')
                cursor.close()
                db.close()
        else:
            print('Вы не можете зарегистрироваться')       
            self.enter() 

with sqlite3.connect("database.db") as db:
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
    try:
        cursor.executescript(query)
        data = cursor.execute("SELECT * FROM casino").fetchone()
        if data is None:
            cursor.execute("""INSERT INTO casino(name, description)
                VALUES(?, ?)""", ["Casino", ""])
            db.commit()
        enter()           
        for data in cursor.execute("SELECT * FROM users"):
            print(data)
    except sqlite3.Error as err:
        print(" ошибка: ", err)
    finally:
        print('Работа завершина')