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


# connect = sqlite3.connect('db.sqlite')
# cursor = connect.cursor()

# query1 = """
# CREATE TABLE groups(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     groupName TEXT
# )
# """

# query2 = """
# CREATE TABLE user(
#     id INTEGER PRIMARY KEY,
#     group_id INTEGER,
#     FOREIGN KEY group_id REFERENCES groups id
# )
# """


# cursor.execute(query1)
# connect.commit()
# cursor.execute(query2)
# connect.commit()

# connect.close()
def insert(table_name, cols, data):
    db = sqlite3.connect('db.sqlite')
    cur = db.cursor()

    query = """
        INSERT INTO {0}({1})
        VALUES('{2}');
    """.format(table_name, ",".join(cols), "','".join(data))

    cur.execute(query)

    db.commit()
    db.close()

def get(table_name, cols = "*"):
    db = sqlite3.connect('db.sqlite')
    cur = db.cursor()

    query = """
        SELECT {1} FROM {0}
        """.format(table_name,  cols if cols=="*" else "({0})".format(",".join(cols)))

    cur.execute(query)
    colNames = list(map(lambda x: x[0], cur.description))

    result = []

    for i in cur.fetchall():
        result.append(dict(zip(colNames, i)))
    db.close()

    return result
# insert("groups", ["groupName"], ["Admin"])
# insert("groups", ["groupName"], ["User"])
# insert("groups", ["groupName"], ["Student"])