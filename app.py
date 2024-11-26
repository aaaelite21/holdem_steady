
from src.hand import Hand
#from src.holdem import TexasHoldem

#game = TexasHoldem(["Alice", "Bob", "Carol", "David"])
common_cards = ["9D", "4H", "7S", "8C", "TD"]
hand_1 = Hand.from_strings(["AS", "2C"] + common_cards)
hand_2 = Hand.from_strings(["KS", "QC"] + common_cards)
print(hand_1.score_hand())
print(hand_2.score_hand())
print(hand_1 > hand_2)




# rate = game.simulate(hand=[], number_of_players=5, number_of_rounds=1000)

# print(rate)

# game.print_player_standings()

# # game.take_blinds()

# game.print_player_standings()

# game.deal()

# game.round_of_betting()

# game.flop()

# game.round_of_betting()

# game.turn()

# game.round_of_betting()

# game.river()

# game.round_of_betting()

# winners = game.determine_winner()

# game.distribute_winnings(winners)

# for winner in winners:
#     print(f"{winner[0]} wins!\n\tRank: {winner[1]}\n\tHand: {winner[3]}")

# game.print_player_standings()
