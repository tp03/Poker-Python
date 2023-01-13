from cpu import CPU
from klasy import Player, Turn


def test_reset():
    cpu = CPU('cpu')
    cpu._folded = True
    cpu._hand = [('7', 'clubs'), ('9', 'spades')]
    cpu._end_hand = [
        ('4', 'hearts'), ('7', 'spades'), ('8', 'diamonds'),
        ('2', 'clubs'), ('7', 'diamonds'),
        ('7', 'clubs'), ('9', 'diamonds')]
    cpu._hand_str = "Triple '7'"
    cpu._kicker_check = [
        ('4', 'hearts'), ('8', 'diamonds'),
        ('2', 'clubs'), ('9', 'diamonds')]
    cpu._call = 25
    cpu.reset()
    assert cpu.fold() is False
    assert cpu.hand() == []
    assert cpu.end_hand() == []
    assert cpu.hand_str() == ''
    assert cpu.kicker_check() == []
    assert cpu.call() == 0


def test_get_pot_odds():
    player = Player('player')
    cpu = CPU('cpu')
    turn = Turn(player, [player, cpu], 1000)
    turn._current_call = 50
    turn._pot = 150
    assert cpu.get_pot_ods(turn) == 0.25


def test_get_pot_odds2():
    player = Player('player')
    cpu = CPU('cpu')
    turn = Turn(player, [player, cpu], 1000)
    turn._current_call = 40
    cpu._call = 20
    turn._pot = 140
    assert cpu.get_pot_ods(turn) == 0.125
