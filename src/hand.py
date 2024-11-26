from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from typing import Counter
from src.card import Card


class PokerHands(Enum):
    HIGH_CARD = 1
    PAIR_OF_TWOS = 2
    PAIR_OF_THREES = 3
    PAIR_OF_FOURS = 4
    PAIR_OF_FIVES = 5
    PAIR_OF_SIXES = 6
    PAIR_OF_SEVENS = 7
    PAIR_OF_EIGHTS = 8
    PAIR_OF_NINES = 9
    PAIR_OF_TENS = 10
    PAIR_OF_JACKS = 11
    PAIR_OF_QUEENS = 12
    PAIR_OF_KINGS = 13
    PAIR_OF_ACES = 14
    TWO_PAIR_THREES_HIGH = 15
    TWO_PAIR_FOURS_HIGH = 16
    TWO_PAIR_FIVES_HIGH = 17
    TWO_PAIR_SIXES_HIGH = 18
    TWO_PAIR_SEVENS_HIGH = 19
    TWO_PAIR_EIGHTS_HIGH = 20
    TWO_PAIR_NINES_HIGH = 21
    TWO_PAIR_TENS_HIGH = 22
    TWO_PAIR_JACKS_HIGH = 23
    TWO_PAIR_QUEENS_HIGH = 24
    TWO_PAIR_KINGS_HIGH = 25
    TWO_PAIR_ACES_HIGH = 26
    THREE_OF_A_KIND = 27
    STRAIGHT = 28
    FLUSH = 29
    FULL_HOUSE = 30
    FOUR_OF_A_KIND = 31
    STRAIGHT_FLUSH = 32
    ROYAL_FLUSH = 33

    # override the comparator functions
    def __lt__(self, other):
        return self.value < other.value
    def __gt__(self, other):
        return self.value > other.value
    def __eq__(self, other):
        return self.value == other.value
    def __le__(self, other):
        return self.value <= other.value
    def __ge__(self, other):
        return self.value >= other.value
    def __ne__(self, other):
        return self.value != other.value
    def __str__(self):
        return self.name.replace("_", " ").title()

@dataclass(frozen=True)
class PokerScore:
    hand: PokerHands
    tie_breaker: int | None = None
    cards: list[Card] | None = None

class Hand:
    @staticmethod
    def from_strings(card_strings: list[str]):
        return Hand([Card.from_string(card_str) for card_str in card_strings])

    def __init__(self, cards: list[Card] = None):
        self.cards = []

        self.value:PokerScore = None

        if cards is not None:
            self.cards = cards

        self.last_known_cards  = self.cards
          
    def __eq__(self, other):
        if not isinstance(other, Hand):
            return False
        self.score_hand()
        other.score_hand()
        return self.value.hand == other.value.hand and self.value.tie_breaker == other.value.tie_breaker
    
    def __lt__(self, other):
        if not isinstance(other, Hand):
            raise NotImplementedError(f"Cannot compare Hand with {type(other)}")
        
        self.score_hand()
        other.score_hand()

        if self.value.hand < other.value.hand:
            return True
        
        if self.value.hand == other.value.hand and self.value.tie_breaker < other.value.tie_breaker:
            return True
    
        return False
    
    def __gt__(self, other):
        if not isinstance(other, Hand):
            raise NotImplementedError(f"Cannot compare Hand with {type(other)}")
        
        self.score_hand()
        other.score_hand()

        if self.value.hand > other.value.hand:
            return True
        
        if self.value.hand == other.value.hand and self.value.tie_breaker > other.value.tie_breaker:
            return True
    
        return False
    
    def __le__(self, other):
        if not isinstance(other, Hand):
            raise NotImplementedError(f"Cannot compare Hand with {type(other)}")
        
        self.score_hand()
        other.score_hand()
        
        if self.value.hand == other.value.hand and self.value.tie_breaker > other.value.tie_breaker:
            return False
        
        if self.value.hand > other.value.hand:
            return False
    
        return True
    
    def __ge__(self, other):
        if not isinstance(other, Hand):
            raise NotImplementedError(f"Cannot compare Hand with {type(other)}")
        
        self.score_hand()
        other.score_hand()

        if self.value.hand == other.value.hand and self.value.tie_breaker < other.value.tie_breaker:
            return False
        
        if self.value.hand < other.value.hand:
            return False
    
        return True
    
    def __ne__(self, other):
        if not isinstance(other, Hand):
            return True
        self.score_hand()
        other.score_hand()
        return self.value.hand != other.value.hand or self.value.tie_breaker != other.value.tie_breaker

    def add_card(self, card: Card):
        self.value = None
        self.cards.append(card)

    def remove_card(self, card: Card):
        self.value = None
        self.cards.remove(card)

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)
    
    def score_hand(self) -> PokerScore:
        if self.value is not None and self.last_known_cards == self.cards:
            return self.value
        all_combinations = combinations(self.cards, 5)

        best_score:PokerScore  = None

        for combination in all_combinations:
            hand_score = self.rank_hand(combination)
            if best_score is None or hand_score.hand > best_score.hand:
                best_score = hand_score

        self.value = best_score
        return best_score
    
    def rank_hand(self, cards) -> PokerScore:
        # Helper function to get the rank of a hand
        if self.is_royal_flush(cards):
            return PokerScore(PokerHands.ROYAL_FLUSH, self.get_high_card(cards), cards)
        elif self.is_straight_flush(cards):
            return PokerScore(PokerHands.STRAIGHT_FLUSH, self.get_high_card(cards), cards)
        elif self.is_four_of_a_kind(cards):
            return PokerScore(PokerHands.FOUR_OF_A_KIND, self.get_high_card(cards), cards)
        elif self.is_full_house(cards):
            return PokerScore(PokerHands.FULL_HOUSE, self.get_high_card(cards), cards)
        elif self.is_flush(cards):
            return PokerScore(PokerHands.FLUSH, self.get_high_card(cards), cards)
        elif self.is_straight(cards):
            return PokerScore(PokerHands.STRAIGHT, self.get_high_card(cards), cards)
        elif self.is_three_of_a_kind(cards):
            return PokerScore(PokerHands.THREE_OF_A_KIND, self.get_high_card(cards), cards)
        elif self.is_two_pair(cards):
            highest_pair = self.get_two_pair_rank(cards)[0]
            return PokerScore(PokerHands(PokerHands.PAIR_OF_ACES.value+highest_pair), self.get_high_card(cards)), cards
        elif self.is_one_pair(cards):
            pair_value = self.get_one_pair_rank(cards)  # Get the rank of the pair
            kickers = sorted([card.rank.value for card in cards if card.rank.value != pair_value], reverse=True)  # Kickers are the highest other cards
            pair = PokerHands(pair_value)  # Pair of twos is rank 2, etc.
            return PokerScore(pair, max(kickers), cards)
        else:
            return PokerScore(PokerHands.HIGH_CARD, self.get_high_card(cards), cards)
    
    # get_high_card
    def get_high_card(self, cards):
        return max(card.rank.value for card in cards)
    
    # Check for flush
    def is_flush(self, cards):
        suits = [card.suit for card in cards]
        return len(set(suits)) == 1
    
    # Check for straight
    def is_straight(self, cards):
        ranks = sorted([card.rank.value for card in cards])
        return ranks == list(range(ranks[0], ranks[0] + 5)) or ranks == [2, 3, 4, 5, 14]  # Handles Ace low straight

    # Check for straight flush
    def is_straight_flush(self, cards):
        return self.is_straight(cards) and self.is_flush(cards)

    # Check for royal flush
    def is_royal_flush(self, cards):
        ranks = [card.rank.value for card in cards]
        return self.is_straight_flush(cards) and sorted(ranks) == [10, 11, 12, 13, 14]

    # Check for four of a kind
    def is_four_of_a_kind(self, cards):
        rank_counts = Counter(card.rank for card in cards)
        return 4 in rank_counts.values()

    def get_four_of_a_kind_rank(self, cards):
        rank_counts = Counter(card.rank for card in cards)
        four_rank = [rank for rank, count in rank_counts.items() if count == 4]
        return four_rank[0].value if four_rank else None

    # Check for full house
    def is_full_house(self, cards):
        rank_counts = Counter(card.rank for card in cards)
        return 3 in rank_counts.values() and 2 in rank_counts.values()

    def get_full_house_rank(self, cards):
        rank_counts = Counter(card.rank for card in cards)
        three_rank = [rank for rank, count in rank_counts.items() if count == 3]
        pair_rank = [rank for rank, count in rank_counts.items() if count == 2]
        return (three_rank[0].value, pair_rank[0].value) if three_rank and pair_rank else None

    # Check for three of a kind
    def is_three_of_a_kind(self, cards):
        rank_counts = Counter(card.rank for card in cards)
        return 3 in rank_counts.values()

    def get_three_of_a_kind_rank(self, cards):
        rank_counts = Counter(card.rank for card in cards)
        three_rank = [rank for rank, count in rank_counts.items() if count == 3]
        return three_rank[0].value if three_rank else None

    # Check for two pair
    def is_two_pair(self, cards):
        rank_counts = Counter(card.rank for card in cards)
        pairs = [rank for rank, count in rank_counts.items() if count == 2]
        return len(pairs) == 2

    def get_two_pair_rank(self, cards):
        rank_counts = Counter(card.rank for card in cards)
        pairs = [rank.value for rank, count in rank_counts.items() if count == 2]
        return sorted(pairs, reverse=True)

    # Check for one pair
    def is_one_pair(self, cards):
        rank_counts = Counter(card.rank for card in cards)
        return 2 in rank_counts.values()

    def get_one_pair_rank(self, cards):
        rank_counts = Counter(card.rank for card in cards)
        pair_rank = [rank for rank, count in rank_counts.items() if count == 2]
        pair_rank.sort(reverse=True)
        return pair_rank[0].value if pair_rank else None