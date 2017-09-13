import unittest
from bot import bus

class BusTest(unittest.TestCase):
    def test_load_seats_available(self):
        self.assertEqual(bus.load_to_icon("SEA"), "🔵")
    
    def test_load_standing_available(self):
        self.assertEqual(bus.load_to_icon("SDA"), "🔸")

    def test_load_limited_standing(self):
        self.assertEqual(bus.load_to_icon("LSD"), "🔴")
    
    def test_load_other_syntax(self):
        self.assertEqual(bus.load_to_icon("asdf"), "")

    def test_time_parsing(self):
        self.assertEqual(bus.parse_time("2017-09-13T20:24:55+08:00"), "20:24")