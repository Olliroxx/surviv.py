import unittest
from survivpy_net import ingame
from pytest import approx

ASCII_CHARS = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefhijklmnopqrstuvwxyz{|}~"
TARGET_HEX = ("202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f50515253"
              "5455565758595a5b5c5d5e5f6061626364656668696a6b6c6d6e6f707172737475767778797a7b7c7d7e0001fc0102fc0300fcff"
              "01000200fcff03000000fcffffff0100000002000000fcffffff03000000000000fe0000200b5ddc46e5009e999d999d999d9999"
              "9898686b9b686b03")


class test_packets(unittest.TestCase):
    def test_type1(self):
        from os.path import join, dirname
        import json
        file = open(join(dirname(__file__), "type_01_packet_test_data.json"), "r")
        # A thing that gets the correct file irrelevant of the working directory
        test_data = json.load(file)
        file.close()
        for pair in test_data:
            actual = bytes(ingame.Type01Packet(pair["input"]).data).hex()
            expected = pair["output"]
            self.assertEqual(expected, actual)

    def test_bitstring_read_write(self):
        bs = ingame.BitString(bytearray(164))
        bs.write_ascii_str(ASCII_CHARS)
        bs.write_bool(True)
        bs.write_bool(False)
        bs.write_int8(0)
        bs.write_int8(127)
        bs.write_int8(-128)
        bs.write_uint8(0)
        bs.write_uint8(255)
        bs.write_int16(0)
        bs.write_int16(32767)
        bs.write_int16(-32768)
        bs.write_uint16(0)
        bs.write_uint16(65535)
        bs.write_int32(0)
        bs.write_int32(2147483647)
        bs.write_int32(-2147483648)
        bs.write_uint32(0)
        bs.write_uint32(4294967295)
        bs.write_float32(0)
        bs.write_float32(1)
        bs.write_float32(100)
        bs.write_float32(0.0002)
        bs.write_float(-0.0039215686, 1, -1, 8)
        bs.write_float(0.2, 1, -1, 16)
        bs.write_float(3.6, 0, 9, 16)
        bs.write_vec(0, 0, 9, 9, 3.6, 3.6, 16)
        bs.write_unit_vec((-0.707, -0.707), 8)
        bs.write_unit_vec((-0.707, 0.707), 8)
        bs.write_unit_vec((0.707, -0.707), 8)
        bs.write_unit_vec((0.707, 0.707), 8)
        self.assertEqual(TARGET_HEX, bs.get_view().hex())
        bs.index = 0
        self.assertEqual(bs.read_ascii_str(), ASCII_CHARS)
        self.assertEqual(True, bs.read_bool())
        self.assertEqual(False, bs.read_bool())
        self.assertEqual(0, bs.read_int8())
        self.assertEqual(127, bs.read_int8())
        self.assertEqual(-128, bs.read_int8())
        self.assertEqual(0, bs.read_uint8())
        self.assertEqual(255, bs.read_uint8())
        self.assertEqual(0, bs.read_int16())
        self.assertEqual(32767, bs.read_int16())
        self.assertEqual(-32768, bs.read_int16())
        self.assertEqual(0, bs.read_uint16())
        self.assertEqual(65535, bs.read_uint16())
        self.assertEqual(0, bs.read_int32())
        self.assertEqual(2147483647, bs.read_int32())
        self.assertEqual(-2147483648, bs.read_int32())
        self.assertEqual(0, bs.read_uint32())
        self.assertEqual(4294967295, bs.read_uint32())
        self.assertEqual(0, bs.read_float32())
        self.assertEqual(1, bs.read_float32())
        self.assertEqual(100, bs.read_float32())
        self.assertEqual(0.0002, approx(bs.read_float32()))
        self.assertEqual(-0.0039215686, approx(bs.read_float(1, -1, 8), rel=0.1))
        self.assertEqual(0.2, approx(bs.read_float(1, -1, 16), rel=0.1))
        self.assertEqual(3.60013733, approx(bs.read_float(0, 9, 16), rel=0.1))
        self.assertEqual((3.6, 3.6), approx(bs.read_vec(0, 0, 9, 9, 16), rel=0.1))
        self.assertEqual((-0.707, -0.707), approx(bs.read_unit_vec(8), rel=0.1))
        self.assertEqual((-0.707, 0.707), approx(bs.read_unit_vec(8), rel=0.1))
        self.assertEqual((0.707, -0.707), approx(bs.read_unit_vec(8), rel=0.1))
        self.assertEqual((0.707, 0.707), approx(bs.read_unit_vec(8), rel=0.1))


if __name__ == '__main__':
    unittest.main()
