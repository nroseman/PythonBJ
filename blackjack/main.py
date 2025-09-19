from helpers import create_shoe, create_spots, reset, deal_card, check_bj, resolve_action, get_actions, results, show_hand, get_wagers, results_to_file
import os

os.system('cls' if os.name == 'nt' else 'clear')

NUM_DECKS = 2
NUM_PLAYERS = 2
STARTING_CHIPS = 1000
MIN_WAGER = 2
PAYOUT_BJ = 1.5

# TODO:
#   OFFER INSURANCE
#   SHOW CARDS IN RESULTS


def main():

    # CREATE TABLE
    # NEW SHOE OF CARDS
    shoe = create_shoe(NUM_DECKS)
    shoe_penetration = int(len(shoe) * .3)
    # SETUP PLAYERS {INDEX, CHIPS, HANDS: [{CARDS, TOTAL, NUM_SOFT_ACE, RESULT, BET}]}
    spots = create_spots(NUM_PLAYERS, STARTING_CHIPS, MIN_WAGER)
    count_rounds = 0

    # START ROUND
    while len(shoe) >= shoe_penetration:
        count_rounds += 1
        print(f"\n***Round {count_rounds} Begins!***\n")

        # INITIAL DEAL
        for spot in spots:
            deal_card(shoe, spot['hands'][0], 2)
            if check_bj(spot['hands'][0]):
                spot['hands'][0]['result'] = 'blackjack'

        dealer = spots[0]
        players = spots[1:]

        get_wagers(players, MIN_WAGER)

        dealer_hand = dealer['hands'][0]
        dealer_up_card = dealer_hand['cards'][0][0]

        # SHOW STARTING HANDS
        for player in players:
            for hand in player['hands']:
                print(f"Player {player['index']} Hand: ", end='')
                show_hand(hand)
        print(f"Dealer up card: {dealer_up_card}")
        print('---------')

        # DEALER BLACKJACK
        if dealer_hand['result'] == 'blackjack':
            print('dealer blackjack')

        # PLAYER LOOP
        else:
            num_busts = 0
            num_total_hands = 0
            for player in players:
                print(f"\nPlayer {player['index']}")
                print(f"Dealer shows: {dealer_up_card}")
                curr_hand = 1
                while curr_hand <= len(player['hands']):
                    hand_idx = curr_hand - 1
                    print(f"Hand {curr_hand}")
                    hand = player['hands'][hand_idx]
                    next_action = get_actions(hand)
                    resolve_action(hand, next_action, shoe, hand_idx, player)
                    if hand['result'] != '' and hand['result'] != 'split' and hand['result'] != 'double':
                        curr_hand += 1
                        num_total_hands += 1
                        if hand['result'] == 'bust':
                            num_busts += 1

            # DEALER PLAY
            if num_busts < num_total_hands:
                print('Dealers turn')
                while dealer_hand['result'] != 'bust' and dealer_hand['result'] != 'stand':
                    hand = dealer_hand
                    next_action = get_actions(hand, is_dealer=True)
                    resolve_action(hand, next_action, shoe,
                                   0, dealer, is_dealer=True)
            else:
                print('Dealer had:')
                show_hand(dealer_hand)

        # END OF ROUND
        # RESULTS
        results(dealer_hand, players, PAYOUT_BJ)
        results_to_file(spots, count_rounds)

        # CLEAR SPOTS
        for spot in spots:
            spot = reset(spot, MIN_WAGER)
    # END OF SHOE
    print("\nEnd of Shoe\n")


if __name__ == "__main__":
    main()
