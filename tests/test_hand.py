import unittest

from src.hand import Hand

# Your test cases will go here
class TestHoldem(unittest.TestCase):

    def test_holdem(self):
        hand_1 = Hand.from_strings(["2D", "3D", "4C", "5S", "6H", "AH", "AS"])
        hand_2 = Hand.from_strings(["2H", "3D", "4C", "5S", "6H", "AC", "AS"])
        assert hand_1 == hand_2, "Hands were not equal"

if __name__ == '__main__':
    unittest.main()
