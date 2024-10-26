from enum import Enum
import random

class PlayerState(Enum):
    ACTIVE = "active"
    FOLDED = "folded"
    ALL_IN = "all-in"
    BUSTED = "busted"

class PlayerActions(Enum):
    FOLD = "Fold"
    CHECK = "Check"
    CALL = "Call"
    RAISE = "Raise"
    ALL_IN = "All-in"

    def __str__(self):
        return self.value

class Attitude(Enum):
    PASSIVE = "passive"
    AGGRESSIVE = "aggressive"
    CHAOTIC = "chaotic"
    PLAYER = "player"

class Player:
    def __init__(self, name, chips=500, attitude=Attitude.PLAYER):
        self.name = name
        self.chips = chips
        self.attitude = attitude
        self.state = PlayerState.ACTIVE
        self.cards = []

    def action(self, game_state):
        if self.attitude == Attitude.PLAYER:
            print(f"Player {self.name}, your hand is: {self.cards}")
            if len(game_state.board_cards) > 0:
                print(f"The board cards are: {game_state.board_cards}")
            available_actions = self.available_actions(game_state)
            available_actions = [str(action) for action in available_actions]
            player_input = input(f"Available actions: {', '.join(available_actions)} ").lower()
            if player_input == "check":
                return PlayerActions.CHECK
            elif player_input == "call":
                return PlayerActions.CALL
            elif player_input == "raise":
                return PlayerActions.RAISE
            elif player_input == "fold":
                return PlayerActions.FOLD
            else:
                print("Invalid input. Please try again.")
                return self.action(game_state)
        else:
            return self.ai_action(game_state)
    
    def ai_action(self, game_state):
        # Placeholder for AI decision-making logic
        if PlayerActions.CALL in self.available_actions(game_state):
            return PlayerActions.CALL
        elif PlayerActions.CHECK in self.available_actions(game_state):
            return PlayerActions.CHECK
        else:
            return PlayerActions.FOLD
    
    def available_actions(self, game_state):
        actions = [PlayerActions.FOLD]
        if self.chips >= game_state.big_blind:
            actions.append(PlayerActions.CALL)
        if self.chips >= game_state.big_blind * 2:
            actions.append(PlayerActions.RAISE)
        return actions


    def receive_card(self, card):
        self.cards.append(card)

    def bet(self, amount):
        if amount > self.chips:
            raise ValueError("Not enough chips to bet that amount")
        self.chips -= amount
        return amount

    def fold(self):
        old_hand = self.cards
        self.cards = []
        return old_hand

    def show_hand(self):
        return self.cards

    def __str__(self):
        return f"Player {self.name} with {self.chips} chips and attitude {self.attitude.value}"