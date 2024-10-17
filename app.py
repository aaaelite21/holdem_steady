
from src.holdem import TexasHoldem
game = TexasHoldem(["Alice", "Bob", "Carol", "David"])

# rate = game.simulate(hand=[Card(Rank.ACE, Suit.SPADES), Card(Rank.ACE, Suit.CLUBS)], number_of_players=3, number_of_rounds=1000)

# print(rate)

game.print_player_standings()

game.take_blinds()

game.print_player_standings()

game.deal()

game.round_of_betting()

game.flop()

game.round_of_betting()

game.turn()

game.round_of_betting()

game.river()

game.round_of_betting()

winners = game.determine_winner()

game.distribute_winnings(winners)

for winner in winners:
    print(f"{winner[0]} wins!\n\tRank: {winner[1]}\n\tHand: {winner[3]}")

game.print_player_standings()
