from player import Dealer, Player
from cards import Shoe


class Table:
    def __init__(self):
        self.dealer = Dealer()
        self.ruleset = {
            'Num Decks': 4,
            'Penetration': .65,
            'Min Bet': 2,
            'BJ Payout': 1.5,
            'Max Spots': 4,
            'Insurance': False,
            'Surrender': False,
            'Double': True,
            'Split': True,
            'Max Split': 4,
            'on 17': 'Hit'
        }
        self.shoe = Shoe(self.ruleset['Num Decks'],
                         self.ruleset['Penetration'])
        self.spots = []
        self.add_spots()
        self.round = 1

    def add_spots(self):
        num_players = int(
            input(f"How many players (max: {self.ruleset['Max Spots']})? "))
        spots_taken = num_players
        for p in range(num_players):
            print(f"Spot {p}:")
            start_chips = int(input('How many chips do you want? '))
            num_hands = int(input(
                f"how many hands for Spot {p} (max: {self.ruleset['Max Spots'] - spots_taken - 1})? "))  # TODO MAX SPOTS INCORRECT
            spots_taken += num_hands
            self.add_player(Player(start_chips, p, num_hands))
        return True

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
                f"Spot {x+1}: What is your bet(min-{self.ruleset['Min Bet']} max-{player.chips})? "))
            player['hands'][0].wager = wager
        return True

    def initial_deal(self):
        for i in range(2):
            for spot in self.spots:
                for hand in spot.hands:
                    hand.get_card(self.shoe.deal_card())
                    hand.check_bj()
            self.dealer.hands[0].get_card(self.shoe.deal_card())
            self.dealer.hands[0].check_bj()

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

        print(self.dealer.show_up_card())

        for spot in self.spots:
            print(f"Spot {spot.index} ", end='')
            for hand in spot.hands:
                hand.show()

    def show_curr(self):
        return

    def play(self):
        # TODO
        # Get Wagers and Deal Cards
        self.start_round()
        # Players Turns
        for spot in self.spots:
            while spot.is_playing:
                spot.play(self.dealer, self.shoe)
        # Dealer Plays
        self.dealer.play(self.spots, self.shoe)
        self.resolve()
        return

    def resolve(self):
        print('\nROUND RESULTS:')
        dealer_hand = self.dealer.hands[0]
        # DEALER HAS BLACKJACK
        if dealer_hand.result == 'blackjack':
            for spot in self.spots:
                for hand in spot.hands:
                    if hand.result != 'blackjack':
                        spot.chips -= hand.wager
                        hand.result = 'loss'
                    else:
                        hand.result = 'push'
                spot.show_final()

        # NO DEALER BLACKJACK
        else:
            for spot in self.spots:
                for hand in spot.hands:
                    if hand.result == 'blackjack':
                        spot.chips += int(hand['bet']
                                          * self.ruleset['BJ Payout'])
                    if hand.result == 'bust':
                        spot.chips -= hand.wager
                        hand.result = 'loss'
                    elif dealer_hand.result == 'bust':
                        spot.chips += hand.wager
                        hand.result = 'win'
                    elif dealer_hand.total > hand.total:
                        spot.chips -= hand.wager
                        hand.result = 'loss'
                    elif dealer_hand.total < hand.total:
                        spot.chips += hand.wager
                        hand.result = 'win'
                    else:
                        hand.result = 'push'
                spot.show_final()  # TODO INCORRECT CHIP COUNT WITH NUM_HANDS > 1
        return

    def results_to_file(self):
        with open('results.txt', 'a', encoding='UTF-8') as f:
            f.write(f"\n***ROUND {self.round} ***\n")
            for player in self.spots:
                f.write(player.get_final())
            f.write(self.dealer.get_final())
            f.write("\n*** END ROUND ***\n")
        return

    def __str__(self):
        snapshot = [spot.hands[0].cards for spot in self.spots]
        snapshot.append(self.dealer.hands[0].cards)
        return f"{snapshot}"
