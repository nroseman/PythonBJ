import random


def create_shoe(num_decks):
    # CARD FACES AND VALUES, SUITS IGNORED (FOR NOW)
    cards = [
        {'face': '2', 'value': 2},
        {'face': '3', 'value': 3},
        {'face': '4', 'value': 4},
        {'face': '5', 'value': 5},
        {'face': '6', 'value': 6},
        {'face': '7', 'value': 7},
        {'face': '8', 'value': 8},
        {'face': '9', 'value': 9},
        {'face': '10', 'value': 10},
        {'face': 'J', 'value': 10},
        {'face': 'Q', 'value': 10},
        {'face': 'K', 'value': 10},
        {'face': 'A', 'value': 11}
    ]

    shoe = [(card['face'], card['value']) for card in cards] * 4 * num_decks

    random.shuffle(shoe)

    return shoe


def create_spots(NUM_PLAYERS, CHIPS, wager):
    spots = [{'index': i, 'chips': CHIPS, 'hands': [{'cards': [], 'total': 0, 'num_soft_ace': 0, 'bet': wager, 'result': ''}]}
             for i in range(NUM_PLAYERS + 1)]
    return spots


def new_hand(hands, idx, wager):
    hands.insert(idx, {'cards': [], 'total': 0,
                 'num_soft_ace': 0, 'bet': wager, 'result': ''})
    return True


def reset(spot, wager):
    spot['hands'].clear()
    spot['hands'] = [{'cards': [], 'total': 0,
                      'num_soft_ace': 0, 'bet': wager, 'result': ''}]
    return spot


def deal_card(shoe, hand, num_cards, card=None):
    for x in range(num_cards):
        if card != None:
            dealt = card
        else:
            dealt = shoe.pop(0)
        hand['cards'].append(dealt)
        if dealt[0] == 'A':
            hand['num_soft_ace'] += 1
        update_hand(hand)
    return True


def update_hand(hand):
    # UPDATE TOTAL
    hand['total'] += hand['cards'][-1][1]
    # CHECK SOFT ACES
    while hand['num_soft_ace'] and hand['total'] > 21:
        hand['total'] -= 10
        hand['num_soft_ace'] -= 1
    return True


def check_bj(hand):
    if len(hand['cards']) == 2:
        if hand['total'] == 21:
            return True
    return False


def get_actions(hand, is_dealer=False):
    actions = []

    if hand['total'] > 21:
        return 'bust'
    # DEALER ONLY
    if is_dealer:
        if hand['num_soft_ace'] > 0:
            min_score = 18
        else:
            min_score = 17
        if hand['total'] < min_score:
            return 'hit'
        else:
            return 'stand'
    # PLAYER ONLY
    if hand['result'] == 'double':
        show_hand(hand)
        return 'stand'
    if hand['result'] == 'blackjack':
        return 'blackjack'

    if hand['total'] < 21:
        actions.append('hit')
    if hand['total'] <= 21:
        actions.append('stand')

    if len(hand['cards']) == 2:
        if hand['cards'][0][1] == hand['cards'][1][1]:
            actions.append('split')
        actions.append('double')

    # Get Player Choice
    show_hand(hand)
    option = input(f"What would you like to do {*actions,}? ")

    if option == 'exit':
        exit()
    elif option in actions:
        return option
    else:
        return 'invalid'


def resolve_action(hand, next_action, shoe, hand_idx, player, is_dealer=False):
    if next_action == 'bust':
        show_hand(hand)
        print('bust')
        hand['result'] = 'bust'
        return 'bust'
    if next_action == 'blackjack':
        show_hand(hand)
        print('blackjack!')
        hand['result'] = 'blackjack'
        return 'blackjack'
    if next_action == 'hit':
        deal_card(shoe, hand, 1)
        hand['result'] = ''
    if next_action == 'stand':
        if is_dealer:
            show_hand(hand)
        hand['result'] = 'stand'
        return 'stand'
    if next_action == 'double':
        deal_card(shoe, hand, 1)
        hand['bet'] *= 2
        hand['result'] = 'double'
        return 'double'
    if next_action == 'split':
        cards = hand['cards']
        bet = hand['bet']
        player['hands'].remove(player['hands'][hand_idx])
        for x in range(2):
            new_hand(player['hands'], hand_idx + x, bet)
            deal_card(shoe, player['hands'][hand_idx + x], 1, cards[x])
            deal_card(shoe, player['hands'][hand_idx + x], 1)
        print('spliting')
        print(player['hands'])
        return 'split'


def show_hand(hand):
    for card in hand['cards']:
        print(card[0], end=" ")
    print(f"({hand['total']}", end="")
    if hand['num_soft_ace'] and hand['total'] != 21:
        print(' soft', end="")
    print(')')
    return True


def results(dealer_hand, players, PAYOUT_BJ):
    print('\nROUND RESULTS:')
    # DEALER HAS BLACKJACK
    if dealer_hand == 'blackjack':
        for player in players:
            for hand in player['hands']:
                if hand['result'] == 'blackjack':
                    player['chips'] -= hand['bet']
                    hand['result'] = 'loss'
                else:
                    hand['result'] = 'push'
                print(
                    f"Player {player['index']} Hand {hand_idx} Result: {hand['result']} Chips: {player['chips']}")
    # NO DEALER BLACKJACK
    else:
        for player in players:
            hand_idx = 1
            for hand in player['hands']:
                if hand['result'] == 'blackjack':
                    player['chips'] += int(hand['bet'] * PAYOUT_BJ)
                if hand['result'] == 'bust':
                    player['chips'] -= hand['bet']
                    hand['result'] = 'loss'
                elif dealer_hand['result'] == 'bust':
                    player['chips'] += hand['bet']
                    hand['result'] = 'win'
                elif dealer_hand['total'] > hand['total']:
                    player['chips'] -= hand['bet']
                    hand['result'] = 'loss'
                elif dealer_hand['total'] < hand['total']:
                    player['chips'] += hand['bet']
                    hand['result'] = 'win'
                else:
                    hand['result'] = 'push'
                print(
                    f"Player {player['index']} Hand {hand_idx} Result: {hand['result']} Chips: {player['chips']}")
