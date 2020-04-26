import sqlite3

# Подключение к БД
connect = sqlite3.connect('db.sqlite')
# Создание курсора для подключения
cursor = connect.cursor()

# Для работы создаём запрос query
query = """
CREATE TABLE carsbook (
    id INT PRIMARY,
    mark TEXT,
    color TEXT,
    number TEXT
);
"""

query = """
INSERT INTO carsbook (id, mark, color, number) VALUES (100, 'Toyota', 'red', "М123РС77"),
(110, 'Nissan', 'gray', "А123МР78"),
(120, 'Lexus', 'green', "О887ОО98"),
(130, 'Mazda', 'cyan', "О666УА77"),
(140, 'Mercedes', 'yellow', "М610КА77");

"""
cursor.execute(query)

query = """
SELECT * FROM carsbook
"""
# Выполнение запроса через курсор
cursor.execute(query)

result = cursor.fetchall()
print(result)
# Сохранение состояния
connect.commit()



# Закрываем подключение к БД
connect.close()