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
    spots = [{'index': i, 'chips': CHIPS, 'hands': [{'idx': i, 'cards': [], 'total': 0, 'num_soft_ace': 0, 'bj': False, 'can_split': False, 'can_double': False, 'doubled': False, 'bust': False}]}
             for i in range(NUM_PLAYERS + 1)]
    return spots


def new_hand(hands):
    index = len(hands)
    hands.append({'idx': index, 'cards': [], 'total': 0, 'num_soft_ace': 0, 'bj': False,
                 'can_split': False, 'can_double': False, 'doubled': False, 'bust': False})
    return True


def deal_card(shoe, hand, num_cards, card=None):
    for x in range(num_cards):
        if card != None:
            dealt = card
        else:
            dealt = shoe[0]
            del shoe[:1]
        hand['cards'].append(dealt)
        if dealt[0] == 'A':
            hand['num_soft_ace'] += 1
        update_hand(hand)
    return True


def reset(spot):
    spot['hands'].clear()
    spot['hands'] = [{'idx': 0, 'cards': [], 'total': 0, 'num_soft_ace': 0,
                      'bj': False, 'can_split': False, 'can_double': False, 'doubled': False, 'bust': False}]
    return spot


def update_hand(hand):
    # UPDATE TOTAL
    hand['total'] += hand['cards'][-1][1]
    # CHECK SOFT ACES
    while hand['num_soft_ace'] and hand['total'] > 21:
        hand['total'] -= 10
        hand['num_soft_ace'] -= 1
    if hand['total'] > 21:
        hand['bust'] = True
    # TODO HANDLE SOFT/HARD ACES
    return True


def play(hand, shoe, action=None, player=False):
    # DEALER
    if not player:
        while not hand['bust']:
            if hand['num_soft_ace'] > 0:
                min_score = 18
            else:
                min_score = 17
            if hand['total'] < min_score:
                deal_card(shoe, hand, 1)
            else:
                return True
    # PLAYER
    else:
        if action == 'hit':
            deal_card(shoe, hand, 1)
        if action == 'stand':
            return 'end'
        if action == 'double' and hand['can_double']:
            deal_card(shoe, hand, 1)
            hand['doubled'] = True
            show_hand(hand)
            return 'end'
        # TODO FIX THIS - ISSUES WITH INDEXING AND REFERENCES
        if action == 'split' and hand['can_split']:
            cards = hand['cards']
            player['hands'].pop(hand['idx'])
            for card in cards:
                new_hand(player['hands'])
                deal_card(shoe, player['hands'][-1], 1, card)
                deal_card(shoe, hand, 1)
        if action == 'exit':
            exit()


def check_bj(hand):
    if hand['total'] == 21:
        hand['bj'] = True
    return True


def check_split_double(hand):
    if len(hand['cards']) == 2:
        if hand['cards'][0][1] == hand['cards'][1][1]:
            hand['can_split'] = True
        hand['can_double'] = True
    return True


def get_actions(hand):
    actions = ['hit', 'stand']
    if len(hand['cards']) == 2:
        if hand['can_split']:
            actions.append('split')
        if hand['can_double']:
            actions.append('double')
        hand['can_double'] = True
    else:
        hand['bj'] = False
        hand['can_split'] = False
        hand['can_double'] = False
    return actions


def show_hand(hand):
    for card in hand['cards']:
        print(card[0], end=" ")
    print(f"({hand['total']}", end="")
    if hand['num_soft_ace'] and not hand['bj']:
        print(' soft', end="")
    print(')')
    return True
