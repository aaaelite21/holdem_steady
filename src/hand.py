from typing import Counter
from deck import Card, Suit, Rank
from src.holdem import Hands

# hand.py

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card: Card):
        self.cards.append(card)

    def remove_card(self, card: Card):
        self.cards.remove(card)

    def get_value(self):
        # Assuming Card class has a value attribute
        return sum(card.value for card in self.cards)

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)
    
    @staticmethod
    def from_strings(card_strings: list[str]):
        return Hand([Card.from_string(card_str) for card_str in card_strings])
    
    def score_hand(self, cards:list[Card]) -> tuple[Hands, int, list[Card]]:
        # Placeholder for hand scoring logic
        all_combinations = combinations(cards, 5)

        best_high_card = None
        best_rank = None
        best_hand = None

        for combination in all_combinations:
            rank, high_card = self.rank_hand(combination)
            if best_rank is None or rank > best_rank or (best_rank == rank and high_card > best_high_card):
                best_rank = rank
                best_high_card = high_card
                best_hand = combination

            return best_rank, best_high_card, best_hand
    
    def rank_hand(self, cards) -> tuple[int, int]:
        # Helper function to get the rank of a hand
        if self.is_royal_flush(cards):
            return (Hands.ROYAL_FLUSH, self.get_high_card(cards))
        elif self.is_straight_flush(cards):
            return (Hands.STRAIGHT_FLUSH, self.get_high_card(cards))
        elif self.is_four_of_a_kind(cards):
            return (Hands.FOUR_OF_A_KIND, self.get_high_card(cards))
        elif self.is_full_house(cards):
            return (Hands.FULL_HOUSE, self.get_high_card(cards))
        elif self.is_flush(cards):
            return (Hands.FLUSH, self.get_high_card(cards))
        elif self.is_straight(cards):
            return (Hands.STRAIGHT, self.get_high_card(cards))
        elif self.is_three_of_a_kind(cards):
            return (Hands.THREE_OF_A_KIND, self.get_high_card(cards))
        elif self.is_two_pair(cards):
            return (Hands.TWO_PAIR, self.get_high_card(cards))
        elif self.is_one_pair(cards):
            pair_value = self.get_one_pair_rank(cards)  # Get the rank of the pair
            kickers = sorted([card.rank.value for card in cards if card.rank.value != pair_value], reverse=True)  # Kickers are the highest other cards
            pair = Hands(pair_value + 1)  # Pair of twos is rank 2, etc.
            return (pair, max(kickers))
        else:
            return (Hands.HIGH_CARD, self.get_high_card(cards))
    
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