from helpers import create_shoe, create_spots, reset, deal_card, play
import os

os.system('cls' if os.name == 'nt' else 'clear')

NUM_DECKS = 2
NUM_PLAYERS = 2
STARTING_CHIPS = 1000
WAGER = 2
PAYOUT_BJ = 1.5


def main():

    # CREATE TABLE
    # NEW SHOE OF CARDS
    shoe = create_shoe(NUM_DECKS)
    shoe_penetration = int(len(shoe) * .75)
    # SETUP PLAYERS {INDEX, CHIPS, HANDS: [{CARDS, TOTAL, NUM_SOFT_ACE, BJ}]}
    spots = create_spots(NUM_PLAYERS, STARTING_CHIPS)
    count_rounds = 0

    # START ROUND
    while len(shoe) >= shoe_penetration:
        count_rounds += 1
        print(f"\nRound {count_rounds} Begins!\n")
        # INITIAL DEAL
        for spot in spots:
            deal_card(shoe, spot['hands'][0], 2)
            # CHECK BJ
            if spot['hands'][0]['total'] == 21:
                spot['hands'][0]['bj'] = True
        dealer = spots[0]
        players = spots[1:]

        if dealer['hands'][0]['bj']:
            print('dealer blackjack')
        else:
            for player in players:
                for hand in player['hands']:
                    is_active = True
                    print(f"dealer shows: {dealer['hands'][0]['cards'][0][0]}")
                    action = ''
                    while action != 'exit':
                        # SHOW PLAYER'S HAND
                        print(f"player {player['index']}:")
                        for card in hand['cards']:
                            print(card[0], end=" ")
                        print(f"({hand['total']}", end="")
                        if hand['num_soft_ace'] and not hand['bj']:
                            print(' soft', end="")
                        print(')')
                        action = ''
                        if hand['total'] < 21:
                            action = input(
                                "What would you like to do (stand/hit)? ").lower()
                            if action == 'hit':
                                deal_card(shoe, hand, 1)
                            if action == 'stand':
                                break
                            if action == 'exit':
                                exit()
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

        # END OF ROUND
        for spot in spots:
            spot = reset(spot)
    # END OF SHOE
    print("\nEnd of Shoe\n")


if __name__ == "__main__":
    main()
