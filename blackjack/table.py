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

    def add_player(self, player):
        if len(self.spots) < self.ruleset['Max Spots']:
            self.spots.append(player)
            return True
        else:
            print('Table is already full. Unable to sit new player.')
            return False

    def set_wagers(self):
        for x, player in enumerate(self.spots):
            wager = int(input(
                f"Spot {x+1}: What is your bet(min-{self.ruleset['Min Bet']} max-{player['chips']})? "))
            player['hands'][0].wager = wager
        return True

    def initial_deal(self):
        for i in range(2):
            for spot in self.spots:
                for hand in spot.hands:
                    hand.get_card(self.shoe.deal_card())
            self.dealer.hands[0].get_card(self.shoe.deal_card())

    def show(self):
        print(f"Dealer shows: {self.dealer['hands'][0].cards[0]}")
        for x, spot in enumerate(self.spots):
            print(f"Spot {x+1} ", end='')
            for y, hand in enumerate(spot.hands):
                print(f"Hand {y+1}: {hand}")

    def play(self):
        # TODO

        return

    def __str__(self):
        snapshot = [spot.hands[0].cards for spot in self.spots]
        snapshot.append(self.dealer.hands[0].cards)
        return f"{snapshot}"
