from card_comparison import Card
from read_from_json_file import sign
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

    def reset_end_hand(self):
        self._end_hand = []

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

    def reset(self):
        """


        Resets cpu's atributes to values
        from before the turn has started.


        """
        self.set_fold(False)
        self._hand = []
        self._hand_str = ''
        self._call = 0
        self.reset_kicker()
        self.reset_end_hand()

    def kicker(self):
        return self._kicker

    def fold(self):
        return self._folded

    def set_fold(self, bool):
        self._folded = bool

    def set_kicker(self, kicker):
        self._kicker = kicker

    def reset_kicker(self):
        self._kicker_check = []

    def add_hand(self, dealer):
        hand = dealer.get_two()
        for card in hand:
            self._hand.append(card)

    def print_cards(self):
        """


        Prints CPU's cards.


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

    def get_pot_ods(self, turn):
        """


        Divides current call in a turn by
        itself plus current pot in a turn.
        This function helps to calculate
        optimal CPU move.


        """
        current_pot = turn.pot()
        if self.call() == 0:
            call = turn.current_call()
        else:
            call = turn.current_call() - self.call()
        if int(current_pot) + int(call) == 0:
            return 0
        return int(call) / (int(current_pot) + int(call))

    def check_probability(self, turn, round):
        """


        Checks CPU's probability of getting a good
        hand in round 1 or round 2.


        """
        self.reset_end_hand()
        self._hand_str = ''
        self.reset_kicker()
        for card in self.hand():
            self.add_card(card)
        if round == 1:
            n = 3
        else:
            n = 4
        for i in range(0, n):
            self.add_card(turn.table().cards()[i])
        return self.get_probability(turn, round)

    def check_if_check_or_raise(self, turn, round_number):
        """


        Based on the difference between odds of getting a
        good hand and pot odds, this function calculates if
        the CPU should check or raise the current call.


        """
        if round_number == 1:
            difference = 0.2
        else:
            difference = 0.1
        x = self.check_probability(turn, round_number)
        if x['Good hand'] - self.get_pot_ods(turn) > difference:
            _raise = round(0.5*difference*self.pot(), 0)
            if turn.current_call() >= int(_raise):
                turn.player_check(self)
                return True
            turn.player_raise_pot(self, int(_raise))
            return True
        elif x['Good hand'] - self.get_pot_ods(turn) > 0:
            turn.player_check(self)
            return True
        return False

    def get_probability(self, turn, round):
        """


        Based on round number, CPUs hand and cards on the table,
        the function calculates wheter a good hand, or a pair can occur during
        current round and returns a dictionary of them, with the probability of
        occurances as keys. A 'good hand' means two pairs or higher.


        """
        hand_occurance = {}
        cards_to_check = []
        for card in turn.dealer().game_deck():
            cards_to_check.append(card)
        for player in turn.players():
            if player.name() != self.name():
                for card in player.hand():
                    cards_to_check.append(card)
        for card in cards_to_check:
            self.add_card(card)
            for second_card in cards_to_check:
                if second_card != card:
                    self.add_card(second_card)
                    if round != 1:
                        self.remove_card(second_card)
                    card_class = Card()
                    card_class.check_hand(self)
                    if sign[self.hand_str()] >= 27:
                        try:
                            hand_occurance['Good hand'] += 1
                        except Exception:
                            hand_occurance['Good hand'] = 1
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
                            hand_occurance['Nothing'] += 1
                        except Exception:
                            hand_occurance['Nothing'] = 1
                        if round == 1:
                            self.remove_card(second_card)
            self.remove_card(card)
        self.reset_end_hand()
        if 'Good hand' not in hand_occurance.keys():
            hand_occurance['Good hand'] = 0
        if 'Pair' not in hand_occurance.keys():
            hand_occurance['Pair'] = 0
        if 'Nothing' not in hand_occurance.keys():
            hand_occurance['Nothing'] = 0
        occurances = [value for value in hand_occurance.values()]
        all_options = sum(occurances)
        for key in hand_occurance:
            new_value = int(hand_occurance[key]) / (all_options)
            hand_occurance[key] = new_value
        return hand_occurance

    def check_move_round1or2(self, turn, round_num):
        """


        Based on cards on the table, CPU's hand,
        current call, current pot and CPU's pot,
        the function calculates an optimal move
        for the CPU unit in round 1 or 2.


        """
        hand_ocr = self.check_probability(turn, round_num)
        if turn.current_call() - self.call() > self.pot():
            turn.player_fold(self)
            return
        if self.pot() < 25:
            if hand_ocr['Good hand'] == 1.0:
                if turn.current_call() <= self.pot():
                    turn.set_all_in_caller(self)
                    turn.all_in(round_num)
                    return
                else:
                    turn.player_fold(self)
                    return
            else:
                turn.player_fold(self)
                return
        if hand_ocr['Good hand'] > 0.8:
            if self.pot() <= 0.1*turn.entry():
                if turn.current_call() <= self.pot():
                    turn.set_all_in_caller(self)
                    turn.all_in(round_num)
        if turn.current_call() == 0:
            if hand_ocr['Nothing'] == 0.0:
                if hand_ocr['Good hand'] > 0.4:
                    _raise = int(round(0.05*self.pot(), 0))
                    turn.player_raise_pot(self, _raise)
                    return
                else:
                    _raise = int(round(0.03*self.pot(), 0))
                    turn.player_raise_pot(self, _raise)
                    return
            else:
                turn.player_check(self)
                return
        else:
            if self.check_if_check_or_raise(turn, round_num) is True:
                return
            elif turn.current_call() < 0.1*self.pot():
                if round_num == 1:
                    if hand_ocr['Nothing'] < hand_ocr['Pair']:
                        turn.player_check(self)
                        return
                    else:
                        turn.player_fold(self)
                        return
                else:
                    if hand_ocr['Pair'] - hand_ocr['Nothing'] > 0.1:
                        turn.player_check(self)
                        return
                    else:
                        turn.player_fold(self)
                        return
            else:
                turn.player_fold(self)
                return

    def check_move_round3(self, turn):
        """


        Based on CPU's final hand,
        the function calculates an optimal move
        for the CPU unit in round 3.


        """
        self.reset_end_hand()
        self._hand_str = ''
        self.reset_kicker()
        for card in self.hand():
            self.add_card(card)
        for i in range(0, 5):
            self.add_card(turn.table().cards()[i])
        cards_class = Card()
        cards_class.check_hand(self)
        if turn.current_call() - self.call() > self.pot():
            turn.player_fold(self)
            return
        if turn.current_call() > 0:
            if sign[self.hand_str()] > 124:
                _raise = int(round(0.2*self.pot(), 0))
                if turn.current_call() >= _raise:
                    turn.player_check(self)
                    return
                turn.player_raise_pot(self, _raise)
                return
            elif turn.current_call() > 0.2*self.pot():
                if sign[self.hand_str()] > 59:
                    turn.player_check(self)
                    return
                else:
                    turn.player_fold(self)
                    return
            else:
                if sign[self.hand_str()] >= 23:
                    turn.player_check(self)
                    return
                else:
                    turn.player_fold(self)
                    return
        else:
            if sign[self.hand_str()] > 101:
                _raise = int(round(0.1*self.pot(), 0))
                turn.player_raise_pot(self, _raise)
                return
            if sign[self.hand_str()] > 26:
                x = random.randint(1, 4)
                if x == 1:
                    _raise = int(round(0.05*self.pot(), 0))
                    turn.player_raise_pot(self, _raise)
                    return
                elif x == 2:
                    turn.player_check(self)
                    return
                else:
                    _raise = int(round(0.025*self.pot(), 0))
                    turn.player_raise_pot(self, _raise)
                    return
            else:
                turn.player_check(self)
                return
