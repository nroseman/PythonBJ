from player import Dealer, Player
from cards import Card, Deck, Shoe


class Table:
    def __init__(self):
        self.dealer = Dealer()
        self.ruleset = {
            'Num Decks': 4,
            'Penetration': .65,
            'Min Bet': 2,
            'BJ Payout': 1.5,
            'Max Spots': 2,
            'Insurance': True,
            'Surrender': True,
            'Double': True,
            'Split': True,
            'Max Split': 4,
            'on 17': 'Hit'
        }
        self.shoe = Shoe(self.ruleset['Num Decks'],
                         self.ruleset['Penetration'])
        self.spots = [Player(1000, p)
                      for p in range(self.ruleset['Max Spots'])]
        self.round = 1

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
        self.dealer.set_up_card()

    def start_round(self):
        self.show_round()
        # Let Players Bet
        self.set_wagers()
        # Deal two cards to each spot/hand
        self.initial_deal()
        self.show_all()

    def show_round(self):
        print(f"\n*** ROUND {self.round} BEGINS ***\n")

    def show_all(self):

        self.dealer.show_up_card()

        for x, spot in enumerate(self.spots):
            print(f"Spot {x+1} ", end='')
            for hand in spot.hands:
                print(hand)

    def show_curr(self):
        return

    def play(self):
        # TODO
        # Get Wagers and Deal Cards
        self.start_round()
        # Players Turns
        for spot in self.spots:
            while spot.is_playing:
                # Show table condition

                # Get Next Action
                # Resolve Action
                # Continue or Next
                spot.play()
                break
        return

    def __str__(self):
        snapshot = [spot.hands[0].cards for spot in self.spots]
        snapshot.append(self.dealer.hands[0].cards)
        return f"{snapshot}"
