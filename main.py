# File: main.py
# Description: Основной скрипт для запуска всех заданий тестового задания Datagile.

import subprocess
import os
import platform
import importlib.util
from task1_regex.parser import main as parse_events
from task2_sql.create_db import create_database
from task2_sql.query_orm import query_orm
from task2_sql.query_native import query_native
from task3_bash.archive_cron import archive_cron_dirs


def check_dependencies():
    """Проверяет наличие необходимых зависимостей."""
    if not importlib.util.find_spec("peewee"):
        print("Ошибка: Модуль peewee не установлен. Установите: pip install peewee")
        return False
    return True


def check_environment():
    """Проверяет окружение и возвращает, можно ли запускать bash."""
    is_windows = platform.system() == "Windows"
    if is_windows:
        print("Обнаружено Windows/WSL. Bash-скрипт будет пропущен.")
        return False
    return True


def run_task1():
    """Запускает задание 1: парсинг событий."""
    print("\n=== Задание 1: Парсинг событий ===")
    try:
        parse_events()
        print("Результат сохранён в task1_regex/events.json")
    except Exception as e:
        print(f"Ошибка в задании 1: {str(e)}")


def run_task2():
    """Запускает задание 2: SQL-запросы."""
    print("\n=== Задание 2: SQL-запросы ===")
    try:
        # Создаём базу данных, если не существует
        if not os.path.exists("task2_sql/database.db"):
            print("Создаём SQLite базу...")
            create_database()
        else:
            print("База данных уже существует.")

        # Запускаем ORM-запрос
        print("\nВыполняем запрос через Peewee ORM:")
        results = query_orm()
        if not results:
            print("ORM-запрос не вернул результатов.")

        # Запускаем нативный SQL-запрос
        print("\nВыполняем нативный SQL-запрос:")
        query_native()
    except Exception as e:
        print(f"Ошибка в задании 2: {str(e)}")


def run_task3():
    """Запускает задание 3: архивация cron*."""
    print("\n=== Задание 3: Архивация каталогов ===")
    can_run_bash = check_environment()
    log_path = "logs/archive_cron.log" if platform.system() == "Windows" else "/var/log/archive_cron.log"
    backup_dir = "test_etc/bkp" if platform.system() == "Windows" else "/etc/bkp"

    try:
        if can_run_bash:
            print("Запускаем bash-скрипт...")
            result = subprocess.run(
                ["bash", "task3_bash/archive_cron.sh"],
                capture_output=True,
                text=True
            )
            print(result.stdout)
            if result.stderr:
                print(f"Ошибки bash-скрипта: {result.stderr}")
        else:
            print("Пропускаем bash-скрипт из-за Windows/WSL.")

        # Запускаем Python-альтернативу
        print("\nЗапускаем Python-альтернативу...")
        archive_cron_dirs()
        print(f"Логи сохранены в {log_path}")
        if os.path.exists(backup_dir):
            print(f"Архивы созданы в {backup_dir}: {os.listdir(backup_dir)}")
        else:
            print(f"Директория {backup_dir} не создана.")
    except Exception as e:
        print(f"Ошибка в задании 3: {str(e)}")


def run_task4():
    """Инструкции для задания 4: rsyslog."""
    print("\n=== Задание 4: Настройка rsyslog ===")
    print("Задание 4 требует ручной настройки. Пожалуйста, прочтите:")
    print("task4_rsyslog/rsyslog_config.txt")
    print("Там описаны шаги для мониторинга /var/log/apache.log и отправки на 10.10.10.10.")
    print("Включает пример лога, фильтр 5xx и TLS для безопасности.")


def main():
    """Запускает все задания последовательно."""
    print("Запуск тестового задания для Datagile SIEM...")

    # Проверяем зависимости
    if not check_dependencies():
        print("Прерываем выполнение из-за отсутствия зависимостей.")
        return

    # Запускаем задания
    run_task1()
    run_task2()
    run_task3()
    run_task4()

    print("\nВсе задания выполнены! Результаты:")
    print("- Задание 1: task1_regex/events.json")
    print("- Задание 2: SQLite база в task2_sql/database.db")
    print(
        "- Задание 3: Архивы в test_etc/bkp (Windows) или /etc/bkp (Linux), логи в logs/archive_cron.log (Windows) или /var/log/archive_cron.log (Linux)")
    print("- Задание 4: Инструкции в task4_rsyslog/rsyslog_config.txt")


if __name__ == "__main__":
    main()