from card_comparison import check_hand
from card_hierarchy import sign
import random


class CPU:
    def __init__(self, name):
        self._name = name
        self._hand = []
        self._pot = 0
        self._call = 0
        self._is_blind = False
        self._end_hand = []
        self._hand_str = ''
        self._kicker_check = []
        self._kicker = ''
        self._folded = False

    def name(self):
        return self._name

    def hand(self):
        return self._hand

    def pot(self):
        return self._pot

    def add_pot(self, new_pot):
        self._pot += new_pot

    def call(self):
        return self._call

    def reset_call(self):
        self._call = 0

    def add_call(self, new_call):
        self._call += new_call

    def is_blind(self):
        return self._is_blind

    def set_blind(self, bool):
        self._is_blind = bool

    def end_hand(self):
        return self._end_hand

    def add_card(self, card):
        self._end_hand.append(card)

    def remove_card(self, card):
        self._end_hand.remove(card)

    def hand_str(self):
        return self._hand_str

    def add_hand_str(self, str):
        self._hand_str = str

    def kicker_check(self):
        return self._kicker_check

    def add_kicker_check(self, card):
        self._kicker_check.append(card)

    def kicker(self):
        return self._kicker

    def fold(self):
        return self._folded

    def set_fold(self, bool):
        self._folded = bool

    def set_kicker(self, kicker):
        self._kicker = kicker

    def add_hand(self, dealer):
        hand = dealer.get_two()
        for card in hand:
            self._hand.append(card)

    def get_pot_ods(self, turn):
        current_pot = turn.pot()
        if self.call() == 0:
            call = turn.current_call()
        else:
            call = turn.current_call() - self.call()
        return int(call) / (int(current_pot) + int(call))

    def get_propability(self, turn, round):
        hand_occurance = {}
        for card in turn.dealer().game_deck():
            self.add_card(card)
            for second_card in turn.dealer().game_deck():
                if second_card != card:
                    self.add_card(second_card)
                    if round != 1:
                        self.remove_card(second_card)
                    check_hand(self)
                    if sign[self.hand_str()] >= 303:
                        try:
                            hand_occurance['Straight Flush'] += 1
                        except Exception:
                            hand_occurance['Straight Flush'] = 1
                        if round == 1:
                            self.remove_card(second_card)
                    elif sign[self.hand_str()] >= 290:
                        try:
                            hand_occurance['Four of a kind'] += 1
                        except Exception:
                            hand_occurance['Four of a kind'] = 1
                        if round == 1:
                            self.remove_card(second_card)
                    elif sign[self.hand_str()] >= 134:
                        try:
                            hand_occurance['Full house'] += 1
                        except Exception:
                            hand_occurance['Full house'] = 1
                        if round == 1:
                            self.remove_card(second_card)
                    elif sign[self.hand_str()] >= 125:
                        try:
                            hand_occurance['Flush'] += 1
                        except Exception:
                            hand_occurance['Flush'] = 1
                        if round == 1:
                            self.remove_card(second_card)
                    elif sign[self.hand_str()] >= 116:
                        try:
                            hand_occurance['Straight'] += 1
                        except Exception:
                            hand_occurance['Straight'] = 1
                        if round == 1:
                            self.remove_card(second_card)
                    elif sign[self.hand_str()] >= 102:
                        try:
                            hand_occurance['Triple'] += 1
                        except Exception:
                            hand_occurance['Triple'] = 1
                        if round == 1:
                            self.remove_card(second_card)
                    elif sign[self.hand_str()] >= 27:
                        try:
                            hand_occurance['Two pairs'] += 1
                        except Exception:
                            hand_occurance['Two pairs'] = 1
                        if round == 1:
                            self.remove_card(second_card)
                    elif sign[self.hand_str()] >= 14:
                        try:
                            hand_occurance['Pair'] += 1
                        except Exception:
                            hand_occurance['Pair'] = 1
                        if round == 1:
                            self.remove_card(second_card)
                    else:
                        try:
                            hand_occurance['nothing'] += 1
                        except Exception:
                            hand_occurance['nothing'] = 1
                        if round == 1:
                            self.remove_card(second_card)
            self.remove_card(card)
        self._end_hand = []
        try:
            x = hand_occurance['nothing']
        except Exception:
            hand_occurance['nothing'] = 1
        occurances = [value for value in hand_occurance.values()]
        all_options = sum(occurances)
        for key in hand_occurance:
            new_value = int(hand_occurance[key]) / (all_options)
            hand_occurance[key] = new_value
        propabilities = []
        for key in hand_occurance:
            if key != 'nothing' and key != 'Pair':
                propabilities.append(hand_occurance[key])
        return propabilities, hand_occurance

    def check_hand_round1(self, turn):
        for card in self.hand():
            self.add_card(card)
        self.add_card(turn.table().cards()[0])
        self.add_card(turn.table().cards()[1])
        self.add_card(turn.table().cards()[2])
        propabilities = self.get_propability(turn, 1)[0]
        hand_occurance = self.get_propability(turn, 1)[1]
        if self.call() > turn.blind():
            turn.player_check(self)
            print(f"{self.name()} checks.")
            return
        if self.call() > 0:
            if int(turn.current_call()) > 0.1*self.pot():
                if max(propabilities) - self.get_pot_ods(turn) > 0.2:
                    turn.player_check(self)
                    print(f"{self.name()} checks.")
                    return
                if hand_occurance['nothing'] == 0:
                    x = random.randint(1, 4)
                    if x == 1:
                        turn.player_check()
                        print(f"{self.name()} checks.")
                        return
                    if x == 2:
                        _raise = int(0.1*self.pot())
                        turn.player_raise_pot(self, _raise)
                        print(f"{self.name()} raises {_raise}.")
                        return
                    if x == 3:
                        _raise = int(0.05*self.pot())
                        turn.player_raise_pot(self, _raise)
                        print(f"{self.name()} raises {_raise}.")
                        return
                else:
                    turn.player_fold(self)
                    print(f"{self.name()} folds.")
                    return
            else:
                if hand_occurance['nothing'] == 0:
                    x = random.randint(1, 4)
                    if x == 1:
                        turn.player_check(self)
                        print(f"{self.name()} checks.")
                        return
                    if x == 2:
                        _raise = int(0.1*self.pot())
                        turn.player_raise_pot(self, _raise)
                        print(f"{self.name()} raises {_raise}.")
                        return
                    if x == 3:
                        _raise = int(0.05*self.pot())
                        turn.player_raise_pot(self, _raise)
                        print(f"{self.name()} raises {_raise}.")
                        return
                else:
                    turn.player_check(self)
                    print(f"{self.name()} checks.")
                    return
        if hand_occurance['nothing'] == 0:
            _raise = int(0.1*self.pot())
            if turn.current_call() >= _raise:
                turn.player_check(self)
                print(f"{self.name()} checks.")
                return
            turn.player_raise_pot(self, _raise)
            print(f"{self.name()} raises {_raise}.")
            return
        elif max(propabilities) - self.get_pot_ods(turn) > 0.2:
            _raise = int(0.2*self.pot())
            if turn.current_call() >= _raise:
                turn.player_check(self)
                print(f"{self.name()} checks.")
                return
            turn.player_raise_pot(self, _raise)
            print(f"{self.name()} raises {_raise}.")
            return
        elif max(propabilities) - self.get_pot_ods(turn) > 0.15:
            _raise = int(0.15*self.pot())
            if turn.current_call() >= _raise:
                turn.player_check(self)
                print(f"{self.name()} checks.")
                return
            turn.player_raise_pot(self, _raise)
            print(f"{self.name()} raises {_raise}.")
            return
        elif max(propabilities) - self.get_pot_ods(turn) > 0.1:
            _raise = int(0.1*self.pot())
            if turn.current_call() >= _raise:
                turn.player_check(self)
                print(f"{self.name()} checks.")
                return
            turn.player_raise_pot(self, _raise)
            print(f"{self.name()} raises {_raise}.")
            return
        elif max(propabilities) - self.get_pot_ods(turn) > 0.05:
            _raise = int(0.05*self.pot())
            if turn.current_call() >= _raise:
                turn.player_check(self)
                print(f"{self.name()} checks.")
                return
            turn.player_raise_pot(self, _raise)
            print(f"{self.name()} raises {_raise}.")
            return
        elif max(propabilities) > self.get_pot_ods(turn):
            turn.player_check(self)
            print(f"{self.name()} checks.")
            return
        elif self.get_pot_ods(turn) - max(propabilities) < 0.1:
            turn.player_check(self)
            print(f"{self.name()} checks.")
            return
        else:
            if hand_occurance['Pair'] > self.get_pot_ods(turn):
                turn.player_check(self)
                print(f"{self.name()} checks.")
                return
            else:
                self.set_fold(True)
                print(f"{self.name()} folds.")
                return

    def check_hand_round2(self, turn):
        for card in self.hand():
            self.add_card(card)
        self.add_card(turn.table().cards()[0])
        self.add_card(turn.table().cards()[1])
        self.add_card(turn.table().cards()[2])
        self.add_card(turn.table().cards()[3])
        propabilities = self.get_propability(turn, 2)[0]
        hand_occurance = self.get_propability(turn, 2)[1]
        if self.call() > 2*turn.blind():
            turn.player_check(self)
            print(f"{self.name()} checks.")
            return
        if self.call() > 0:
            if int(turn.current_call()) > 0.1*self.pot():
                if max(propabilities) - self.get_pot_ods(turn) > 0.2:
                    turn.player_check(self)
                    print(f"{self.name()} checks.")
                    return
                if hand_occurance['nothing'] == 0:
                    x = random.randint(1, 4)
                    if x != 3:
                        _raise = int(0.1*self.pot())
                        turn.player_raise_pot(self, _raise)
                        print(f"{self.name()} raises {_raise}.")
                        return
                    if x == 3:
                        _raise = int(0.05*self.pot())
                        turn.player_raise_pot(self, _raise)
                        print(f"{self.name()} raises {_raise}.")
                        return
                else:
                    turn.player_fold(self)
                    print(f"{self.name()} folds.")
                    return
            else:
                if hand_occurance['nothing'] == 0:
                    x = random.randint(1, 4)
                    if x != 3:
                        _raise = int(0.1*self.pot())
                        turn.player_raise_pot(self, _raise)
                        print(f"{self.name()} raises {_raise}.")
                        return
                    if x == 3:
                        _raise = int(0.05*self.pot())
                        turn.player_raise_pot(self, _raise)
                        print(f"{self.name()} raises {_raise}.")
                        return
                else:
                    turn.player_check(self)
                    print(f"{self.name()} checks.")
                    return
        if hand_occurance['nothing'] == 0:
            _raise = int(0.1*self.pot())
            if turn.current_call() >= _raise:
                turn.player_check(self)
                print(f"{self.name()} checks.")
                return
            turn.player_raise_pot(self, _raise)
            print(f"{self.name()} raises {_raise}.")
        elif max(propabilities) - self.get_pot_ods(turn) > 0.2:
            _raise = int(0.2*self.pot())
            if turn.current_call() >= _raise:
                turn.player_check(self)
                print(f"{self.name()} checks.")
                return
            turn.player_raise_pot(self, _raise)
            print(f"{self.name()} raises {_raise}.")
            return
        elif max(propabilities) - self.get_pot_ods(turn) > 0.15:
            _raise = int(0.15*self.pot())
            if turn.current_call() >= _raise:
                turn.player_check(self)
                print(f"{self.name()} checks.")
                return
            turn.player_raise_pot(self, _raise)
            print(f"{self.name()} raises {_raise}.")
            return
        elif max(propabilities) - self.get_pot_ods(turn) > 0.1:
            _raise = int(0.1*self.pot())
            if turn.current_call() >= _raise:
                turn.player_check(self)
                print(f"{self.name()} checks.")
                return
            turn.player_raise_pot(self, _raise)
            print(f"{self.name()} raises {_raise}.")
            return
        elif max(propabilities) - self.get_pot_ods(turn) > 0.05:
            _raise = int(0.05*self.pot())
            if turn.current_call() >= _raise:
                turn.player_check(self)
                print(f"{self.name()} checks.")
                return
            turn.player_raise_pot(self, _raise)
            print(f"{self.name()} raises {_raise}.")
            return
        elif max(propabilities) > self.get_pot_ods(turn):
            turn.player_check(self)
            print(f"{self.name()} checks.")
            return
        elif self.get_pot_ods(turn) - max(propabilities) < 0.1:
            turn.player_check(self)
            print(f"{self.name()} checks.")
            return
        else:
            self.set_fold(True)
            print(f"{self.name()} folds.")
            return

    def check_hand_round3(self, turn):
        for card in self.hand():
            self.add_card(card)
        self.add_card(turn.table().cards()[0])
        self.add_card(turn.table().cards()[1])
        self.add_card(turn.table().cards()[2])
        self.add_card(turn.table().cards()[3])
        self.add_card(turn.table().cards()[4])
        check_hand(self)
        if self.call() > 2*turn.blind():
            turn.player_check(self)
            print(f"{self.name()} checks.")
            return
        if self.call() > 0:
            turn.player_check(self)
            print(f"{self.name()} checks.")
            return
        if sign[self.hand_str()] > 115:
            x = random.randint(1, 4)
            if x == 1:
                _raise = int(0.1*self.pot())
                if turn.current_call() >= _raise:
                    turn.player_check(self)
                    print(f"{self.name()} checks.")
                    return
                turn.player_raise_pot(self, _raise)
                print(f"{self.name()} raises {_raise}.")
                return
            elif x == 2:
                _raise = int(0.15*self.pot())
                if turn.current_call() >= _raise:
                    turn.player_check(self)
                    print(f"{self.name()} checks.")
                    return
                turn.player_raise_pot(self, _raise)
                print(f"{self.name()} raises {_raise}.")
                return
            else:
                _raise = int(0.2*self.pot())
                if turn.current_call() >= _raise:
                    turn.player_check(self)
                    print(f"{self.name()} checks.")
                    return
                turn.player_raise_pot(self, _raise)
                print(f"{self.name()} raises {_raise}.")
                return
        if sign[self.hand_str()] > 26:
            turn.player_check(self)
            print(f"{self.name()} checks.")
            return
        if sign[self.hand_str()] > 17:
            turn.player_check(self)
            print(f"{self.name()} checks.")
            return
        if sign[self.hand_str()] > 9:
            x = random.randint(1, 5)
            if x == 1:
                turn.player_fold(self)
                print(f"{self.name()} folds.")
                return
            if x == 2:
                _raise = int(0.05*self.pot())
                if turn.current_call() >= _raise:
                    turn.player_check(self)
                    print(f"{self.name()} checks.")
                    return
                turn.player_raise_pot(self, _raise)
                print(f"{self.name()} raises {_raise}.")
                return
            else:
                turn.player_check(self)
                print(f"{self.name()} checks.")
                return
        else:
            turn.player_fold(self)
            print(f"{self.name()} folds.")
            return




# cpu = CPU('cpu')
# player = Player('tom')
# players = [player, cpu]
# turn = Turn(player, players)
# turn.table()._cards = [
#         ('4', 'hearts'), ('7', 'spades'), ('8', 'diamonds'),
#         ('2', 'clubs'), ('jack', 'diamonds')]
# cpu._hand = [('7', 'hearts'), ('3', 'clubs')]
# cpu.check_hand_round1(turn)
