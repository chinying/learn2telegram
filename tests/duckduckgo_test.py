import unittest
import json

from bot import duckduckgo

dummy_data = {"Infobox": {
    "content": [
        {
            "data_type": "string",
            "value": "2 November - 10 December 1932",
            "label": "Date",
            "wiki_order": 0
        },
        {
            "data_type": "string",
            "value": "Emus, Sir George Pearce, Major G.P.W. Meredith, Royal Australian Artillery",
            "label": "Participants",
            "wiki_order": 1
        },
        {
            "data_type": "string",
            "value": "Failure. Emu population persists. See Aftermath",
            "label": "Outcome",
            "wiki_order": 2
        }
    ]
}}

class DuckDuckGoTest(unittest.TestCase):
    def test_infoboxBlank(self):
        data = {}
        data["Infobox"] = ""
        self.assertEqual(duckduckgo.infobox(data, {}), "No infobox")

    def test_infoboxAllKeys(self):
        data = dummy_data 
        expected = ("Date: 2 November - 10 December 1932\nParticipants: Emus, Sir George Pearce, Major G.P.W. Meredith, Royal Australian Artillery\nOutcome: Failure. Emu population persists. See Aftermath").split("\n")
        self.assertEqual(duckduckgo.infobox(data, {"_ALL_"}).splitlines(), expected)

    def test_infoboxSubsetKeys(self):
        data = dummy_data
        expected = ("Date: 2 November - 10 December 1932\nParticipants: Emus, Sir George Pearce, Major G.P.W. Meredith, Royal Australian Artillery").split("\n")
        self.assertEqual(duckduckgo.infobox(data, {"Date", "Participants"}).splitlines(), expected)

if __name__ == "__main__":
    unittest.main()
