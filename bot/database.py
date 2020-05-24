import sqlite3
# Подключение к БД
# connect = sqlite3.connect('db.sqlite')
# Создание курсора для подключения
# cursor = connect.cursor()

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
#     CREATE TABLE user(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     group_id INTEGER,
#     FOREIGN KEY (groupId) REFERENCES groups(id)
# )
# """


# cursor.execute(query1)
# connect.commit()
# cursor.execute(query2)
# connect.commit()

# connect.close()
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

def getGroup(userID = None, groupID = None):
    db = sqlite3.connect('db.sqlite')
    cur = db.cursor()

    query = ""

    if userID == None and groupID == None:
        query = """
            SELECT * FROM groups
            JOIN user
            ON groups.id = user.groupId
        """
    elif groupID:
        query = """
            SELECT * FROM groups
            INNER JOIN user
            ON groups.id = user.groupId
            WHERE user.groupId == '{0}'
        """.format(groupID) 
    else:
        query = """
            SELECT * FROM groups
            INNER JOIN user
            ON groups.id = user.groupId
            WHERE user.id == '{0}'
        """.format(userID) 

    cur.execute(query)
    colNames = list(map(lambda x: x[0], cur.description))

    result = []

    for i in cur.fetchall():
        result.append(dict(zip(colNames, i)))
    db.commit()
    db.close()

    return result

def deleteUser(userID = None):
    db = sqlite3.connect('db.sqlite')
    cur = db.cursor()

    if(getGroup(userID)) == []:
        db.commit()
        db.close()
        return "Ошибка, такого пользователя нет в Базе Данных"

    query = ""

    if userID == None:
        query = """
            DELETE FROM user
        """
    else:
        query = """
            DELETE FROM user
            WHERE user.id == '{0}'
        """.format(userID)
    
    cur.execute(query)
    db.commit()
    db.close()

    return "Вы были удалены из базы данных"

# insert("groups", ["id", "groupName"], ["1", "Admin"])
# insert("groups", ["id", "groupName"], ["2", "Student"])
# insert("groups", ["id", "groupName"], ["3", "User"])
print(get("groups"))
# query = """DELETE FROM groups"""
# cursor.execute(query)
# connect.commit()


# Подключение к БД
# connect = sqlite3.connect('db.sqlite')
# Создание курсора для подключения
# cursor = connect.cursor()


# query1 = """
# CREATE TABLE groups(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     groupName TEXT
# )
# """

# query2 = """
#     CREATE TABLE user(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     groupid INTEGER,
#     FOREIGN KEY (groupId) REFERENCES groups(id)
# )
# """


# cursor.execute(query1)
# connect.commit()
# cursor.execute(query2)
# connect.commit()

# connect.close()