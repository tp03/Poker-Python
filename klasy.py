import random
from card_comparison import cards_comparison, check_hand
from card_hierarchy import sign
from cpu import CPU
import os
from time import sleep
deck = [('2', 'hearts'), ('2', 'diamonds'), ('2', 'spades'), ('2', 'clubs'),
('3', 'hearts'), ('3', 'diamonds'), ('3', 'spades'), ('3', 'clubs'),
('4', 'hearts'), ('4', 'diamonds'), ('4', 'spades'), ('5', 'clubs'),
('5', 'hearts'), ('5', 'diamonds'), ('5', 'spades'), ('5', 'clubs'),
('6', 'hearts'), ('6', 'diamonds'), ('6', 'spades'), ('6', 'clubs'),
('7', 'hearts'), ('7', 'diamonds'), ('7', 'spades'), ('7', 'clubs'),
('8', 'hearts'), ('8', 'diamonds'), ('8', 'spades'), ('8', 'clubs'),
('9', 'hearts'), ('9', 'diamonds'), ('9', 'spades'), ('9', 'clubs'),
('10', 'hearts'), ('10', 'diamonds'), ('10', 'spades'), ('10', 'clubs'),
('jack', 'hearts'), ('jack', 'diamonds'), ('jack', 'spades'), ('jack', 'clubs'),
('queen', 'hearts'), ('queen', 'diamonds'), ('queen', 'spades'), ('queen', 'clubs'),
('king', 'hearts'), ('king', 'diamonds'), ('king', 'spades'), ('king', 'clubs'),
('ace', 'hearts'), ('ace', 'diamonds'), ('ace', 'spades'), ('ace', 'clubs')]


class EmptyNameError(Exception):
    pass


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

    def give_cards(self):
        dealer = self.dealer()
        dealer.reset_deck()
        dealer.shuffle()
        for player in self.players():
            player.add_hand(dealer)
        self.table().add_cards(dealer)

    def player_raise_pot(self, player, raise_amount):
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
        player.set_fold(True)
        self._how_many_folded += -1
        print(f"{player.name()} folds.")

    def set_blind(self):
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

    def round(self, number):
        while self.winner() is False:
            players = self.players()
            os.system('clear')
            print(f"ROUND {number}")
            sleep(2)
            if number == 1:
                self.table().show_three()
            if number == 2:
                self.table().show_four()
            if number == 3:
                self.table().show_five()
            if self.gamer() in players:
                print('YOUR TURN')
                sleep(2)
                print(f'Current call: {self.current_call()}')
                print('Your hand is:')
                print(self.gamer().hand())
                self.player_moves(self.gamer(), number)
                if self.how_many_folded() == 0:
                    new_players = [player for player in players]
                    players1 = []
                    for player in new_players:
                        if player.fold() is False:
                            players1.append(player)
                    self.has_won()
                    return
                if self.how_many_folded()+1 == self.how_many_called():
                    new_players = [player for player in players]
                    players1 = []
                    for player in new_players:
                        if player.fold() is False:
                            players1.append(player)
                    self.set_players(players1)
                    self.set_current_call(0)
                    self._how_many_called = 0
                    for player in self.players():
                        player.reset_call()
                    return
            for player in players:
                if isinstance(player, CPU):
                    print(f'{player.name()} TURN')
                    sleep(3)
                    if number == 1:
                        player.check_hand_round1(self)
                        sleep(4)
                        if self.how_many_folded() == 0:
                            new_players = [player for player in players]
                            players1 = []
                            for player in new_players:
                                if player.fold() is False:
                                    players1.append(player)
                            self.set_players(players1)
                            self.has_won()
                            return
                        if self.how_many_folded()+1 == self.how_many_called():
                            new_players = [player for player in players]
                            players1 = []
                            for player in new_players:
                                if player.fold() is False:
                                    players1.append(player)
                            self.set_players(players1)
                            self.set_current_call(0)
                            self._how_many_called = 0
                            for player in players:
                                player.reset_call()
                            return
                    elif number == 2:
                        player.check_hand_round2(self)
                        sleep(4)
                        if self.how_many_folded() == 0:
                            new_players = [player for player in players]
                            players1 = []
                            for player in new_players:
                                if player.fold() is False:
                                    players1.append(player)
                            self.set_players(players1)
                            self.has_won()
                            return
                        if self.how_many_folded()+1 == self.how_many_called():
                            new_players = [player for player in players]
                            players1 = []
                            for player in new_players:
                                if player.fold() is False:
                                    players1.append(player)
                            self.set_players(players1)
                            self.set_current_call(0)
                            self._how_many_called = 0
                            for player in players:
                                player.reset_call()
                            return
                    else:
                        player.check_hand_round3(self)
                        sleep(4)
                        if self.how_many_folded() == 0:
                            new_players = [player for player in players]
                            players1 = []
                            for player in new_players:
                                if player.fold() is False:
                                    players1.append(player)
                            self.set_players(players1)
                            self.has_won()
                            return
                        if self.how_many_folded()+1 == self.how_many_called():
                            new_players = [player for player in players]
                            players1 = []
                            for player in new_players:
                                if player.fold() is False:
                                    players1.append(player)
                            self.set_players(players1)
                            self.set_current_call(0)
                            self._how_many_called = 0
                            for player in players:
                                player.reset_call()
                            return
            new_players = [player for player in players]
            players1 = []
            for player in new_players:
                if player.fold() is False:
                    players1.append(player)
            self.set_players(players1)

    def has_won(self):
        if self.winner() is True:
            return
        winner = self.players()[0]
        os.system('clear')
        print(f'{winner.name()} has won {self.pot()}')
        winner.add_pot(self.pot())
        self._winner = True
        return

    def player_moves(self, player, round):
        move = input('What is your move? 0 - check, 1 - raise, 2 - fold, 3 - all-in: ')
        if move == '0':
            if self.current_call() > player.pot():
                print("You don't have enough money to check.")
                self.player_moves(player)
            elif self.current_call() == player.pot():
                self.set_all_in_caller(self.gamer())
                self.all_in()
            else:
                self.player_check(player)
        elif move == '1':
            amount = input(f'How much do you raise? Your pot is {player.pot()}: ')
            if int(amount) > player.pot():
                print("You don't have that much money.")
                self.player_moves(player)
            elif int(amount) == player.pot():
                self.set_all_in_caller(player)
                self.all_in()
            else:
                self.player_raise_pot(player, int(amount))
        elif move == '2':
            self.player_fold(player)
        elif move == '3':
            if self.current_call() > player.pot():
                print("You don't have enough money to go all-in.")
                self.player_moves(player)
            else:
                self.set_all_in_caller(player)
                self.all_in(round)
        else:
            print('PLEASE ONLY USE 0, 1, 2 OR 3.')
            self.player_moves(player, round)

    def first_round(self):
        os.system('clear')
        print("ROUND 1")
        self.table().show_three()
        print('Your hand is:')
        print(self.gamer().hand())
        print('YOUR TURN')
        if self.gamer().is_blind() is True:
            print("You will raise blind.")
            self.player_raise_pot(self.gamer(), self.blind())
            sleep(10)
        else:
            self.player_moves(self.gamer(), 1)
        for player in self.players():
            if self.winner() is False:
                if isinstance(player, CPU):
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
        new_players = []
        for player in self.players():
            if player.fold() is False:
                new_players.append(player)
        self.set_players(new_players)
        if len(self.players()) == 1:
            self.has_won()
        if len(self.players()) == self.how_many_called():
            self.set_current_call(0)
            self._how_many_called = 0
            for player in new_players:
                player.reset_call()
            return
        self.round(1)
        return

    def second_round(self):
        self.round(2)
        return

    def third_round(self):
        self.round(3)
        return self.players()

    def all_in(self, round):
        new_players = []
        for player in self.players():
            if player.fold() is False:
                new_players.append(player)
        self.set_players(new_players)
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
            print(self.gamer().hand())
            move = input(f'Do you check? Your pot is {self.gamer().pot()}. If so, press "1": ')
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
                    for card in player.hand():
                        player.add_card(card)
                    if round == 1:
                        player.add_card(self.table().cards()[0])
                        player.add_card(self.table().cards()[1])
                        player.add_card(self.table().cards()[2])
                    elif round == 2:
                        player.add_card(self.table().cards()[0])
                        player.add_card(self.table().cards()[1])
                        player.add_card(self.table().cards()[2])
                        player.add_card(self.table().cards()[3])
                    else:
                        player.add_card(self.table().cards()[0])
                        player.add_card(self.table().cards()[1])
                        player.add_card(self.table().cards()[2])
                        player.add_card(self.table().cards()[3])
                        player.add_card(self.table().cards()[4])
                    check_hand(player)
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
        new_players = []
        for player in self.players():
            if player.fold() is False:
                new_players.append(player)
        self.set_players(new_players)
        if len(self.players()) == 1:
            self.has_won()
        self.table().show_five()
        for player in self.players():
            print(f"{player.name()}'s cards:")
            print(player.hand())
        if self.winner() is False:
            self.check_winner(self.players())

    def check_winner(self, remaining_players):
        winners = cards_comparison(remaining_players, self.table())
        if len(winners) == 1:
            os.system('clear')
            print(f'{winners[0].name()} has won!')
            sleep(3)
            print("Table:")
            self.table().show_five()
            sleep(1)
            print(f"{winners[0].name()}'s hand:")
            print(winners[0].hand()[0])
            print(winners[0].hand()[1])
            print(winners[0].hand_str())
            sleep(3)
            print(f'The prize is {self.pot()}.')
            winners[0].add_pot(self.pot())
            self._winner = True
        else:
            os.system('clear')
            print("It's a draw!")
            sleep(1)
            prize = round(self.pot()/len(winners), 0)
            print(f"The prize is {prize}.")
            print("Table:")
            self.table().show_five()
            sleep(3)
            print("Winners:")
            for player in winners:
                print(player.name())
                print(f"{player.name()}'s hand:")
                print(player.hand()[0])
                print(player.hand()[1])
                print(player.hand_str())
                sleep(3)
                player.add_pot(prize)
            self._winners = True


class Player:
    def __init__(self, name):
        if not name:
            raise EmptyNameError
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

    def reset(self):
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
        for card in deck:
            self._game_deck.append(card)

    def remove_from_deck(self, card):
        self.game_deck().remove(card)

    def reset_deck(self):
        self._game_deck = []
        self.set_game_deck()

    def shuffle(self):
        random.shuffle(self.game_deck())

    def get_two(self):
        my_deck = self.game_deck()
        card1 = random.choice(my_deck)
        self.remove_from_deck(card1)
        card2 = random.choice(my_deck)
        self.remove_from_deck(card2)
        return card1, card2

    def get_five(self):
        my_deck = self.game_deck()
        card1 = random.choice(my_deck)
        self.remove_from_deck(card1)
        card2 = random.choice(my_deck)
        self.remove_from_deck(card2)
        card3 = random.choice(my_deck)
        self.remove_from_deck(card3)
        card4 = random.choice(my_deck)
        self.remove_from_deck(card4)
        card5 = random.choice(my_deck)
        self.remove_from_deck(card5)
        return card1, card2, card3, card4, card5


class Table:
    def __init__(self):
        self._cards = []

    def cards(self):
        return self._cards

    def add_cards(self, dealer):
        table = dealer.get_five()
        for card in table:
            self.cards().append(card)

    def clear_table(self):
        for card in self.cards():
            self.cards().remove(card)

    def show_three(self):
        print(f'{self.cards()[0]}')
        print(f'{self.cards()[1]}')
        print(f'{self.cards()[2]}')
        print('hidden')
        print('hidden')

    def show_four(self):
        print(f'{self.cards()[0]}')
        print(f'{self.cards()[1]}')
        print(f'{self.cards()[2]}')
        print(f'{self.cards()[3]}')
        print('hidden')

    def show_five(self):
        print(f'{self.cards()[0]}')
        print(f'{self.cards()[1]}')
        print(f'{self.cards()[2]}')
        print(f'{self.cards()[3]}')
        print(f'{self.cards()[4]}')
