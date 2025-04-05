from unittest import TestCase

import my_ai_agent.tool as tool


class TestCommand(TestCase):
    def test_run(self):
        c = tool.Command(executable="tests/command_example.py", timeout_seconds=1)

        with self.subTest("help"):
            got = c.help()
            want = tool.Help(
                name="example",
                description="sample",
                schema={
                    "title": "Args",
                    "type": "object",
                },
            )
            self.assertEqual(want, got)

        with self.subTest("run"):
            input = '{"text":"hello"}'
            got = c.run(input)
            self.assertTrue(got.ok)
            self.assertEqual(input, got.stdout)
