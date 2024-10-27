import random
from enum import Enum
from .card import Card, Rank, Suit
class Deck:
    def __init__(self):
        self.reset()
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop() if self.cards else None
    
    def draw_specific_card(self, rank, suit):
        for card in self.cards:
            if card.rank == rank and card.suit == suit:
                self.cards.remove(card)
                return card
        return None

    def reset(self):
        self.cards = [Card(rank, suit) for suit in Suit for rank in Rank]
        self.shuffle()

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return ', '.join([f'{rank} of {suit}' for rank, suit in self.cards])

