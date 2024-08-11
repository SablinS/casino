import sqlite3
import random

def win(login,bet):
    cursor.execute("UPDATE users SET balance = balance + ? WHERE login = ?", [bet, login])
    cursor.execute("UPDATE casino SET balance = balance - ?", [bet])
def lose(login,bet):
    cursor.execute("UPDATE users SET balance = balance - ? WHERE login = ?", [bet, login])
    cursor.execute("UPDATE casino SET balance = balance + ?", [bet])
def play_casino(login):
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
                win(login,bet)
            else:
                print("Вы проиграли") 
                lose(login,bet)
        else:
            print("Недостаточно денег на балансе")
            play_casino(login)

    except sqlite3.Error as err:
        print(" ошибка: ", err)
    finally: 
        print('Работа завершина')
        cursor.close()
        db.close()


def enter():
    enter_type = input("Вы хотите зарегистрироваться(1) или войти?(2): ")
    if enter_type == "1":
        reg()
    elif enter_type == "2":
        log_in()
    else:
        pass
def log_in():
    login = input("Login: ")
    password = input("Password: ")
    try:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("SELECT login FROM users WHERE login = ?", [login])
        if cursor.fetchone() is None:
            print("Такого логина нет")
            enter()
        else:
            cursor.execute("SELECT password FROM users WHERE password = ?", [password])
            if cursor.fetchone() is None:
                print("Пароль неверный")
                enter()
            else:
                print('Вы вошли в систему')
                play_casino(login)
    except sqlite3.Error as err:
        print(" ошибка: ", err)
    finally:
        print('Работа завершина')
        cursor.close()
        db.close()
def reg():
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
                log_in()
            else:
                print("Такой логин уже есть")
                reg()
        except sqlite3.Error as err:
            print(" ошибка: ", err)
        finally:
            print('Работа завершина')
            cursor.close()
            db.close()
    else:
        print('Вы не можете зарегистрироваться')       
        enter() 

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