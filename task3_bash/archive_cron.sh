#!/bin/bash

# File: task3_bash/archive_cron.sh
# Description: Архивирует каталоги с префиксом cron* в /etc/bkp с логированием.

# Проверяем, существует ли директория для бэкапов
BACKUP_DIR="/etc/bkp"
if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
    if [ $? -ne 0 ]; then
        echo "Error: Cannot create $BACKUP_DIR" | tee -a /var/log/archive_cron.log
        exit 1
    fi
fi

# Ищем каталоги cron* и архивируем
for dir in /etc/cron*; do
    if [ -d "$dir" ]; then
        dir_name=$(basename "$dir")
        tar -czf "$BACKUP_DIR/$dir_name.tar.gz" -C /etc "$dir_name"
        if [ $? -eq 0 ]; then
            echo "$(date): Archived $dir_name to $BACKUP_DIR/$dir_name.tar.gz" | tee -a /var/log/archive_cron.log
        else
            echo "$(date): Failed to archive $dir_name" | tee -a /var/log/archive_cron.log
        fi
    fi
done

exit 0