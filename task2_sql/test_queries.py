# File: task2_sql/test_queries.py
# Description: Тесты для проверки SQL-запросов (ORM и нативного).

import unittest
from query_orm import query_orm
from query_native import query_native
import sqlite3

class TestQueries(unittest.TestCase):
    def test_orm_query(self):
        """Проверяет, что ORM-запрос возвращает корректные данные."""
        results = query_orm()
        self.assertGreater(len(results), 0, "ORM-запрос не вернул данных")
        self.assertNotIn(14, [r["UserName"] for r in results], "UserID=14 не исключён")

    def test_native_query(self):
        """Проверяет, что нативный запрос возвращает данные."""
        conn = sqlite3.connect("task2_sql/database.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, u.UserName, d.DataName
            FROM COMMON c
            LEFT JOIN USER u ON c.UserID = u.UserID
            LEFT JOIN DOC d ON c.DataID = d.DataID
            WHERE c.UserID != 14
            AND c.Timestamp > '11-05-2018 12:13'
        """)
        results = cursor.fetchall()
        conn.close()
        self.assertGreater(len(results), 0, "Нативный запрос не вернул данных")

if __name__ == "__main__":
    unittest.main()