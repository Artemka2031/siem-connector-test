# File: task1_regex/parser.py
# Description: Парсит события логов с помощью регулярных выражений для нормализации в SIEM.
# Extracts at least 3 tokens per event, handles start/end parsing as required.

import re
import json
from typing import Dict, List


def parse_event(event: str, event_id: int) -> Dict[str, str]:
    """
    Парсит одно событие лога, извлекая ключевые токены с помощью regex.

    Args:
        event: Строка события из лога.
        event_id: Номер события (1-4) для выбора правильного regex.

    Returns:
        Словарь с извлечёнными токенами или ошибкой.
    """
    # Убираем точку в конце события, если она есть
    event = event.rstrip(".")

    # Определяем regex для каждого события
    patterns = {
        1: (
            r"^(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+)\s+(?P<hostname>\S+)\s+KSMG:\s+(?P<action>.+)$",
            "Начинаем с начала: извлекаем время, хост и действие."
        ),
        2: (
            r"^\<\d+\>(?P<timestamp>\w+\s+\d+\s+\d+\s+\d+:\d+:\d+)\s+(?P<device>\S+)\s+.*UserName=(?P<username>\w+)",
            "Начинаем с начала: время, устройство, имя пользователя."
        ),
        3: (
            r".*?(?P<error_code>HSCE\d+)\s+User\s+name\s+(?P<username>\S+):.*ID\s+(?P<partition_id>\d+)",
            "Начинаем с конца: код ошибки, имя пользователя, ID раздела."
        ),
        4: (
            r".*?Authentication\s+success:\s+(?P<username>[^\s,]+)\s+from\s+host\s+(?P<host_ip>\d+\.\d+\.\d+\.\d+)\s+with\s+address\s+(?P<source_ip>\d+\.\d+\.\d+\.\d+)",
            "Начинаем с конца: имя пользователя, IP хоста, IP источника."
        )
    }

    try:
        pattern, description = patterns[event_id]
        match = re.search(pattern, event)  # Используем search вместо match для событий 3 и 4
        if not match:
            return {"error": f"Event {event_id} did not match pattern: {event}"}

        # Извлекаем токены в словарь
        result = match.groupdict()
        result["description"] = description
        return result
    except Exception as e:
        return {"error": f"Failed to parse event {event_id}: {str(e)}"}


def main():
    # Пример событий из задания
    events = [
        "Jun  6 17:51:24 ksmg.loc KSMG: Delete all messages in MTA queues: success, queues: [def].",
        "<181>Oct 15 2018 07:49:40 HuaweiS6700 %%01SHELL/2/CHANGE_PASSWORD_FAIL(s)[680]:Failed to change the password. (Ip=10.10.185.132, VpnName=, UserName=efros_w, Times=5, FailedReason=many_incorrect_logon_attempts).",
        "<27>Dec  29 14:50:29 hmc-p730 HMC: HSCE2001 User name hscroot: Logical Partition test with ID 14*8231-E2C*06C5DER failed to be created in managed system Server-8231-E2C-SN06C5DER.",
        "2017/12/26 13:03:12 MSK,0,0,,Authentication Service,Success Access,27,Initial authentication successful,otadmin@otds.admin,,Authentication success: otadmin@otds.admin from host 10.56.70.77 with address 10.56.70.77 for resource __OTDS_AS__."
    ]

    # Парсим каждое событие и сохраняем результаты
    results = []
    for idx, event in enumerate(events, 1):
        parsed = parse_event(event, idx)
        results.append({f"event_{idx}": parsed})

    # Сохраняем результат в JSON для SIEM
    with open("task1_regex/events.json", "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Выводим для проверки
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()