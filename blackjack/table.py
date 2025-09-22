from player import Player
from cards import Card, Deck, Shoe


class Table:
    def __init__(self):
        self.dealer = Player(0, is_dealer=True)
        self.ruleset = {
            'Num Decks': 4,
            'Penetration': .65,
            'Min Bet': 2,
            'BJ Payout': 1.5,
            'Max Spots': 1,
            'Insurance': True,
            'Surrender': True,
            'Double': True,
            'Split': True,
            'Max Split': 4,
            'on 17': 'Hit'
        }
        self.shoe = Shoe(self.ruleset['Num Decks'],
                         self.ruleset['Penetration'])
        self.spots = [Player(1000) for p in range(self.ruleset['Max Spots'])]

    def add_player(player):
        return

    def initial_deal(self):
        for i in range(2):
            for spot in self.spots:
                for hand in spot.hands:
                    hand.get_card(self.shoe.deal_card())
            self.dealer.hands[0].get_card(self.shoe.deal_card())

    def __str__(self):
        snapshot = [spot.hands[0].cards for spot in self.spots]
        snapshot.append(self.dealer.hands[0].cards)
        return f"{snapshot}"
