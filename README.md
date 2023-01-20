### Poker Texas Hold'em single player.

A python script for a poker game with texas hold'em rules.


### Why should you check this code.

If you think you are a good poker player, check this projects to
see if you are correct.


### Base of the project.

This app is run through the terminal. It communicates with user
through imputs. Rules of the game are inline with those of a competetive
texas hold'em game in Las Vegas, Nevada. User can setup key information
about the game, such as number of players, entry pot amount and blind system.
You will be playing against a computer oponent, whose moves are chosen by an
algorythm. Go ahead, run this code and give it a shot!


### CPU algorythm


The CPU counts probability using current cards on the table and the rest of cards on deck to determine
probabilities for each combination using 'get_propability' function. It returns a dictionary of: a 'good hand', where a  good hand - double pair or better, a pair and 'nothing' - a single card. The values in this dictionary are probability of previously mentioned combinations. In round 1 the code firstly checks if CPU has a small ammount of money. If so, the computer can go all-in, if the propability of getting a good hand
is over 0.8. Else, the CPU will fold. In both round 1 and 2, if the current call is 0, the CPU will either check, or raise, if it has a good probability of getting a good hand. When the CPU has to check the raise, the move is decided by the probability to get a good hand and 'pot odds' - it calculates which procent of the pot will be the money the CPU raised. Based on the difference between 'pot odds' and 'good hand propability' the CPU decides it next move. If the computer doesn't check any of those conditions, it will fold. In round 3, when the CPU knows all shown cards, it decides its moves by the strength of its hand.


### Card comparison


To calculate who has the highest hand, the card_comparison function firstly adds hand to every
remaining player in the game. Then, it uses the dictionary in the 'card_database.json' file, where
every hand has a number value written to it. The player with the highest hand value wins. In case of the draw, the 'kicker' can decide the winner.

### Setup

You need 'python3' or higher to run this script.


### How to run the app.

You can run the script by typing:

'python3 -m main'

into the command terminal.


### Thanks for checking my app!

Hopefully you will have a great time.
If you have a question send me an email.
My email: zalewski.tomek03@gmail.com