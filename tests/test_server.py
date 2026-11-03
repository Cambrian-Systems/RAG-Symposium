"""Fast tests for launch-option validation, without starting any server.

These use Python's built-in unittest runner. Each test compares accepted inputs
or expected failures; the transport smoke checks separately exercise networking.
"""
import argparse
import unittest

from rag_symposium.server import browser_origin, local_port


class ConnectionTests(unittest.TestCase):
    def test_only_specific_web_origins(self):
        """Allow complete origins, and reject broad access or full page URLs."""
        self.assertEqual(browser_origin("https://client.example/"), "https://client.example")
        self.assertEqual(browser_origin("http://localhost:3000"), "http://localhost:3000")
        for value in ("*", "https://*.example", "https://client.example/path", "file:///tmp",
                      "https://user:password@client.example", "https://client.example?x=y",
                      "https://client.example:99999"):
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                browser_origin(value)

    def test_port_bounds(self):
        """Reject invalid port values before the HTTP listener starts."""
        self.assertEqual(local_port("8765"), 8765)
        for value in ("0", "65536", "abc", "-1"):
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                local_port(value)


if __name__ == "__main__":
    unittest.main()
