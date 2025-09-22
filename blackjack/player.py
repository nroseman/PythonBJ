class Player:
    def __init__(self, chips, num_hands=1, is_dealer=False):
        self.chips = chips
        self.is_dealer = False
        self.hands = []
        self.add_hand()

    def add_hand(self):
        hand = Hand()
        self.hands.append(hand)

    def discard(self):
        self.hands.clear()
        return True


class Hand:
    def __init__(self):
        self.cards = []
        self.total = 0
        self.result = ''

    def get_card(self, card):
        self.cards.extend(card)
        self.total += card.value
