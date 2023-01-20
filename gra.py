from klasy import Player, Turn
from cpu import CPU
import os
from time import sleep


class Game:
    def add_name(self):
        """

        Asks user for his/her nickname.

        """
        player_name = input("What's your gamertag? ")
        if player_name == '':
            print('Please choose your gamertag.')
            self.add_name()
        else:
            return player_name

    def add_bots(self):
        """

        Asks user for the number of CPU oponents.

        """
        bots_number = input("How many oponents do you want to play? ")
        try:
            c = int(bots_number)
        except ValueError:
            print("Please enter an integer amount.")
            c = self.add_bots()
        return c

    def add_pot(self):
        """

        Asks user for every player's starting pot.


        """
        x = "Enter the starting pot amount. Min. 1000. Enter integer: "
        pot = input(x)
        try:
            p = int(pot)
        except ValueError:
            print("Please enter an integer amount.")
            p = self.add_pot()
        if p < 1000:
            print("Please enter a value bigger than 1000.")
            p = self.add_pot()
        return p

    def add_blind(self, pot):
        """


        Asks user for the blind amount.


        """
        blind = input(f"Enter blind value from 0 to {int(round(0.05*pot, 0))}. Enter integer:")
        try:
            b = int(blind)
        except ValueError:
            print("Please enter an integer amount.")
            b = self.add_blind(pot)
        if b < 0 or b > 0.05*pot:
            print("Amount too big or too small.")
            b = self.add_blind(pot)
        return b

    def play(self):
        """

        Prints interface for the game.
        If user continues playing, the function loops.

        """
        os.system('clear')
        print("WELCOME TO P.I.P.R CASINO!")
        print("You will be playing no limits texas hold'em.")
        # sleep(4)
        os.system('clear')
        name = self.add_name()
        player1 = Player(name)
        players = [player1]
        os.system('clear')
        bots = self.add_bots()
        for n in range(1, bots+1):
            cpu = CPU(f"CPU{n}")
            players.append(cpu)
        os.system('clear')
        entry = self.add_pot()
        for player in players:
            player.add_pot(entry)
        blind = self.add_blind(entry)
        continue_playing = True
        while continue_playing is True:
            for player in players:
                player.reset()
                if player.pot() <= 0:
                    players.remove(player)
                    print(f"{player.name()} has lost all money.")
                    sleep(2)
                else:
                    print(f"{player.name()}'s pot: {int(player.pot())}")
                    # sleep(2)
            if player1 not in players:
                print("You have lost!")
                continue_playing = False
            turn = Turn(player1, players, entry, blind)
            turn._winner = False
            turn.give_cards()
            turn.set_blind()
            turn.first_round()
            if turn.winner() is False:
                turn.second_round()
                if turn.winner() is False:
                    remaining = turn.third_round()
                    if turn.winner() is False:
                        turn.check_winner(remaining)
            next = input("Do you want to continue? If so, press 1. ")
            if next != '1':
                print('Goodbye')
                continue_playing = False
