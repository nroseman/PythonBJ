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


def create_spots(NUM_PLAYERS, CHIPS):
    spots = [{'index': i, 'chips': CHIPS, 'hands': [{'cards': [], 'total': 0, 'num_soft_ace': 0, 'bj': False, 'bust': False}]}
             for i in range(NUM_PLAYERS + 1)]
    return spots


def deal_card(shoe, hand, num_cards):
    for x in range(num_cards):
        dealt = shoe[0]
        hand['cards'].append(dealt)
        if dealt[0] == 'A':
            hand['num_soft_ace'] += 1
        del shoe[:1]
        update_hand(hand)
    return True


def reset(spots):
    for player in spots:
        player['hands'] = [
            [{'cards': [], 'total': 0, 'num_soft_ace': 0, 'bj': False, 'bust': False}]]
        return True


def update_hand(hand):
    # UPDATE TOTAL
    hand['total'] += hand['cards'][-1][1]
    # CHECK SOFT ACES
    while hand['num_soft_ace'] and hand['total'] > 21:
        hand['total'] -= 10
        hand['num_soft_ace'] -= 1
    if hand['total'] > 21:
        hand['bust'] == True
    # TODO HANDLE SOFT/HARD ACES
    return True
