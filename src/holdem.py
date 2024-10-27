from enum import Enum
from itertools import combinations
from typing import Counter

from .hand import Hand
from .player import Player, Attitude, PlayerActions, PlayerState
from .deck import Deck

class Round():
    def __init__(self, game):
        self.better:Player = None
        self.bet_amount:int = 0

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
            while len(player.cards) < 2:
                player.cards.append(self.deck.draw_card())

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
    
    def determine_winner(self):
        best_hands = []
        
        for player in self.players:
            combined_cards = player.cards + self.board_cards
            hand = Hand(combined_cards)
            best_hands.append((player.name, hand))

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
            sub_game.players[0].cards = [sub_game.deck.draw_specific_card(card.rank, card.suit) for card in hand]
            sub_game.deal()
            sub_game.flop()
            sub_game.turn()
            sub_game.river()
            winners = sub_game.determine_winner()
            for winner in winners:
                player_index = int(winner[0].name.split()[-1])  # Extract player index from name (e.g., "Player 0")
                wins[player_index] += 1 / len(winners)  # Distribute win equally in case of a tie
        return [win_count/number_of_rounds for win_count in wins]

    def __str__(self):
        return f"Players: {[player.name for player in self.players]}, Pot: {self.pot}, Board: {self.board_cards}"