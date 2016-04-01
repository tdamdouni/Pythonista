from unittest import TestCase

from nokiacomposer2wav import parse_ringtone as p

class TestParseRingtone(TestCase):
    def test_basics(self):
        # Regular 1/4 C in 2nd octave
        self.assertEqual(p("4c2"), [("c2", 4)])

        # Sharp
        self.assertEqual(p("4#c2"), [("c#2", 4)])

        # Pause
        self.assertEqual(p("4-"), [("r", 4)])

        # Dot
        self.assertEqual(p("8.c2"), [("c2", -8)])

        # 1/16 and 1/32
        self.assertEqual(p("16c2"), [("c2", 16)])
        self.assertEqual(p("32c2"), [("c2", 32)])
        
        # Space delimiters
        self.assertEqual(p("4c2 4c2"), [("c2", 4), ("c2", 4)])

        # Comma delimiters
        self.assertEqual(p("4c2, 4c2"), [("c2", 4), ("c2", 4)])
        