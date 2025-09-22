import random


class Card:
    def __init__(self, rank, suit, value):
        self.rank = str(rank)
        self.suit = suit
        self.face = self.rank + self.suit
        self.value = value
        self.is_ace = False
        self.is_soft = False
        if self.rank == 'A':
            self.is_ace = True
            self.is_soft = True

    def __str__(self):
        return self.face

    def __repr__(self):
        return self.face

    def __iter__(self):
        yield self


class Deck:
    def __init__(self):
        self.deck = []
        self.suits = ('H', 'D', 'C', 'S')
        self.rank = {1: ('A', 11), 11: ('J', 10), 12: ('Q', 10), 13: ('K', 10)}

        self.make_deck()

    def make_deck(self):
        self.deck = [Card(self.rank[r][0], suit, self.rank[r][1]) if r in self.rank else
                     Card(r, suit, r) for suit in self.suits for r in range(1, 14)]

    def __repr__(self):
        return self.deck

    def __str__(self):
        cards = ''
        for card in self.deck:
            cards += card.face
        return cards


class Shoe:
    def __init__(self, decks, penetration):
        self.cards = []
        self.discard = []
        self.num_decks = decks
        self.penetration = penetration

        self.make_shoe()

    def make_shoe(self):
        deck = Deck()
        self.cards = deck.deck * self.num_decks
        random.shuffle(self.cards)

    def deal_card(self):
        card = self.cards[0]
        self.cards.pop(0)
        self.discard.append(card)
        return card

    def __repr__(self):
        return self.cards

    def __len__(self):
        return len(self.cards)
