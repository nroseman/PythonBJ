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

    def show_hands(self):
        for hand in self.hands:
            print(hand)

    def __getitem__(self, key):
        return getattr(self, key)


class Hand:
    def __init__(self):
        self.cards = []
        self.total = 0
        self.result = ''
        self.wager = 0

    def get_card(self, card):
        self.cards.extend(card)
        self.total += card.value

    def __str__(self):
        return f"{self.cards} total: {self.total}"
