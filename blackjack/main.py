from helpers import create_shoe, create_spots, reset, deal_card, update_hand
import os

os.system('cls' if os.name == 'nt' else 'clear')

NUM_DECKS = 2
NUM_PLAYERS = 2
STARTING_CHIPS = 1000


def main():

    # CREATE TABLE
    # NEW SHOE OF CARDS
    shoe = create_shoe(NUM_DECKS)
    # SETUP PLAYERS {INDEX, CHIPS, HANDS: [{CARDS, TOTAL, SOFT, BJ}]}?
    spots = create_spots(NUM_PLAYERS, STARTING_CHIPS)

    # START ROUND
    # INITIAL DEAL
    for spot in spots:
        deal_card(shoe, spot['hands'][0], 2)
        # CHECK BJ
        if spot['hands'][0]['total'] == 21:
            spot['hands'][0]['bj'] = True
    dealer = spots[0]
    players = spots[1:]
    # SHOW DEALER'S UPCARD
    print(f"dealer upcard is: {dealer['hands'][0]['cards'][0][0]}\n")
    # SHOW PLAYERS' CARDS
    for player in players:
        for hand in player['hands']:
            while hand['total'] < 21:
                print(f"player {player['index']}:")
                for card in hand['cards']:
                    print(card[0], end=" ")
                print(f"({hand['total']})")
                action = input(
                    "What would you like to do (stand/hit)? ").lower()
                if action == 'hit':
                    deal_card(shoe, hand, 1)
    # END OF ROUND
    # RESET
    # reset(spots)

    #

    # CHOICES
    # HIT STAND DOUBLE SPLIT
    # DEAL CARD IF APPLICABLE

    # EVALUATE
    # CHECK TOTAL
    # CHECK SOFT
    # CHECK FOR BJ

    # RESOLVE

    # shoe = create_shoe(num_decks)
    # shoe_length = len(shoe)
    # shoe_penetration = int(shoe_length * .75)
    # discard = []
    # next_action = None
    # spots = [[] for spot in range(players + 1)]  # TODO make dict instead?
    # bj = False
    # soft = False

    # while len(discard) < shoe_penetration:
    #     # deal two cards to players and dealer
    #     for x, spot in enumerate(spots):
    #         bj = False
    #         soft = False
    #         spot = shoe[:2]
    #         discard.extend(spot)
    #         del shoe[:2]

    #         if x < players:
    #             total = spot[0][1] + spot[1][1]
    #             if total == 21:
    #                 bj = True
    #             elif "A" in (spot[0][0], spot[1][0]):
    #                 if total > 21:
    #                     total -= 10
    #                 else:
    #                     soft = True

    #             print(f"Player {x+1}: {spot[0][0]} {spot[1][0]} ", end="")
    #             if bj:
    #                 print("blackjack!")
    #             elif soft:
    #                 print(f"(soft {total})")
    #             else:
    #                 print(f"({total})")

    #         else:
    #             print(f"\nDealer is showing a {spot[0][0]}\n")

    # TODO Add player options
    # for player in range(players):
    #     action = input(f"Player {player+1} (hit, stand)? ")

    # check for win/loss/push


if __name__ == "__main__":
    main()
