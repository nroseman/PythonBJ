from helpers import create_shoe, create_spots, reset, deal_card, play, check_bj, check_split, get_actions, show_hand
import os

os.system('cls' if os.name == 'nt' else 'clear')

NUM_DECKS = 2
NUM_PLAYERS = 2
STARTING_CHIPS = 1000
WAGER = 2
PAYOUT_BJ = 1.5

# TODO:
#   FUNC FOR DECISIONS (HIT/STAND/SPLIT/DOUBLE)
#       - DECISIONS ARE LIST
#       - ON INITIAL -> SPLIT/DOUBLE
#   OFFER INSURANCE


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

        check_bj(dealer['hands'][0])
        if dealer['hands'][0]['bj']:
            print('dealer blackjack')
        # PLAYER DECISION LOOP
        else:
            for player in players:
                print(f"player {player['index']}:")
                for hand in player['hands']:
                    print(
                        f"dealer shows: {dealer['hands'][0]['cards'][0][0]}\n")
                    if len(player['hands']) > 1:
                        print(f"hand {hand['idx']}")
                    action = None
                    is_active = True
                    check_bj(hand)
                    check_split(hand)
                    next_action = ''
                    while next_action != 'end':
                        actions = get_actions(hand)
                        # SHOW PLAYER'S HAND
                        print('Your cards:')
                        show_hand(hand)
                        # PLAYER INPUT DECISION
                        if hand['total'] < 21:
                            options = get_actions(hand)
                            action = input(
                                f"\nWhat would you like to do {options}? ").lower()
                            next_action = play(
                                hand, shoe, action=action, player=player)
                        else:
                            break
                    if hand['bj']:
                        print("Blackjack!\n")
                    elif hand['bust']:
                        print("bust :(\n")
                    else:
                        print('good luck\n')

            # DEALER TURN
            num_busts = 0
            num_hands = 0
            for player in players:
                for hand in player['hands']:
                    num_hands += 1
                    if hand['bust']:
                        num_busts += 1
            if num_busts != num_hands:
                play(dealer['hands'][0], shoe)
        # RESULTS
        print('dealer has:')
        for card in dealer['hands'][0]['cards']:
            print(card[0], end=" ")
        print(f"({dealer['hands'][0]['total']})")
        if dealer['hands'][0]['bust']:
            print('Dealer Busts!')

        print('\nRESULTS\n')
        for player in players:
            count_hand = 1
            result = ''
            winnings = 0
            for hand in player['hands']:
                if hand['bust']:
                    result = 'loss'
                    winnings -= WAGER
                elif dealer['hands'][0]['bust']:
                    result = 'win!'
                    winnings += WAGER
                elif dealer['hands'][0]['total'] > hand['total']:
                    result = 'loss'
                    winnings -= WAGER
                elif dealer['hands'][0]['total'] == hand['total']:
                    result = 'push'
                else:
                    if hand['bj']:
                        winnings += (PAYOUT_BJ * WAGER) - WAGER
                    result = 'win!'
                    winnings += WAGER
                player['chips'] += winnings

                print(
                    f"player {player['index']} hand {count_hand}: {result} chip count: {int(player['chips'])}")
                count_hand += 1

        # END OF ROUND
        for spot in spots:
            spot = reset(spot)
    # END OF SHOE
    print("\nEnd of Shoe\n")


if __name__ == "__main__":
    main()
