import random
from enum import Enum

class Suit(Enum):
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3
    SPADES = 4

    def __str__(self):
        return self.name.title()

class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __str__(self):
        return self.name.title()

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        # print 3 of clubs
        return f'{self.rank.name.title()} of {self.suit.name.title()}'

    def __repr__(self):
        return self.__str__()

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



# Example usage:
# deck = Deck()
# print(deck)
# card = deck.draw_card()
# print(f'Drawn card: {card}')
# print(f'Remaining cards: {len(deck)}')
# deck.reset()
# print(f'Deck after reset: {deck}')
# print(f'Remaining cards: {len(deck)}')

