from klasy import Player, EmptyNameError, Turn
import pytest


def test_player_init():
    player = Player('Tomek')
    assert player.name() == 'Tomek'
    assert player.pot() == 0
    assert player.hand() == []
    assert player.is_blind() is False


def test_player_no_name():
    with pytest.raises(EmptyNameError):
        Player('')


def test_set_pot():
    player = Player('Michał')
    player.add_pot(10000)
    assert player.pot() == 10000


def test_set_blind():
    player = Player('Michał')
    assert player.is_blind() is False
    player.set_blind(True)
    assert player.is_blind() is True


def test_player_hand():
    player = Player('Tomek')
    player.add_hand()
    assert len(player.hand()) == 2


def test_turn():
    player = Player('lmao')
    cpu1 = Player('CPU1')
    cpu2 = Player('CPU2')
    cpu3 = Player('CPU3')
    players = [player, cpu1, cpu2, cpu3]
    turn = Turn(player, players)
    assert turn.gamer() == player
    assert turn.players() == players
    assert turn.pot() == 0
    assert turn.current_call() == 0
    assert turn.how_many_called() == 0


def test_turn_cards():
    player = Player('lmao')
    cpu1 = Player('CPU1')
    cpu2 = Player('CPU2')
    cpu3 = Player('CPU3')
    players = [player, cpu1, cpu2, cpu3]
    turn = Turn(player, players)
    turn.give_cards()
    assert len(player.hand()) == 2
    assert len(cpu1.hand()) == 2
    assert len(cpu2.hand()) == 2
    assert len(cpu3.hand()) == 2
    assert len(turn.table().cards()) == 5


def test_turn_raise():
    player = Player('playerone')
    turn = Turn(player, [player])
    player.add_pot(200)
    turn.player_raise_pot(player, 60)
    assert player.pot() == 140
    assert turn.current_call() == 60
    assert turn.how_many_called() == 1
    assert turn.pot() == 60


def test_turn_raise_check():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    turn = Turn(player, [player, cpu1])
    player.add_pot(200)
    cpu1.add_pot(200)
    turn.player_raise_pot(player, 60)
    assert player.pot() == 140
    assert turn.current_call() == 60
    assert turn.how_many_called() == 1
    assert turn.pot() == 60
    turn.player_check(cpu1)
    assert cpu1.pot() == 140
    assert turn.current_call() == 60
    assert turn.how_many_called() == 2
    assert turn.pot() == 120


def test_turn_two_raises():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    turn = Turn(player, [player, cpu1])
    player.add_pot(200)
    cpu1.add_pot(200)
    turn.player_raise_pot(player, 60)
    assert player.pot() == 140
    assert turn.current_call() == 60
    assert turn.how_many_called() == 1
    assert turn.pot() == 60
    turn.player_raise_pot(cpu1, 100)
    assert cpu1.pot() == 100
    assert turn.current_call() == 100
    assert turn.how_many_called() == 1
    assert turn.pot() == 160


def test_turn_two_raises2():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    turn = Turn(player, [player, cpu1])
    player.add_pot(200)
    cpu1.add_pot(200)
    turn.player_raise_pot(player, 60)
    assert player.pot() == 140
    assert turn.current_call() == 60
    assert turn.how_many_called() == 1
    assert turn.pot() == 60
    turn.player_raise_pot(cpu1, 100)
    assert cpu1.pot() == 100
    assert turn.current_call() == 100
    assert turn.how_many_called() == 1
    assert turn.pot() == 160
    turn.player_check(player)
    assert player.pot() == 100
    assert player.call() == 100
    assert turn.current_call() == 100
    assert turn.how_many_called() == 2
    assert turn.pot() == 200


def test_player_fold():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    turn = Turn(player, [player, cpu1])
    player.add_pot(200)
    cpu1.add_pot(200)
    turn.player_raise_pot(player, 60)
    turn.player_fold(cpu1)
    assert len(turn.players()) == 1


def test_blind():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    turn = Turn(player, [player, cpu1])
    turn.set_blind()
    assert player.is_blind() is True


def test_blind2():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    cpu2 = Player('CPU2')
    turn = Turn(player, [player, cpu1, cpu2])
    cpu1.set_blind(True)
    turn.set_blind()
    assert cpu2.is_blind() is True


def test_blind3():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    cpu2 = Player('CPU2')
    turn = Turn(player, [player, cpu1, cpu2])
    cpu2.set_blind(True)
    turn.set_blind()
    assert player.is_blind() is True


def test_has_won():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    cpu2 = Player('CPU2')
    turn = Turn(player, [player, cpu1, cpu2])
    turn._pot += 1000
    turn.player_fold(cpu1)
    turn.player_fold(cpu2)
    turn.has_won()
    assert player.pot() == 1000
