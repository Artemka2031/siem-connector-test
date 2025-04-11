# File: task2_sql/query_native.py
# Description: Выполняет нативный SQL-запрос для объединения таблиц COMMON, USER и DOC.

import sqlite3


def query_native():
    """
    Выполняет SQL-запрос с объединением таблиц, исключая UserID=14 и даты до 11-05-2018 12:13.
    """
    conn = sqlite3.connect("task2_sql/database.db")
    cursor = conn.cursor()

    # Запрос с LEFT JOIN для включения всех записей
    query = """
        SELECT c.*, u.UserName, u.ClientAddress, u.ClientHostName,
               d.DataName, d.DataDetail1, d.DataDetail2, d.DataConfidLevel
        FROM COMMON c
        LEFT JOIN USER u ON c.UserID = u.UserID
        LEFT JOIN DOC d ON c.DataID = d.DataID
        WHERE c.UserID != 14
        AND c.Timestamp > '11-05-2018 12:13'
        ORDER BY c.Timestamp
    """

    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)

    # Отличия для Oracle
    print("\nДля Oracle нужно использовать TO_DATE для фильтрации дат:")
    print("WHERE c.UserID != 14 AND c.Timestamp > TO_DATE('11-05-2018 12:13', 'DD-MM-YYYY HH24:MI')")

    conn.close()


if __name__ == "__main__":
    query_native()