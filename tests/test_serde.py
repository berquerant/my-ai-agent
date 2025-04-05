from unittest import TestCase

import my_ai_agent.bot as bot
import my_ai_agent.serde as serde


class TestConverter(TestCase):
    def test_serde(self):
        testcases = [
            ("empty", "", []),
            ("message", "R:C", [bot.Message(role="R", content="C")]),
            ("messages", "R:C---R2:C2", [bot.Message(role="R", content="C"), bot.Message(role="R2", content="C2")]),
        ]
        for title, text, msgs in testcases:
            with self.subTest(title):
                c = serde.Converter(role_separator=":", message_separator="---")
                with self.subTest("into_str"):
                    got = c.into_str(msgs)
                    self.assertEqual(text, got)
                with self.subTest("from_str"):
                    got = c.from_str(text)
                    self.assertEqual(msgs, got)
