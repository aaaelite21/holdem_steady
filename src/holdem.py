from enum import Enum
from itertools import combinations
from typing import Counter
from .deck import Card, Deck
from .player import Player, Attitude, PlayerActions, PlayerState

class Hands(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    def __str__(self):
        return self.name.replace("_", " ").title()

class TexasHoldem:
    def __init__(self, players, starting_chips=500, big_blind=10):
        self.players = [Player(name, starting_chips, Attitude.CHAOTIC) for name in players]
        self.players[0].attitude = Attitude.PLAYER
        self.deck = Deck()
        self.pot = 0
        self.board_cards = []
        self.big_blind = big_blind

    def deal(self):
        self.deck.shuffle()
        for player in self.players:
            while len(player.hand) < 2:
                player.hand.append(self.deck.draw_card())

    def round_of_betting(self):
        for player in self.players:
            action = player.action(self)
            if action == PlayerActions.FOLD:
                self.players.index(player).state = PlayerState.FOLDED
            elif action == PlayerActions.CALL:
                player.bet(self.big_blind)
                self.add_to_pot(self.big_blind)
            elif action == PlayerActions.RAISE:
                #todo raise logic
                player.bet(20)
                self.add_to_pot(20)
                
    def flop(self):
        self.board_cards.extend([self.deck.draw_card() for _ in range(3)])

    def turn(self):
        self.board_cards.append(self.deck.draw_card())

    def river(self):
        self.board_cards.append(self.deck.draw_card())

    def add_to_pot(self, amount):
        self.pot += amount

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
    
    def rank_hand(self, cards) -> tuple[Hands, int]:
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
            return (Hands.ONE_PAIR, max(kickers))
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
        return pair_rank[0].value if pair_rank else None
    
    def determine_winner(self):
        best_hands = []
        
        for player in self.players:
            combined_cards = player.hand + self.board_cards
            best_rank, high_card, five_card_hand = self.score_hand(combined_cards)
            best_hands.append((player.name, best_rank, high_card, five_card_hand))

        #sort best_rank and high_card
        best_hands.sort(reverse=True, key=lambda x: x[2])
        best_hands.sort(reverse=True, key=lambda x: x[1].value)

        # The winning hand(s)
        winners = [best_hands[0]]

        # Check for ties
        for hand in best_hands[1:]:
            # Compare rank and card values to see if they tie with the current winner(s)
            if hand[1] == winners[0][1] and hand[2] == winners[0][2]:  # Same hand rank and card values
                winners.append(hand)
            else:
                break  # If the next hand is worse, stop checking for ties


        return [winner for winner in winners]  # Return the names of the winners
    
    def distribute_winnings(self, winners):
        self.pot -= self.pot % len(winners)
        for winner in winners:
            winning_player = next(player for player in self.players if player.name == winner[0])
            winning_player.chips += (self.pot / len(winners))
        self.pot = 0

    def print_player_standings(self):
        name_string = "\t".join([player.name for player in self.players])
        chips_string = "\t".join([str(player.chips) for player in self.players])
        print(f"Players:\t{name_string}\nChip Count:\t{chips_string}")



    def simulate(self, hand, number_of_players=4, number_of_rounds=1000):
        wins = [0] * number_of_players
        for _ in range(number_of_rounds):
            sub_game = TexasHoldem([Player(f"Player {i}", attitude=Attitude.PASSIVE) for i in range(number_of_players)])
            sub_game.players[0].hand = [sub_game.deck.draw_specific_card(card.rank, card.suit) for card in hand]
            sub_game.deal()
            sub_game.flop()
            sub_game.turn()
            sub_game.river()
            winners = sub_game.determine_winner()
            for winner_name in winners:
                player_index = int(winner_name.split()[-1])  # Extract player index from name (e.g., "Player 0")
                wins[player_index] += 1 / len(winners)  # Distribute win equally in case of a tie
        return [win_count/number_of_rounds for win_count in wins]

    def __str__(self):
        return f"Players: {[player.name for player in self.players]}, Pot: {self.pot}, Board: {self.board_cards}"