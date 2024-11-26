import unittest

from src.hand import Hand, PokerScore, PokerHands

# Your test cases will go here
class TestHoldemHand(unittest.TestCase):

    def test_equal(self):
        hand_1 = Hand()
        hand_1.value = PokerScore(PokerHands.PAIR_OF_EIGHTS, 3, [])
        hand_2 = Hand()
        hand_2.value = PokerScore(PokerHands.PAIR_OF_EIGHTS, 3, [])
        assert hand_1 == hand_2, "Hands were not equal"

    def test_less_than(self):
        hand_1 = Hand()
        hand_1.value = PokerScore(PokerHands.PAIR_OF_TWOS, 3, [])
        hand_2 = Hand()
        hand_2.value = PokerScore(PokerHands.PAIR_OF_THREES, 2, [])
        assert hand_1 < hand_2, "Hands were not less than"

    def test_greater_than(self):
        hand_1 = Hand()
        hand_1.value = PokerScore(PokerHands.PAIR_OF_NINES, 10, [])
        hand_2 = Hand()
        hand_2.value = PokerScore(PokerHands.PAIR_OF_EIGHTS, 10, [])
        assert hand_1 > hand_2, "Hands were not greater than"

    def test_less_than_or_equal(self):
        hand_1 = Hand()
        hand_1.value = PokerScore(PokerHands.PAIR_OF_FIVES, 10, [])
        hand_2 = Hand()
        hand_2.value = PokerScore(PokerHands.PAIR_OF_FIVES, 10, [])
        assert hand_1 <= hand_2, "Hands were not less than or equal"

    def test_greater_than_or_equal(self):
        hand_1 = Hand()
        hand_1.value = PokerScore(PokerHands.PAIR_OF_ACES, 10, [])
        hand_2 = Hand()
        hand_2.value = PokerScore(PokerHands.PAIR_OF_ACES, 10, [])
        assert hand_1 >= hand_2, "Hands were not greater than or equal"

    def test_not_equal(self):
        hand_1 = Hand()
        hand_1.value = PokerScore(PokerHands.PAIR_OF_ACES, 11, [])
        hand_2 = Hand()
        hand_2.value = PokerScore(PokerHands.PAIR_OF_ACES, 10, [])
        assert hand_1 != hand_2, "Hands were equal"

    def test_is_royal_flush(self):
        hand = Hand.from_strings(["AD", "KD", "QD", "JD", "TD"])
        assert hand.is_royal_flush(hand.cards), "Hand was not a royal flush"
    
    def test_is_straight_flush(self):
        hand = Hand.from_strings(["9D", "KD", "QD", "JD", "TD"])
        assert hand.is_straight_flush(hand.cards), "Hand was not a straight flush"

    def test_is_four_of_a_kind(self):
        hand = Hand.from_strings(["9D", "9H", "9S", "9C", "TD"])
        assert hand.is_four_of_a_kind(hand.cards), "Hand was not four of a kind"
    
    def test_is_full_house(self):
        hand = Hand.from_strings(["9D", "9H", "9S", "TC", "TD"])
        assert hand.is_full_house(hand.cards), "Hand was not a full house"

    def test_is_flush(self):
        hand = Hand.from_strings(["9D", "KD", "QD", "JD", "TD"])
        assert hand.is_flush(hand.cards), "Hand was not a flush"

    def test_is_straight(self):
        hand = Hand.from_strings(["9D", "KD", "QD", "JD", "TD"])
        assert hand.is_straight(hand.cards), "Hand was not a straight"
    
    def test_is_three_of_a_kind(self):
        hand = Hand.from_strings(["9D", "9H", "9S", "JD", "TD"])
        assert hand.is_three_of_a_kind(hand.cards), "Hand was not three of a kind"
    
    def test_is_two_pair(self):
        hand = Hand.from_strings(["9D", "9H", "JS", "JD", "TD"])
        assert hand.is_two_pair(hand.cards), "Hand was not two pair"
    
    def test_is_pair(self):
        hand = Hand.from_strings(["9D", "9H", "JS", "KD", "TD"])
        assert hand.is_one_pair(hand.cards), "Hand was not a pair"
    
    def test_get_high_card(self):
        hand = Hand.from_strings(["9D", "KH", "JS", "KD", "TD"])
        assert hand.get_high_card(hand.cards) == 13, "High card was not KD"
    
    def test_score_hand_high_card(self):
        common_cards = ["9D", "4H", "7S", "8C", "5D"]
        hand = Hand.from_strings(["AS", "2C"] + common_cards)
        score = hand.score_hand()
        assert score.hand == PokerHands.HIGH_CARD, "Hand was not scored correctly"
    
    def test_score_hand_one_pair(self):
        common_cards = ["AD", "4H", "7S", "8C", "5D"]
        hand = Hand.from_strings(["2S", "2D"] + common_cards)
        score = hand.score_hand()
        assert score.hand == PokerHands.PAIR_OF_TWOS, "Hand was not scored correctly"
        assert score.tie_breaker == 14, "Tie breaker was not 14"
    
    def test_score_hand_one_pair(self):
        common_cards = ["AD", "4H", "7S", "8C", "5D"]
        hand = Hand.from_strings(["2S", "2D"] + common_cards)
        score = hand.score_hand()
        assert score.hand == PokerHands.PAIR_OF_TWOS, "Hand was not scored correctly"
        assert score.tie_breaker == 14, "Tie breaker was not 14"
    
    def test_score_hand_two_pair(self):
        common_cards = ["AD", "4H", "7S", "8C", "5D"]
        hand = Hand.from_strings(["7C", "8D"] + common_cards)
        score = hand.score_hand()
        assert score.hand == PokerHands.TWO_PAIR_EIGHTS_HIGH, "Hand was not scored correctly"
        assert score.tie_breaker == 14, "Tie breaker was not 14"

if __name__ == '__main__':
    unittest.main()
