# File: task2_sql/create_db.py
# Description: Создаёт SQLite базу данных с таблицами из задания для выполнения SQL-запросов.

import sqlite3
from datetime import datetime

def create_database():
    """
    Создаёт SQLite базу с таблицами COMMON, USER и DOC, заполняет их данными из задания.
    """
    conn = sqlite3.connect("task2_sql/database.db")
    cursor = conn.cursor()

    # Создаём таблицу COMMON
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS COMMON (
            Timestamp TEXT,
            EventNumber INTEGER,
            Severity TEXT,
            EventID INTEGER,
            EventName TEXT,
            UserID INTEGER,
            ServerID TEXT,
            ServerName TEXT,
            DeviceID INTEGER,
            DeviceName TEXT,
            DataID INTEGER
        )
    """)

    # Создаём таблицу USER
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS USER (
            UserID INTEGER PRIMARY KEY,
            UserName TEXT,
            ClientAddress TEXT,
            ClientHostName TEXT
        )
    """)

    # Создаём таблицу DOC
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS DOC (
            DataID INTEGER PRIMARY KEY,
            DataName TEXT,
            DataDetail1 TEXT,
            DataDetail2 TEXT,
            DataConfidLevel TEXT
        )
    """)

    # Вставляем данные в COMMON
    common_data = [
        ("11-05-2018 12:13:05.135", 1, "Critical", 45, "Печать выходной формы №23", 12, "10.10.10.10", "GEOSERVER.CORP.LOC", 11, "Printer-11", 1245),
        ("12-05-2018 15:55:05.555", 2, "Info", 45, "Печать выходной формы №23", 13, "10.10.10.10", "GEOSERVER.CORP.LOC", 11, "Printer-11", 1145),
        ("13-05-2018 10:35:03.353", 3, "High", 44, "Вывод на экран выходной формы №23", 12, "10.10.10.10", "GEOSERVER.CORP.LOC", 4, "Monitor-4", 1245),
        ("14-05-2018 12:25:00.250", 4, "Info", 44, "Вывод на экран выходной формы №23", 13, "10.10.10.10", "GEOSERVER.CORP.LOC", 4, "Monitor-4", 1145),
        ("15-05-2018 18:43:05.435", 5, "Info", 15, "Успешный вход пользователя", 14, "10.10.10.10", "GEOSERVER.CORP.LOC", None, None, None),
        ("16-05-2018 20:03:55.355", 6, "High", 16, "Неуспешный вход пользователя", 13, "10.10.10.10", "GEOSERVER.CORP.LOC", None, None, None),
        ("18-05-2018 11:23:02.232", 7, "High", 33, "Просмотр защищаемого ресурса", 12, "10.10.10.10", "GEOSERVER.CORP.LOC", None, None, 1246),
    ]
    cursor.executemany("INSERT INTO COMMON VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", common_data)

    # Вставляем данные в USER
    user_data = [
        (12, "Иванов А. А.", "192.168.45.35", "ARM-2.CORP.LOC"),
        (13, "Петров А. А.", "192.168.45.36", "ARM-1.CORP.LOC"),
        (14, "Сидоров А.А.", "192.168.45.37", "ARM-3.CORP.LOC"),
    ]
    cursor.executemany("INSERT INTO USER VALUES (?, ?, ?, ?)", user_data)

    # Вставляем данные в DOC
    doc_data = [
        (1245, "Doc1", "DOC1-1245", "Шифр 'DOC1-1245'", "Коммерческая тайна"),
        (1145, "Doc14", "DOC14-1145", "Шифр 'DOC1-1145'", "Не коммерческая тайна"),
        (1246, "Doc2", "DOC2-1246", "Шифр 'DOC1-1246'", "Коммерческая тайна"),
    ]
    cursor.executemany("INSERT INTO DOC VALUES (?, ?, ?, ?, ?)", doc_data)

    conn.commit()
    conn.close()
    print("Database created successfully.")

if __name__ == "__main__":
    create_database()