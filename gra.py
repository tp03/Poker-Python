from klasy import Player, Turn

print("WELCOME TO P.I.P.R POKER!")


def add_name():
    player_name = input("What's your gamertag? ")
    if player_name == '':
        print('Please choose your gamertag.')
        add_name()
    else:
        return player_name


name = add_name()
player1 = Player(name)
players = [player1]


# def add_bots():
#     bots_number = input("How many oponents do you want to play? ")
#     if int(bots_number) != bots_number:
#         print("Please enter an integer.")
#         add_bots()
#     return bots_number


# bots = add_bots()
# for n in range(1, bots+1):
#     cpu = CPU(f"CPU{n}")
#     players.append(cpu)


def add_pot():
    pot = input("What should be the starting pot amount? Enter integer: ")
    try:
        p = int(pot)
    except ValueError:
        print("Please enter an integer amount.")
        add_pot()
    blind = input("What should be the blind value? Enter integer: ")
    try:
        b = int(blind)
    except ValueError:
        print("Please enter an integer amount.")
        add_pot()
    else:
        return p, b


x = add_pot()
for player in players:
    player.add_pot(x[0])
blind = x[1]
continue_playing = True
while continue_playing is True:
    for player in players:
        if player.pot() == 0:
            players.remove(player)
    if player1 not in players:
        print("You have lost!")
        continue_playing = False
    bust = Player('b')
    players.append(bust)
    turn = Turn(player1, players, blind)
    turn.give_cards()
    turn.set_blind()
    turn.first_round()
    if turn.winner() is False:
        turn.second_round()
        if turn.winner() is False:
            remaining = turn.third_round()
            turn.check_winner(remaining)
    next = input("Do you want to continue? If so, press 1. ")
    if next != '1':
        continue_playing = False
