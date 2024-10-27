
from src.hand import Hand
#from src.holdem import TexasHoldem

#game = TexasHoldem(["Alice", "Bob", "Carol", "David"])

hand = Hand.from_strings(["AD", "KD", "QD", "JD", "TD"])
print(hand.cards)

print(hand.is_royal_flush())


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
