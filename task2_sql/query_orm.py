# File: task2_sql/query_orm.py
# Description: Выполняет SQL-запрос через Peewee ORM, объединяя таблицы COMMON, USER и DOC.

from peewee import *

# Подключаемся к базе
db = SqliteDatabase("task2_sql/database.db")


# Определяем модели для таблиц
class Common(Model):
    Timestamp = CharField()
    EventNumber = IntegerField()
    Severity = CharField()
    EventID = IntegerField()
    EventName = CharField()
    UserID = IntegerField(null=True)  # Поле для связи с User
    ServerID = CharField(null=True)
    ServerName = CharField(null=True)
    DeviceID = IntegerField(null=True)
    DeviceName = CharField(null=True)
    DataID = IntegerField(null=True)  # Поле для связи с Doc

    class Meta:
        database = db
        table_name = "COMMON"


class User(Model):
    UserID = IntegerField(primary_key=True)  # Явный первичный ключ
    UserName = CharField()
    ClientAddress = CharField()
    ClientHostName = CharField()

    class Meta:
        database = db
        table_name = "USER"


class Doc(Model):
    DataID = IntegerField(primary_key=True)  # Явный первичный ключ
    DataName = CharField()
    DataDetail1 = CharField()
    DataDetail2 = CharField()
    DataConfidLevel = CharField()

    class Meta:
        database = db
        table_name = "DOC"


def query_orm():
    """
    Выполняет запрос с объединением таблиц, исключая UserID=14 и даты до 11-05-2018 12:13.
    """
    try:
        db.connect()

        # Формируем запрос с явным выбором полей
        query = (Common
                 .select(
            Common.Timestamp,
            Common.EventName,
            User.UserName,
            Doc.DataName
        )
                 .join(User, JOIN.LEFT_OUTER, on=(Common.UserID == User.UserID))
                 .join(Doc, JOIN.LEFT_OUTER, on=(Common.DataID == Doc.DataID))
                 .where(Common.UserID != 14, Common.Timestamp > "11-05-2018 12:13"))

        # Выводим результаты
        results = []
        for row in query:
            result = {
                "Timestamp": row.Timestamp,
                "EventName": row.EventName,
                "UserName": row.UserName or "N/A",
                "DataName": row.DataName or "N/A"
            }
            results.append(result)
            print(f"Event: {result['EventName']}, User: {result['UserName']}, "
                  f"Doc: {result['DataName']}, Time: {result['Timestamp']}")

        return results
    except Exception as e:
        print(f"Ошибка в ORM-запросе: {str(e)}")
        return []
    finally:
        if not db.is_closed():
            db.close()


if __name__ == "__main__":
    query_orm()