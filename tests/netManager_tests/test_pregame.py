import unittest
from survivpy.netManager import pregame


class test_profile(unittest.TestCase):
    def test_gen_user_id(self):
        self.assertEqual(pregame.Profile._gen_user_id()[18], "-")
        self.assertEqual(pregame.Profile._gen_user_id()[23], "-")
        for _ in range(1000):
            self.assertTrue(int(pregame.Profile._gen_user_id()[8]) in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            self.assertTrue(int(pregame.Profile._gen_user_id()[13]) in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            self.assertTrue(15 & int(pregame.Profile._gen_user_id()[10:12], 16) | 64)
            self.assertTrue(63 & int(pregame.Profile._gen_user_id()[15:17], 16) | 128)


if __name__ == '__main__':
    unittest.main()
