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
    spots = [{'index': i, 'chips': CHIPS, 'hands': [{'idx': 0, 'cards': [], 'total': 0, 'num_soft_ace': 0, 'bj': False, 'result': ''}]}
             for i in range(NUM_PLAYERS + 1)]
    return spots


def new_hand(hands):
    index = len(hands)
    hands.append({'idx': index, 'cards': [], 'total': 0,
                 'num_soft_ace': 0, 'bj': False, 'result': ''})
    return True


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


def reset(spot):
    spot['hands'].clear()
    spot['hands'] = [{'idx': 0, 'cards': [], 'total': 0,
                      'num_soft_ace': 0, 'bj': False, 'result': ''}]
    return spot


def update_hand(hand):
    # UPDATE TOTAL
    hand['total'] += hand['cards'][-1][1]
    # CHECK SOFT ACES
    while hand['num_soft_ace'] and hand['total'] > 21:
        hand['total'] -= 10
        hand['num_soft_ace'] -= 1
    return True

# Outdated
# def play(hand, action):
#     # DEALER
#     if not player:
#         while not hand['bust']:
#             if hand['num_soft_ace'] > 0:
#                 min_score = 18
#             else:
#                 min_score = 17
#             if hand['total'] < min_score:
#                 deal_card(shoe, hand, 1)
#             else:
#                 return True
#     # PLAYER
#     else:
#         player_current = player
#         hand_current = player['hands']
#         if action == 'hit':
#             deal_card(shoe, hand, 1)
#         if action == 'stand':
#             return 'end'
#         if action == 'double' and hand['can_double']:
#             deal_card(shoe, hand, 1)
#             hand['doubled'] = True
#             show_hand(hand)
#             return 'end'
#         if action == 'split' and hand['can_split']:
#             cards = hand['cards']
#             player['hands'].remove(hand)
#             for x in range(2):
#                 new_hand(player['hands'])
#                 deal_card(shoe, player['hands'][-1], 1, cards[x])
#                 deal_card(shoe, player['hands'][-1], 1)
#             print(player['hands'])
#         if action == 'exit':
#             exit()


def check_bj(hand):
    if len(hand['cards']) == 2:
        if hand['total'] == 21:
            return True
    return False


def get_actions(hand):
    actions = []

    if hand['total'] > 21:
        return 'bust'
    if hand['result'] == 'double':
        return 'stand'

    if hand['total'] < 21:
        actions.append('hit')
    if hand['total'] <= 21:
        actions.append('stand')

    if len(hand['cards']) == 2:
        if hand['cards'][0][1] == hand['cards'][1][1]:
            actions.append('split')
        actions.append('double')
        if check_bj(hand):
            return 'blackjack'

    # Get Player Choice
    show_hand(hand)
    option = input(f"What would you like to do {*actions,}? ")

    if option == 'exit':
        exit()
    elif option in actions:
        return option
    else:
        return 'invalid'


def resolve_action(hand, next_action, shoe):
    if next_action == 'bust':
        show_hand(hand)
        print('bust:(')
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
        hand['result'] = 'stand'
        return 'stand'
    if next_action == 'double':
        # TODO double wager
        deal_card(shoe, hand, 1)
        show_hand(hand)
        hand['result'] = 'double'
        return 'double'
    if next_action == 'split':
        # TODO add option
        return 'split'


def show_hand(hand):
    for card in hand['cards']:
        print(card[0], end=" ")
    print(f"({hand['total']}", end="")
    if hand['num_soft_ace']:
        print(' soft', end="")
    print(')')
    return True
