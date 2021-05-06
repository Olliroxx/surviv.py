from survivpy.netManager import ingame
import unittest


class test_packets(unittest.TestCase):
    def test_type1(self):
        import os
        import json
        file = open(os.path.join(os.path.dirname(__file__), "type_01_packet_test_data.json"), "r")
        test_data = json.load(file)
        file.close()
        del json, os
        for pair in test_data:
            actual = bytes(ingame.Type01Packet(pair["input"]).data).hex()
            expected = pair["output"]
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
