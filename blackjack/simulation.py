# NO PLAYER DECISIONS - BASED ON PREDETERMINED STRATEGY
from table import Table

# Setup Table -> players, dealer, ruleset
table = Table()
# Let Players Bet
table.set_wagers()
# Deal two cards to each spot/hand
table.initial_deal()
table.show()
# Each Player Plays Hand(s)
table.play()
