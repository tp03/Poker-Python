from card_hierarchy import sign, Kicker


def check_royal_flush(player):
    for card in player.end_hand():
        if card[0] == '10':
            colour = card[1]
            for card in player.end_hand():
                if card[0] == 'jack' and card[1] == colour:
                    for card in player.end_hand():
                        if card[0] == 'queen' and card[1] == colour:
                            for card in player.end_hand():
                                if card[0] == 'king' and card[1] == colour:
                                    for card in player.end_hand():
                                        if card[0] == 'ace':
                                            if card[1] == colour:
                                                cl = colour
                                                x = f"Royal flush in '{cl}'"
                                                player.add_hand_str(x)
                                                return True
    return False


def check_straight_flush(player):
    flushes = []
    for card in player.end_hand():
        begining = card[0]
        x = sign[begining]
        colour = card[1]
        for card in player.end_hand():
            if sign[card[0]] == (x + 1) and card[1] == colour:
                for card in player.end_hand():
                    if sign[card[0]] == (x + 2) and card[1] == colour:
                        for card in player.end_hand():
                            if sign[card[0]] == (x + 3) and card[1] == colour:
                                for card in player.end_hand():
                                    s = sign[card[0]]
                                    if s == (x + 4) and card[1] == colour:
                                        flushes.append(begining)
    if len(flushes) != 0:
        right_one = max(flushes)
        player.add_hand_str(f"Straight flush from '{right_one}' in '{colour}'")
        return True
    return False


def check_four(player):
    hand_dict = {}
    for card in player.end_hand():
        try:
            hand_dict[card[0]] += 1
        except KeyError:
            hand_dict[card[0]] = 1
    for card in hand_dict:
        if hand_dict[card] == 4:
            player.add_hand_str(f"4 times '{card}'")
            for i in player.end_hand():
                if i[0] != card:
                    player.add_kicker_check(i)
            return True
    return False


def check_full_house(player):
    hand_dict = {}
    for card in player.end_hand():
        try:
            hand_dict[card[0]] += 1
        except KeyError:
            hand_dict[card[0]] = 1
    for card in hand_dict:
        if hand_dict[card] == 3:
            threes = [card]
            for card in hand_dict:
                if hand_dict[card] == 2:
                    two = card
                    player.add_hand_str(f"'{threes[0]}' on '{two}'")
                    return True
                if hand_dict[card] == 3 and card != threes[0]:
                    threes.append(card)
                    three = max(threes)
                    two = min(threes)
                    player.add_hand_str(f"'{three}' on '{two}'")
                    return True
    return False


def check_flush(player):
    hand_dict = {}
    for card in player.end_hand():
        try:
            hand_dict[card[1]] += 1
        except KeyError:
            hand_dict[card[1]] = 1
    for card in hand_dict:
        if hand_dict[card] >= 5:
            colour = card
            values = []
            for card in player.end_hand():
                if card[1] == colour:
                    player.add_kicker_check(card)
                    values.append(sign[card[0]])
            kicker_value = max(values)
            for card in player.kicker_check():
                if sign[card[0]] == kicker_value:
                    player.add_hand_str(f"Flush to '{card[0]}'")
                    return True
    return False


def check_straight(player):
    straights = []
    for card in player.end_hand():
        begining = card[0]
        x = sign[begining]
        for card in player.end_hand():
            if sign[card[0]] == (x + 1):
                for card in player.end_hand():
                    if sign[card[0]] == (x + 2):
                        for card in player.end_hand():
                            if sign[card[0]] == (x + 3):
                                for card in player.end_hand():
                                    if sign[card[0]] == (x + 4):
                                        straights.append(begining)
    if len(straights) != 0:
        right_one = max(straights)
        player.add_hand_str(f"Straight from '{right_one}'")
        return True
    return False


def check_triple(player):
    hand_dict = {}
    for card in player.end_hand():
        try:
            hand_dict[card[0]] += 1
        except KeyError:
            hand_dict[card[0]] = 1
    for card in hand_dict:
        if hand_dict[card] == 3:
            player.add_hand_str(f"Triple '{card}'")
            for tuple in player.end_hand():
                if tuple[0] != card:
                    player.add_kicker_check(tuple)
            return True
    return False


def check_double_pair(player):
    hand_dict = {}
    for card in player.end_hand():
        try:
            hand_dict[card[0]] += 1
        except KeyError:
            hand_dict[card[0]] = 1
    twos = []
    for card in hand_dict:
        if hand_dict[card] == 2:
            twos.append((card, sign[card]))
    if len(twos) == 1:
        return False
    if len(twos) == 2:
        biggest = ('', 0)
        for tuple in twos:
            if tuple[1] > biggest[1]:
                biggest = tuple
        twos.remove(biggest)
        player.add_hand_str(f"Double '{biggest[0]}', double '{twos[0][0]}'")
        for tuple in player.end_hand():
            if tuple[0] != biggest[0] and tuple[0] != twos[0][0]:
                player.add_kicker_check(tuple)
        return True
    if len(twos) == 3:
        biggest = ('', 0)
        for tuple in twos:
            if tuple[1] > biggest[1]:
                biggest = tuple
        twos.remove(biggest)
        mid = ('', 0)
        for tuple in twos:
            if tuple[1] > mid[1]:
                mid = tuple
        player.add_hand_str(f"Double '{biggest[0]}', double '{mid[0]}'")
        for tuple in player.end_hand():
            if tuple[0] != biggest[0] and tuple[0] != mid[0]:
                player.add_kicker_check(tuple)
        return True
    return False


def check_pair(player):
    hand_dict = {}
    for card in player.end_hand():
        try:
            hand_dict[card[0]] += 1
        except KeyError:
            hand_dict[card[0]] = 1
    for card in hand_dict:
        if hand_dict[card] == 2:
            player.add_hand_str(f"Double '{card}'")
            for tuple in player.end_hand():
                if tuple[0] != card:
                    player.add_kicker_check(tuple)
            return True
    return False


def add_kicker(player):
    kicker = ('', 0)
    colour = ''
    for tuple in player.kicker_check():
        if sign[tuple[0]] > kicker[1]:
            kicker = (tuple[0], sign[tuple[0]])
            colour = tuple[1]
    player.set_kicker(f"'{kicker[0]}' in '{colour}'")


def check_hand(player):
    if check_royal_flush(player) is True:
        return
    if check_straight_flush(player) is True:
        return
    if check_four(player) is True:
        return
    if check_full_house(player) is True:
        return
    if check_flush(player) is True:
        return
    if check_straight(player) is True:
        return
    if check_triple(player) is True:
        return
    if check_double_pair(player) is True:
        return
    if check_pair(player) is True:
        return
    player.add_hand_str('nothing')


def cards_comparison(remaining_players, table):
    for player in remaining_players:
        for card in player.hand():
            player.add_card(card)
        for card in table.cards():
            player.add_card(card)
        check_hand(player)
    points = {}
    for player in remaining_players:
        points[player] = sign[player.hand_str()]
    scores = [score for score in points.values()]
    biggest = max(scores)
    winners = []
    for player in points:
        if points[player] == biggest:
            winners.append(player)
    if len(winners) == 1:
        return winners
    else:
        if len(winners[0].kicker_check()) == 0:
            return winners
        else:
            kicker_winners = []
            for player in winners:
                add_kicker(player)
            kickers = {}
            for player in winners:
                kickers[player] = Kicker[player.kicker()]
            biggest = max([score for score in kickers.values()])
            for player in kickers:
                if kickers[player] == biggest:
                    kicker_winners.append(player)
            return kicker_winners