class Person:
    def __init__(self):
        self.hands = []
        self.is_playing = True
        self.next_action = []
        self.curr_hand = 0

    def add_hand(self, idx=-1):
        hand = Hand()
        self.hands.insert(idx, hand)
        # Set Correct Index
        for x, hand in enumerate(self.hands):
            hand.index = x

    def discard(self):
        self.hands.clear()
        return True

    def show_hands(self):
        for hand in self.hands:
            print(hand)

    def __getitem__(self, key):
        return getattr(self, key)


class Dealer(Person):
    def __init__(self):
        super().__init__()
        # TODO DOES THIS NEED TO BE A LIST FOR DEALER?
        self.add_hand()

    def set_up_card(self):
        self.up_card = self.hands[0].cards[0]

    def show_up_card(self):
        return f"Dealer shows: {self.up_card}"

    def play(self, players, shoe):
        self.is_playing = self.check_playing(players)
        while self.is_playing:
            self.next_action = self.get_actions()
            self.resolve_action(shoe)
            self.update()
        self.show_final()

    def check_playing(self, players):  # If All Players Bust, No Play
        for player in players:
            for hand in player.hands:
                if hand.result != 'bust':
                    return True
        self.hands[self.curr_hand].result = 'stand'
        return False

    def get_actions(self):
        curr_hand = self.hands[self.curr_hand]
        if curr_hand.num_soft_aces > 0:
            min_score = 18
        else:
            min_score = 17
        if curr_hand.total < min_score:
            return 'hit'
        else:
            return 'stand'

    def resolve_action(self, shoe):
        curr_hand = self.hands[self.curr_hand]
        if self.next_action == 'hit':
            curr_hand.get_card(shoe.deal_card())
        if self.next_action == 'stand':
            curr_hand.is_done = True
            if curr_hand.result != 'blackjack':
                curr_hand.result = 'stand'

    def update(self):
        curr_hand = self.hands[self.curr_hand]
        if curr_hand.total > 21:
            curr_hand.result = 'bust'
            self.is_playing = False
        if curr_hand.is_done:
            self.is_playing = False

    def show_final(self):
        curr_hand = self.hands[self.curr_hand]
        print(f"Dealer {curr_hand.result}")
        curr_hand.show()

    def get_final(self):
        curr_hand = self.hands[self.curr_hand]
        return f"Dealer {*[cards for cards in curr_hand.cards],}"


class Player(Person):  # TODO Need to accept different num_hands
    def __init__(self, chips, index, num_hands=1):
        super().__init__()
        self.index = index
        self.chips = chips
        for hands in range(num_hands):
            self.add_hand()

    def play(self, dealer, shoe):
        print(f"\nSpot {self.index}\n")
        while self.curr_hand < len(self.hands):
            # Show table condition
            self.show_curr(dealer)
            # Get Next Action
            self.get_action()
            # Resolve Action
            self.resolve_action(shoe)
            # Continue or Next
            self.update()
        self.is_playing = False
        return None

    def get_action(self):
        # GET PLAYER OPTIONS
        options = []
        curr_hand = self.hands[self.curr_hand]
        if curr_hand.total <= 21:
            options.append('stand')
        if curr_hand.total < 21:
            options.append('hit')
        if curr_hand.can_double:
            options.append('double')
        if curr_hand.can_split:
            options.append('split')
        # PLAYER MAKE CHOICE
        self.get_player_choice(options)
        return

    def get_player_choice(self, options):
        try:
            action = input(f"What would you like to do {*options,}? ").lower()
        except:
            print('invalid input. try again')
            self.get_player_choice(options)
        else:
            if action == 'exit':
                exit()
            if action not in options:
                print('invalid selection. try again.')
                self.get_player_choice(options)
            else:
                self.next_action = action
        return None

    def resolve_action(self, shoe):
        curr_hand = self.hands[self.curr_hand]
        if self.next_action == 'stand':
            curr_hand.is_done = True
        if self.next_action == 'hit':
            curr_hand.get_card(shoe.deal_card())
        if self.next_action == 'double':
            curr_hand.wager *= 2
            curr_hand.get_card(shoe.deal_card())
            curr_hand.show()
            curr_hand.is_done = True
        if self.next_action == 'split':
            cards = curr_hand.cards
            self.hands.remove(curr_hand)
            for i in range(2):
                idx = self.curr_hand + i
                self.add_hand(idx)
                self.hands[idx].get_card(cards[idx])
                self.hands[idx].get_card(shoe.deal_card())
            print(f"All your hands:")
            self.show_hands()
        return None

    def update(self):
        curr_hand = self.hands[self.curr_hand]
        if curr_hand.total > 21:
            curr_hand.show()
            print('busto')
            curr_hand.result = 'bust'
            curr_hand.is_done = True
        if curr_hand.is_done:
            self.curr_hand += 1

    def show_curr(self, dealer):
        self.hands[self.curr_hand]
        dealer.show_up_card()
        print(f"Hand {self.curr_hand}:")
        self.hands[self.curr_hand].show()

    def show_final(self):
        print(f"Spot {self.index}:")
        for hand in self.hands:
            print(
                f"  Hand {hand.index} {*[card for card in hand.cards],} Result: {hand.result}")
        print(f"  final chip count: {self.chips}")

    def get_final(self):
        final = [f"Spot {self.index}:",]
        for hand in self.hands:
            final.append(f"  {hand.get_final()}")
        final.append(f"  chip count: {self.chips}\n")
        return '\n'.join(final)


class Hand:
    def __init__(self, index=0):
        self.index = index
        self.cards = []
        self.total = 0
        self.result = ''
        self.wager = 0
        self.num_soft_aces = 0
        self.can_double = False
        self.can_split = False
        self.is_done = False

    def get_card(self, card):
        self.cards.extend(card)
        self.check_double_split()
        if card.is_ace:
            self.num_soft_aces += 1
        self.total += card.value
        while self.num_soft_aces > 0 and self.total > 21:
            self.total -= 10
            self.num_soft_aces -= 1

    def check_bj(self):  # Only Call During Initial Deal
        if self.total == 21:
            self.result = 'blackjack'
            self.can_double = False  # No double on BJ
        return None

    def check_double_split(self):
        if len(self.cards) == 2:
            self.can_double = True
            if self.cards[0].value == self.cards[1].value:
                self.can_split = True
        else:
            self.can_double = False
            self.can_split = False

    def show(self):
        for card in self.cards:
            print(card.face, end=" ")
        print(f"({self.total}", end="")
        if self.num_soft_aces and self.total != 21:
            print(' soft', end="")
        if self.result == 'blackjack':
            print(' blackjack!', end="")
        print(')')
        return True

    def get_final(self):
        return f"Hand {self.index} {*[cards for cards in self.cards],} total: {self.total} Result: {self.result}"

    def __str__(self):
        return f"Hand {self.index} {*[cards for cards in self.cards],} total: {self.total}"
