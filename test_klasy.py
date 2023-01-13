from klasy import Player, Turn, Dealer
from cpu import CPU


def test_player_init():
    player = Player('Tomek')
    assert player.name() == 'Tomek'
    assert player.pot() == 0
    assert player.hand() == []
    assert player.is_blind() is False


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
    dealer = Dealer()
    dealer.set_game_deck()
    player.add_hand(dealer)
    assert len(player.hand()) == 2


def test_turn():
    player = Player('lmao')
    cpu1 = Player('CPU1')
    cpu2 = Player('CPU2')
    cpu3 = Player('CPU3')
    players = [player, cpu1, cpu2, cpu3]
    turn = Turn(player, players, 1000, 5)
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
    turn = Turn(player, players, 1000, 5)
    turn.give_cards()
    assert len(player.hand()) == 2
    assert len(cpu1.hand()) == 2
    assert len(cpu2.hand()) == 2
    assert len(cpu3.hand()) == 2
    assert len(turn.table().cards()) == 5


def test_turn_raise():
    player = Player('playerone')
    turn = Turn(player, [player], 1000, 5)
    player.add_pot(200)
    turn.player_raise_pot(player, 60)
    assert player.pot() == 140
    assert turn.current_call() == 60
    assert turn.how_many_called() == 1
    assert turn.pot() == 60


def test_turn_raise_check():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    turn = Turn(player, [player, cpu1], 1000, 5)
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
    turn = Turn(player, [player, cpu1], 1000, 5)
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
    turn = Turn(player, [player, cpu1], 1000)
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
    turn = Turn(player, [player, cpu1], 1000)
    player.add_pot(200)
    cpu1.add_pot(200)
    turn.player_raise_pot(player, 60)
    turn.player_fold(cpu1)
    assert cpu1.fold() is True


def test_blind():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    turn = Turn(player, [player, cpu1], 1000)
    turn.set_blind()
    assert player.is_blind() is True


def test_blind2():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    cpu2 = Player('CPU2')
    turn = Turn(player, [player, cpu1, cpu2], 1000)
    cpu1.set_blind(True)
    turn.set_blind()
    assert cpu2.is_blind() is True


def test_blind3():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    cpu2 = Player('CPU2')
    turn = Turn(player, [player, cpu1, cpu2], 1000)
    cpu2.set_blind(True)
    turn.set_blind()
    assert player.is_blind() is True


def test_give_cards():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    cpu2 = Player('CPU2')
    turn = Turn(player, [player, cpu1, cpu2], 1000)
    turn.give_cards()
    assert len(player.hand()) == 2
    assert len(cpu1.hand()) == 2
    assert len(cpu2.hand()) == 2
    assert len(turn.table().cards()) == 5


def test_check():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    cpu2 = Player('CPU2')
    turn = Turn(player, [player, cpu1, cpu2], 1000)
    player._pot += 200
    turn._current_call = 50
    turn.player_check(player)
    assert turn.pot() == 50
    assert player.pot() == 150
    assert turn.how_many_called() == 1
    assert player.call() == 50


def test_check2():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    cpu2 = Player('CPU2')
    turn = Turn(player, [player, cpu1, cpu2], 1000)
    player._pot += 200
    turn._current_call = 50
    player._call = 25
    assert player.call() == 25
    turn.player_check(player)
    assert turn.pot() == 25
    assert player.pot() == 175
    assert turn.how_many_called() == 1


def test_raise_pot():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    cpu2 = Player('CPU2')
    turn = Turn(player, [player, cpu1, cpu2], 1000)
    player._pot += 200
    turn.player_raise_pot(player, 100)
    assert player.pot() == 100
    assert turn.pot() == 100
    assert player.call() == 100
    assert turn.how_many_called() == 1
    turn.player_check(cpu1)
    assert turn.how_many_called() == 2


def test_raise_pot2():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    cpu2 = Player('CPU2')
    turn = Turn(player, [player, cpu1, cpu2], 1000)
    player._pot += 200
    player._call = 50
    assert player.call() == 50
    turn.player_raise_pot(player, 100)
    assert player.pot() == 150
    assert turn.pot() == 50
    assert player.call() == 100
    assert turn.how_many_called() == 1
    turn.player_check(cpu1)
    assert turn.how_many_called() == 2


def test_fold():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    cpu2 = Player('CPU2')
    turn = Turn(player, [player, cpu1, cpu2], 1000)
    turn.player_fold(player)
    assert player.fold() is True
    turn.check_folds()
    assert len(turn.players()) == 2


def test_has_won():
    player = Player('playerone')
    cpu1 = Player('CPU1')
    cpu2 = Player('CPU2')
    turn = Turn(player, [player, cpu1, cpu2], 1000)
    turn._pot = 150
    turn.player_fold(cpu1)
    turn.player_fold(cpu2)
    turn.check_folds()
    turn.has_won()
    assert player.pot() == 150
    assert turn.winner() is True


def test_check_winner():
    player = Player('playerone')
    cpu1 = CPU('CPU1')
    cpu2 = CPU('CPU2')
    turn = Turn(player, [player, cpu1, cpu2], 1000)
    turn._pot = 150
    turn.table()._cards = [
        ('9', 'hearts'),
        ('8', 'diamonds'), ('6', 'spades'), ('8', 'spades'), ('7', 'spades')]
    player._hand = [
        ('10', 'diamonds'), ('jack', 'spades')]
    cpu1._hand = [
        ('10', 'spades'), ('9', 'spades')]
    turn.player_fold(cpu2)
    turn.check_folds()
    turn.check_winner(turn.players())
    assert cpu1.pot() == 150
    assert turn.winner() is True


def test_check_winner_draw():
    player = Player('playerone')
    cpu1 = CPU('CPU1')
    cpu2 = CPU('CPU2')
    turn = Turn(player, [player, cpu1, cpu2], 1000)
    turn._pot = 200
    turn.table()._cards = [
        ('9', 'hearts'),
        ('8', 'diamonds'), ('6', 'spades'), ('queen', 'spades'),
        ('2', 'spades')]
    player._hand = [
        ('10', 'spades'), ('jack', 'spades')]
    cpu1._hand = [
        ('3', 'spades'), ('9', 'spades')]
    turn.player_fold(cpu2)
    turn.check_folds()
    turn.check_winner(turn.players())
    assert cpu1.pot() == 100
    assert player.pot() == 100
    assert turn.winner() is True
