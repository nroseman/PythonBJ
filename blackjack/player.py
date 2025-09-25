class Person:
    def __init__(self):
        self.hands = []
        self.add_hand()
        self.is_playing = True

    def add_hand(self):
        hand = Hand()
        self.hands.append(hand)

    def discard(self):
        self.hands.clear()
        return True

    def show_hands(self):
        for hand in self.hands:
            print(hand)

    def play(self):
        while self.curr_hand < len(self.hands):
            self.show_hands()

            self.curr_hand += 1
        return

    def __getitem__(self, key):
        return getattr(self, key)


class Dealer(Person):
    def __init__(self):
        super().__init__()

    def set_up_card(self):
        self.up_card = self.hands[0].cards[0]

    def show_up_card(self):
        print(f"Dealer shows: {self.up_card}")


class Player(Person):
    def __init__(self, chips, index, num_hands=1):
        super().__init__()
        self.index = index
        self.chips = chips
        self.curr_hand = 0


class Hand:
    def __init__(self, index=0):
        self.index = index
        self.cards = []
        self.total = 0
        self.result = ''
        self.wager = 0

    def get_card(self, card):
        self.cards.extend(card)
        self.total += card.value

    def __str__(self):
        return f"Hand {self.index} {*[cards for cards in self.cards],} total: {self.total}"
