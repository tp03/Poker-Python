import random
from card_comparison import Card
from cpu import CPU
import os
from time import sleep
from read_from_json_file import sign


class Turn:
    def __init__(self, gamer, players, entry, blind=0):
        self._gamer = gamer
        self._players = players
        self._pot = 0
        self._current_call = 0
        self._entry = entry
        self._table = Table()
        self._how_many_called = 0
        self._how_many_folded = len(self.players()) - 1
        self._all_in_caller = None
        self._blind = blind
        self._winner = False
        self._dealer = Dealer()

    def gamer(self):
        return self._gamer

    def players(self):
        return self._players

    def entry(self):
        return self._entry

    def set_players(self, new_list):
        self._players = new_list

    def winner(self):
        return self._winner

    def pot(self):
        return self._pot

    def blind(self):
        return self._blind

    def dealer(self):
        return self._dealer

    def how_many_called(self):
        return self._how_many_called

    def how_many_folded(self):
        return self._how_many_folded

    def remove_player(self, player):
        self._players.remove(player)

    def table(self):
        return self._table

    def all_in_caller(self):
        return self._all_in_caller

    def set_all_in_caller(self, caller):
        self._all_in_caller = caller

    def current_call(self):
        return self._current_call

    def set_current_call(self, new_call):
        self._current_call = new_call

    def check_folds(self):
        """

        Checks if any new player has folded
        and creates a new list of players, who are
        still playing.


        """
        new_players = [player for player in self.players()]
        players1 = []
        for player in new_players:
            if player.fold() is False:
                players1.append(player)
                self.set_players(players1)

    def give_cards(self):
        """


        Adds two card to every player in the game and
        adds five cards to the table.


        """
        dealer = self.dealer()
        dealer.reset_deck()
        dealer.shuffle()
        for player in self.players():
            player.add_hand(dealer)
        self.table().add_cards(dealer)

    def player_raise_pot(self, player, raise_amount):
        """


        Makes chosen player raise the current pot.
        The function adds money to turn's pot,
        takes money away from the player and sets calls.
        If the player has already put money to the pot in
        current round, the function will raise the remaining
        amount required to call.


        """
        if player.call() != 0:
            self._pot += (raise_amount-player.call())
            player.add_pot(-(raise_amount-player.call()))
            self.set_current_call(raise_amount)
            player.add_call(raise_amount-player.call())
            self._how_many_called = 1
            print(f"{player.name()} raises {raise_amount}.")
        else:
            player.add_pot(-raise_amount)
            self._pot += raise_amount
            self.set_current_call(raise_amount)
            player.add_call(raise_amount)
            self._how_many_called = 1
            print(f"{player.name()} raises {raise_amount}.")

    def player_check(self, player):
        """


        Makes chosen player check. Depending on
        current call, it can take monet away from the
        player and add it to turns pot.


        """
        if player.call() != 0:
            self._pot += (self.current_call()-player.call())
            player.add_pot(-(self.current_call()-player.call()))
            player.add_call(self.current_call()-player.call())
            self._how_many_called += 1
            print(f"{player.name()} checks.")
        else:
            player.add_pot(-self.current_call())
            player.add_call(self.current_call())
            self._pot += self.current_call()
            self._how_many_called += 1
            print(f"{player.name()} checks.")

    def player_fold(self, player):
        """


        Makes chosen player fold, by setting
        his/her fold bool to True.


        """
        player.set_fold(True)
        self._how_many_folded += -1
        print(f"{player.name()} folds.")

    def set_blind(self):
        """


        Sets the blind for the next round.
        The blind amount depends on player's
        input in the begining of the game.
        For the first round, the function
        sets blind for the player. In the following
        round, it will be shifted to the first cpu.



        """
        for index, player in enumerate(self.players()):
            if player.is_blind() is True:
                current_blind = index
                player.set_blind(False)
                try:
                    self.players()[current_blind+1].set_blind(True)
                    return
                except IndexError:
                    self.players()[0].set_blind(True)
                    return
        self.players()[0].set_blind(True)

    def check_if_checked(self):
        """


        Checks if everyone is a round has checked
        the current call.


        """
        if self.how_many_folded()+1 == self.how_many_called():
            self.check_folds()
            self.set_current_call(0)
            self._how_many_called = 0
            for player in self.players():
                player.reset_call()
            return True
        return False

    def check_if_folded(self):
        """


        Checks if there is only one
        player left in the current turn.


        """
        if self.how_many_folded() == 0:
            self.check_folds()
            self.has_won()
            return True
        return False

    def round(self, number):
        """


        Plays one round of texas hold'em.
        After each player's move, it checks if everyone
        playing has checked the current call, or if
        there is only one player remaining. Unless one
        of these critetias is met, the function
        will loop.


        """
        while self.winner() is False:
            os.system('clear')
            print("Cards on the table:")
            self.table().print_cards(number)
            if self.gamer() in self.players():
                print('YOUR TURN')
                sleep(2)
                print(f'Current call: {self.current_call()}')
                print('Your hand is:')
                self.gamer().print_cards()
                self.player_moves(self.gamer(), number)
                if self.check_if_folded() is True:
                    return
                if self.check_if_checked() is True:
                    return
            for player in self.players():
                if isinstance(player, CPU):
                    if self.winner() is False:
                        print(f'{player.name()} TURN')
                        sleep(3)
                        if number == 1:
                            player.check_hand_round1(self)
                        elif number == 2:
                            player.check_hand_round2(self)
                        else:
                            player.check_hand_round3(self)
                        sleep(4)
                        if self.check_if_folded() is True:
                            return
                        if self.check_if_checked() is True:
                            return
            self.check_folds()

    def has_won(self):
        """


        Is activated when there is only
        one player remaining. The function
        adds pot to the winner and prints
        information to the user.


        """
        if self.winner() is True:
            return
        winner = self.players()[0]
        os.system('clear')
        print(f'{winner.name()} has won {self.pot()}')
        winner.add_pot(self.pot())
        self._winner = True
        return

    def player_moves(self, player, round):
        """


        Allows player to make move in the game
        via simple number inputs. If the player cannot
        make such a move, the function calls itself
        again.

        """
        print(f"Your pot: {player.pot()}.")
        if self.current_call() > player.pot():
            print("You don't have enough money, you have to fold.")
            self.player_fold(player)
        x = 'What is your move? 0 - check, 1 - raise, 2 - fold, 3 - all-in: '
        move = input(x)
        if move == '0':
            if self.current_call() == player.pot():
                self.set_all_in_caller(self.gamer())
                self.all_in()
            else:
                self.player_check(player)
        elif move == '1':
            amount = input(f'How much do you raise? Your pot: {player.pot()} ')
            if int(amount) > player.pot():
                print("You don't have that much money.")
                self.player_moves(player, round)
            elif int(amount) == player.pot():
                self.set_all_in_caller(player)
                self.all_in()
            elif self.current_call() > int(amount):
                print("Current call is bigger than your raise.")
                self.player_moves(player, round)
            elif self.current_call() == int(amount):
                self.player_check(player)
            else:
                self.player_raise_pot(player, int(amount))
        elif move == '2':
            self.player_fold(player)
        elif move == '3':
            self.set_all_in_caller(self.gamer())
            self.all_in(round)
        else:
            print('PLEASE ONLY USE 0, 1, 2 OR 3.')
            self.player_moves(player, round)

    def first_round(self):
        """


        Plays the first found of texas hold'em.
        Differs from round function by implementing
        blinds.


        """
        os.system('clear')
        print("Round 1 - three cards will be shown.")
        sleep(5)
        print("Cards on the table:")
        self.table().print_cards(1)
        print('Your hand is:')
        self.gamer().print_cards()
        print('YOUR TURN')
        if self.gamer().is_blind() is True:
            print("You will raise blind.")
            self.player_raise_pot(self.gamer(), self.blind())
            sleep(10)
        else:
            self.player_moves(self.gamer(), 1)
        for player in self.players():
            if isinstance(player, CPU):
                if self.winner() is False:
                    print(f'{player.name()} TURN')
                    if player.is_blind() is True:
                        if self.blind() > self.current_call():
                            print(f'{player.name()} raises blind.')
                            self.player_raise_pot(player, self.blind())
                            sleep(4)
                        elif self.blind() == self.current_call():
                            self.player_check(player)
                        else:
                            x = random.randint(1, 4)
                            if x == 1:
                                self.player_fold(player)
                                sleep(4)
                            else:
                                self.player_check(player)
                                sleep(4)
                    else:
                        player.check_hand_round1(self)
                        sleep(4)
        if self.winner() is True:
            return
        self.check_folds()
        if len(self.players()) == 1:
            self.has_won()
        if len(self.players()) == self.how_many_called():
            self.set_current_call(0)
            self._how_many_called = 0
            for player in self.players():
                player.reset_call()
            return
        self.round(1)
        return

    def second_round(self):
        """


        Activates the second round of the game,
        with four cards shown on the table.


        """
        os.system('clear')
        print("Everyone has checked, round 2 - fourth card will be shown.")
        sleep(5)
        self.round(2)
        return

    def third_round(self):
        """


        Activates the third round of the game,
        with five cards shown on the table.


        """
        os.system('clear')
        print("Everyone has checked, round 3 - fifth card will be shown.")
        sleep(5)
        self.round(3)
        return self.players()

    def all_in(self, round):
        """

        Plays the all in scenario. Ask every
        player if they want to check the all-in.
        If no one does, the function ends round.


        """
        self.check_folds()
        caller = self.all_in_caller()
        raise_amount = caller.pot()
        caller.add_pot(-raise_amount)
        self._pot += raise_amount
        self.set_current_call(raise_amount)
        caller.add_call(raise_amount)
        self._how_many_called = 1
        os.system('clear')
        print(f'{caller.name()} has called all-in.')
        print(f'Current call is {self.current_call()}')
        sleep(3)
        if self.gamer() in self.players() and self.gamer() is not caller:
            print('Your hand is: ')
            self.gamer().print_cards()
            move = input(f'Your pot: {self.gamer().pot()}. Check - "1": ')
            if move == 1:
                if self.current_call() > self.gamer().pot():
                    print("You don't have enough money. You must fold.")
                    sleep(2)
                    self.player_fold(self.gamer())
                else:
                    self.player_check(self.gamer())
            else:
                self.player_fold()
                sleep(2)
        for player in self.players():
            os.system('clear')
            if isinstance(player, CPU):
                if player is not caller:
                    player.reset_end_hand()
                    player.reset_kicker()
                    for card in player.hand():
                        player.add_card(card)
                    if round == 1:
                        for i in range(0, 3):
                            player.add_card(self.table().cards()[i])
                    elif round == 2:
                        for i in range(0, 4):
                            player.add_card(self.table().cards()[i])
                    else:
                        for i in range(0, 5):
                            player.add_card(self.table().cards()[i])
                    cards_class = Card()
                    cards_class.check_hand(player)
                    if sign[player.hand_str()] > 129:
                        if player.pot() > self.current_call():
                            self.player_check(player)
                            sleep(4)
                        else:
                            self.player_fold(player)
                            sleep(4)
                    else:
                        self.player_fold(player)
                        sleep(4)
        self.check_folds()
        if len(self.players()) == 1:
            self.has_won()
        self.table().print_cards(3)
        for player in self.players():
            print(f"{player.name()}'s cards:")
            player.print_cards()
        if self.winner() is False:
            self.check_winner(self.players())

    def check_winner(self, remaining_players):
        """


        Is called when there is more than one
        player left after round 3. Determines
        the winner or winners by the card comparison
        system.


        """
        cards_class = Card()
        winners = cards_class.cards_comparison(remaining_players, self.table())
        if len(winners) == 1:
            os.system('clear')
            print(f'{winners[0].name()} has won!')
            sleep(3)
            print("Table:")
            self.table().print_cards(3)
            sleep(1)
            print(f"{winners[0].name()}'s hand:")
            winners[0].print_cards()
            print(winners[0].hand_str())
            sleep(3)
            print(f'The prize is {int(self.pot())}.')
            winners[0].add_pot(int(self.pot()))
            self._winner = True
        else:
            os.system('clear')
            print("It's a draw!")
            sleep(1)
            prize = int(round(self.pot()/len(winners), 0))
            print(f"The prize is {prize}.")
            print("Table:")
            self.table().print_cards(3)
            sleep(3)
            print("Winners:")
            for player in winners:
                print(player.name())
                print(f"{player.name()}'s hand:")
                player.print_cards()
                print(player.hand_str())
                sleep(3)
                player.add_pot(prize)
            self._winner = True


class Player:
    def __init__(self, name):
        self._name = name
        self._hand = []
        self._pot = 0
        self._call = 0
        self._is_blind = False
        self._folded = False
        self._end_hand = []
        self._hand_str = ''
        self._kicker_check = []
        self._kicker = ''

    def name(self):
        return self._name

    def pot(self):
        return self._pot

    def hand(self):
        return self._hand

    def call(self):
        return self._call

    def reset_call(self):
        self._call = 0

    def is_blind(self):
        return self._is_blind

    def kicker(self):
        return self._kicker

    def kicker_check(self):
        return self._kicker_check

    def hand_str(self):
        return self._hand_str

    def fold(self):
        return self._folded

    def set_fold(self, new_fold):
        self._folded = new_fold

    def add_call(self, new_call):
        self._call += new_call

    def add_pot(self, new_pot):
        self._pot += new_pot

    def end_hand(self):
        return self._end_hand

    def print_cards(self):
        """


        Prints players's cards.


        """
        for card in self.hand():
            card_str = ''
            if card[0] == 'ace':
                card_str += 'A'
            elif card[0] == 'king':
                card_str += 'K'
            elif card[0] == 'queen':
                card_str += 'Q'
            elif card[0] == 'jack':
                card_str += 'J'
            else:
                card_str += card[0]
            if card[1] == "clubs":
                card_str += '\u2663'
            elif card[1] == "diamonds":
                card_str += '\u2666'
            elif card[1] == "hearts":
                card_str += '\u2665'
            else:
                card_str += '\u2660'
            print(card_str)

    def reset(self):
        """


        Resets player's atributes to values
        from before the turn has started.


        """
        self.set_fold(False)
        self._hand = []
        self._hand_str = ''
        self._call = 0
        self.reset_kicker()
        self.reset_end_hand()

    def set_kicker(self, kicker):
        self._kicker = kicker

    def add_kicker_check(self, card):
        self._kicker_check.append(card)

    def add_card(self, card):
        self._end_hand.append(card)

    def remove_card(self, card):
        self._end_hand.remove(card)

    def reset_end_hand(self):
        self._end_hand = []

    def reset_kicker(self):
        self._kicker_check = []
        self._kicker = ''

    def add_hand_str(self, hand):
        self._hand_str = hand

    def add_hand(self, dealer):
        hand = dealer.get_two()
        for card in hand:
            self._hand.append(card)

    def set_blind(self, bool):
        self._is_blind = bool


class Dealer:
    def __init__(self):
        self._game_deck = []

    def game_deck(self):
        return self._game_deck

    def set_game_deck(self):
        """


        Generates a deck of cards to
        dealer's list.


        """
        for i in range(0, 4):
            if i == 0:
                colour = 'clubs'
            elif i == 1:
                colour = 'diamonds'
            elif i == 2:
                colour = 'hearts'
            else:
                colour = 'spades'
            for n in range(0, 13):
                if n == 0:
                    self._game_deck.append(('2', f'{colour}'))
                elif n == 1:
                    self._game_deck.append(('3', f'{colour}'))
                elif n == 2:
                    self._game_deck.append(('4', f'{colour}'))
                elif n == 3:
                    self._game_deck.append(('5', f'{colour}'))
                elif n == 4:
                    self._game_deck.append(('6', f'{colour}'))
                elif n == 5:
                    self._game_deck.append(('7', f'{colour}'))
                elif n == 6:
                    self._game_deck.append(('8', f'{colour}'))
                elif n == 7:
                    self._game_deck.append(('9', f'{colour}'))
                elif n == 8:
                    self._game_deck.append(('10', f'{colour}'))
                elif n == 9:
                    self._game_deck.append(('jack', f'{colour}'))
                elif n == 10:
                    self._game_deck.append(('queen', f'{colour}'))
                elif n == 11:
                    self._game_deck.append(('king', f'{colour}'))
                else:
                    self._game_deck.append(('ace', f'{colour}'))

    def remove_from_deck(self, card):
        self.game_deck().remove(card)

    def reset_deck(self):
        """


        Adds all cards back to the
        dealer.


        """
        self._game_deck = []
        self.set_game_deck()

    def shuffle(self):
        """


        Shuffles the deck.


        """
        random.shuffle(self.game_deck())

    def get_two(self):
        """


        Randomly draws two cards.


        """
        my_deck = self.game_deck()
        card1 = random.choice(my_deck)
        self.remove_from_deck(card1)
        card2 = random.choice(my_deck)
        self.remove_from_deck(card2)
        return card1, card2

    def get_five(self):
        """


        Randomly draws five cards.


        """
        my_deck = self.game_deck()
        cards = []
        for i in range(0, 5):
            card_i = random.choice(my_deck)
            self.remove_from_deck(card_i)
            cards.append(card_i)
        return cards


class Table:
    def __init__(self):
        self._cards = []

    def cards(self):
        return self._cards

    def add_cards(self, dealer):
        table = dealer.get_five()
        for card in table:
            self.cards().append(card)

    def print_cards(self, round):
        """


        Shows cards on the table, the number of
        them depends on the round.


        """
        if round == 1:
            n = 3
        elif round == 2:
            n = 4
        else:
            n = 5
        for card in self.cards()[0:n]:
            card_str = ''
            if card[0] == 'ace':
                card_str += 'A'
            elif card[0] == 'king':
                card_str += 'K'
            elif card[0] == 'queen':
                card_str += 'Q'
            elif card[0] == 'jack':
                card_str += 'J'
            else:
                card_str += card[0]
            if card[1] == "clubs":
                card_str += '\u2663'
            elif card[1] == "diamonds":
                card_str += '\u2666'
            elif card[1] == "hearts":
                card_str += '\u2665'
            else:
                card_str += '\u2660'
            print(card_str)
        for i in range(0, 5-n):
            print('HIDDEN')
