from helpers import create_shoe, create_spots, reset, deal_card, check_bj, resolve_action, get_actions, show_hand
import os

os.system('cls' if os.name == 'nt' else 'clear')

NUM_DECKS = 2
NUM_PLAYERS = 2
STARTING_CHIPS = 1000
WAGER = 2
PAYOUT_BJ = 1.5

# TODO:
#   OFFER INSURANCE
#   DEALER PLAY AND HAND RESULTS


def main():

    # CREATE TABLE
    # NEW SHOE OF CARDS
    shoe = create_shoe(NUM_DECKS)
    shoe_penetration = int(len(shoe) * .3)
    # SETUP PLAYERS {INDEX, CHIPS, HANDS: [{IDX, CARDS, TOTAL, NUM_SOFT_ACE, BJ, CAN_SPILT, CAN_DOUBLE, BUST}]}
    spots = create_spots(NUM_PLAYERS, STARTING_CHIPS)
    count_rounds = 0

    # START ROUND
    while len(shoe) >= shoe_penetration:
        count_rounds += 1
        print(f"\nRound {count_rounds} Begins!\n")
        # INITIAL DEAL
        for spot in spots:
            deal_card(shoe, spot['hands'][0], 2)

        dealer = spots[0]
        players = spots[1:]
        dealer_up_card = dealer['hands'][0]['cards'][0][0]

        check_bj(dealer['hands'][0])
        if dealer['hands'][0]['bj']:
            print('dealer blackjack')

        # PLAYER DECISION LOOP
        else:
            for player in players:
                curr_hand = 1
                while curr_hand <= len(player['hands']):
                    hand = player['hands'][curr_hand - 1]
                    next_action = get_actions(hand)
                    resolve_action(hand, next_action, shoe)
                    if hand['result'] != '' and hand['result'] != 'split':
                        curr_hand += 1

        # END OF ROUND
        for spot in spots:
            spot = reset(spot)
    # END OF SHOE
    print("\nEnd of Shoe\n")


if __name__ == "__main__":
    main()
