# TODO break into functions:
#       - dealing
#       - evaluating

from create_shoe import create_shoe
import os

os.system('cls' if os.name == 'nt' else 'clear')

num_decks = 2
players = 2


def main():

    shoe = create_shoe(num_decks)
    shoe_length = len(shoe)
    shoe_penetration = int(shoe_length * .75)
    discard = []
    next_action = None
    spots = [[] for spot in range(players + 1)]  # TODO make dict instead?
    bj = False
    soft = False

    while len(discard) < shoe_penetration:
        # deal two cards to players and dealer
        for x, spot in enumerate(spots):
            bj = False
            soft = False
            spot = shoe[:2]
            discard.extend(spot)
            del shoe[:2]

            if x < players:
                total = spot[0][1] + spot[1][1]
                if total == 21:
                    bj = True
                elif "A" in (spot[0][0], spot[1][0]):
                    if total > 21:
                        total -= 10
                    else:
                        soft = True

                print(f"Player {x+1}: {spot[0][0]} {spot[1][0]} ", end="")
                if bj:
                    print("blackjack!")
                elif soft:
                    print(f"(soft {total})")
                else:
                    print(f"({total})")

            else:
                print(f"\nDealer is showing a {spot[0][0]}\n")

    # TODO Add player options
    # for player in range(players):
    #     action = input(f"Player {player+1} (hit, stand)? ")

    # check for win/loss/push


if __name__ == "__main__":
    main()
