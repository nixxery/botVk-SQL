import sqlite3

# Подключение к БД
connect = sqlite3.connect('db.sqlite')
# Создание курсора для подключения
cursor = connect.cursor()

# query = """
# CREATE TABLE answer(
#     id  INT PRIMARY KEY,
#     msg TEXT,
#     answ TEXT
# )
# """
# cursor.execute(query)


connect = sqlite3.connect('db.sqlite')
cursor = connect.cursor()

query1 = """
CREATE TABLE groups(
    id INT PRIMARY KEY AUTOINCREMENT,
    groupName TEXT
)
"""

query2 = """
CREATE TABLE user(
    id INT PRIMARY KEY,
    FOREIGN KEY group_id REFERENCES groups id
)
"""


cursor.execute(query1)
connect.commit()
cursor.execute(query2)
connect.commit()

