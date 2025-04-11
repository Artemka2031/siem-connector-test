# File: task1_regex/test_parser.py
# Description: Тесты для проверки парсинга событий, чтобы убедиться, что regex работают корректно.

import unittest
from parser import parse_event

class TestEventParser(unittest.TestCase):
    def test_event_1(self):
        event = "Jun  6 17:51:24 ksmg.loc KSMG: Delete all messages in MTA queues: success, queues: [def]."
        result = parse_event(event, 1)
        self.assertIn("timestamp", result)
        self.assertIn("hostname", result)
        self.assertIn("action", result)
        self.assertEqual(result["hostname"], "ksmg.loc")

    def test_event_2(self):
        event = "<181>Oct 15 2018 07:49:40 HuaweiS6700 %%01SHELL/2/CHANGE_PASSWORD_FAIL(s)[680]:Failed to change the password. (Ip=10.10.185.132, VpnName=, UserName=efros_w, Times=5, FailedReason=many_incorrect_logon_attempts)."
        result = parse_event(event, 2)
        self.assertIn("username", result)
        self.assertEqual(result["username"], "efros_w")

    def test_invalid_event(self):
        event = "Invalid event string."
        result = parse_event(event, 1)
        self.assertIn("error", result)

if __name__ == "__main__":
    unittest.main()