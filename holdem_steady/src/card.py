
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
    
    @staticmethod
    def cards_from_strings(cards_strs:list[str]):
        return [Card.from_string(card_str) for card_str in cards_strs]
    
    @staticmethod
    def from_string(card_str:str):
        # parse format like 2H 3D 4C 5S 6H QH KD AS
        rank_map = {rank.name[0]: rank for rank in Rank}
        suit_map = {suit.name[0]: suit for suit in Suit}
        
        try:
            rank_int = int(card_str[:-1])
        except ValueError:
            rank_char = card_str[:-1]
            rank_int = rank_map[rank_char.upper()].value
        suit_char = card_str[-1]
        
        rank = Rank(rank_int)
        suit = suit_map[suit_char.upper()]

        return Card(rank, suit)        
