import random


def create_shoe(num_decks):
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


def create_spots(NUM_PLAYERS, CHIPS):
    spots = [{'index': i, 'chips': CHIPS, 'hands': [{'cards': [], 'total': 0, 'soft': False, 'bj': False}]}
             for i in range(NUM_PLAYERS + 1)]
    return spots


def deal_card(shoe, hand, num_cards):
    for x in range(num_cards):
        dealt = shoe[:1]
        hand['cards'].extend(dealt)
        del shoe[:1]
    return True


def reset(spots):
    for player in spots:
        player['hands'] = [
            [{'cards': [], 'total': 0, 'soft': False, 'bj': False}]]
        return True


def update_hands(hand):
    # UPDATE TOTAL
    for card in hand['cards']:
        hand['total'] += card[1]
    # CHECK FOR BJ
    if len(hand['cards']) == 2:
        if hand['total'] == 21:
            hand['bj'] = True
    return
