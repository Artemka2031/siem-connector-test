# File: task3_bash/archive_cron.py
# Description: Альтернатива bash-скрипту для архивации каталогов cron* на Python.

import os
import tarfile
import logging
import platform
from datetime import datetime


def setup_logging():
    """Настраивает логирование в файл, учитывая ОС."""
    log_dir = "/var/log" if platform.system() != "Windows" else "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, "archive_cron.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s: %(message)s"
    )
    # Проверяем, что лог-файл создался
    logging.info("Логирование инициализировано.")


def create_test_cron_dirs(etc_dir):
    """Создаёт тестовые каталоги cron* для Windows/WSL."""
    test_crons = ["cron.d", "cron.daily", "cron.hourly"]
    for cron_dir in test_crons:
        full_path = os.path.join(etc_dir, cron_dir)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            # Создаём пустой файл для теста
            with open(os.path.join(full_path, "test.txt"), "w") as f:
                f.write("Test file")
            logging.info(f"Создан тестовый каталог {full_path}")


def archive_cron_dirs():
    """Архивирует каталоги cron* в /etc/bkp или эквивалент."""
    etc_dir = "/etc" if platform.system() != "Windows" else "test_etc"
    backup_dir = os.path.join(etc_dir, "bkp")

    # Создаём директорию etc для тестов в Windows
    if platform.system() == "Windows" and not os.path.exists(etc_dir):
        os.makedirs(etc_dir)
        logging.info(f"Создан тестовый каталог {etc_dir}")

    # Создаём тестовые cron* каталоги в Windows/WSL
    if platform.system() == "Windows":
        create_test_cron_dirs(etc_dir)

    # Создаём директорию для бэкапов
    if not os.path.exists(backup_dir):
        try:
            os.makedirs(backup_dir)
            logging.info(f"Created backup directory {backup_dir}")
        except Exception as e:
            logging.error(f"Cannot create {backup_dir}: {str(e)}")
            return

    # Ищем и архивируем каталоги
    found_crons = False
    for dir_name in os.listdir(etc_dir):
        if dir_name.startswith("cron") and os.path.isdir(os.path.join(etc_dir, dir_name)):
            found_crons = True
            tar_path = os.path.join(backup_dir, f"{dir_name}.tar.gz")
            try:
                with tarfile.open(tar_path, "w:gz") as tar:
                    tar.add(os.path.join(etc_dir, dir_name), arcname=dir_name)
                logging.info(f"Archived {dir_name} to {tar_path}")
            except Exception as e:
                logging.error(f"Failed to archive {dir_name}: {str(e)}")

    if not found_crons:
        logging.warning("Не найдено каталогов cron* для архивации.")


if __name__ == "__main__":
    setup_logging()
    archive_cron_dirs()