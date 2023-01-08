import card_comparison
from klasy import Player, Table
from card_hierarchy import sign


def test_having_royal_flush():
    player = Player('gracz')
    player._end_hand = [
        ('10', 'spades'), ('jack', 'spades'),
        ('queen', 'spades'), ('8', 'diamonds'), ('4', 'diamonds'),
        ('king', 'spades'), ('ace', 'spades'),
    ]
    assert card_comparison.check_royal_flush(player) is True
    assert player.hand_str() == "Royal flush in 'spades'"
    assert sign[player.hand_str()] == 338


def test_having_four():
    player = Player('gracz')
    player._end_hand = [
        ('10', 'spades'), ('10', 'clubs'), ('queen', 'spades'),
        ('10', 'diamonds'), ('4', 'diamonds'),
        ('10', 'hearts'), ('ace', 'spades')
    ]
    assert card_comparison.check_four(player) is True
    assert player.hand_str() == "4 times '10'"
    assert len(player.kicker_check()) == 3


def test_having_straight_flush():
    player = Player('gracz')
    player._end_hand = [
        ('10', 'spades'), ('jack', 'spades'), ('9', 'spades'),
        ('8', 'diamonds'), ('4', 'diamonds'), ('8', 'spades'), ('7', 'spades')
    ]
    assert card_comparison.check_straight_flush(player) is True
    assert player.hand_str() == "Straight flush from '7' in 'spades'"


def test_having_full_house():
    player = Player('gracz')
    player._end_hand = [
        ('10', 'spades'), ('10', 'clubs'), ('queen', 'spades'),
        ('10', 'diamonds'), ('queen', 'diamonds'), ('2', 'hearts'),
        ('ace', 'spades')
    ]
    assert card_comparison.check_full_house(player) is True
    assert player.hand_str() == "'10' on 'queen'"
    assert sign[player.hand_str()] == 239


def test_having_full_house_two_threes():
    player = Player('gracz')
    player._end_hand = [
        ('10', 'spades'), ('10', 'clubs'), ('queen', 'spades'),
        ('10', 'diamonds'), ('queen', 'diamonds'),
        ('queen', 'hearts'), ('ace', 'spades')
    ]
    assert card_comparison.check_full_house(player) is True
    assert player.hand_str() == "'queen' on '10'"


def test_having_flush():
    player = Player('gracz')
    player._end_hand = [
        ('10', 'spades'), ('10', 'clubs'), ('queen', 'spades'),
        ('7', 'diamonds'), ('2', 'spades'), ('5', 'spades'), ('ace', 'spades')
    ]
    assert card_comparison.check_flush(player) is True
    assert player.hand_str() == "Flush to 'ace'"
    assert len(player.kicker_check()) == 5


def test_having_straight():
    player = Player('gracz')
    player._end_hand = [
        ('3', 'spades'), ('jack', 'spades'), ('5', 'clubs'), ('6', 'diamonds'),
        ('4', 'diamonds'), ('10', 'spades'), ('7', 'hearts')]
    assert card_comparison.check_straight(player) is True
    assert player.hand_str() == "Straight from '3'"


def test_having_straight_flush_two_options():
    player = Player('gracz')
    player._end_hand = [
        ('10', 'spades'), ('jack', 'spades'), ('9', 'spades'),
        ('8', 'diamonds'), ('6', 'spades'), ('8', 'spades'), ('7', 'spades')]
    assert card_comparison.check_straight_flush(player) is True
    assert player.hand_str() == "Straight flush from '7' in 'spades'"


def test_having_straight_two_options():
    player = Player('gracz')
    player._end_hand = [
        ('3', 'spades'), ('jack', 'spades'), ('5', 'clubs'),
        ('6', 'diamonds'), ('4', 'diamonds'), ('8', 'spades'), ('7', 'hearts')]
    assert card_comparison.check_straight(player) is True
    assert player.hand_str() == "Straight from '4'"


def test_triple():
    player = Player('gracz')
    player._end_hand = [
        ('10', 'spades'), ('10', 'clubs'), ('queen', 'spades'),
        ('10', 'diamonds'), ('2', 'diamonds'),
        ('5', 'hearts'), ('ace', 'spades'), ]
    assert card_comparison.check_triple(player) is True
    assert player.hand_str() == "Triple '10'"
    assert len(player.kicker_check()) == 4
    assert sign[player.hand_str()] == 111


def test_double_pair():
    player = Player('gracz')
    player._end_hand = [
        ('10', 'spades'), ('10', 'clubs'), ('queen', 'spades'),
        ('3', 'spades'), ('3', 'diamonds'),
        ('5', 'hearts'), ('ace', 'spades')]
    assert card_comparison.check_double_pair(player) is True
    assert player.hand_str() == "Double '10', double '3'"
    assert len(player.kicker_check()) == 3


def test_double_pair_three_pairs():
    player = Player('gracz')
    player._end_hand = [
        ('10', 'spades'), ('10', 'clubs'), ('queen', 'spades'),
        ('3', 'spades'), ('3', 'diamonds'),
        ('5', 'hearts'), ('5', 'spades')]
    assert card_comparison.check_double_pair(player) is True
    assert player.hand_str() == "Double '10', double '5'"
    assert len(player.kicker_check()) == 3


def test_pair():
    player = Player('gracz')
    player._end_hand = [
        ('10', 'spades'), ('7', 'clubs'), ('queen', 'spades'),
        ('3', 'spades'), ('queen', 'diamonds'),
        ('2', 'hearts'), ('5', 'spades')]
    assert card_comparison.check_pair(player) is True
    assert player.hand_str() == "Double 'queen'"
    assert len(player.kicker_check()) == 5


def test_add_kicker():
    player = Player('gracz')
    player._kicker_check = [
        ('10', 'spades'), ('7', 'clubs'),
        ('queen', 'spades'), ('3', 'spades')]
    card_comparison.add_kicker(player)
    assert player.kicker() == "'queen' in 'spades'"


def test_card_comparison():
    player1 = Player('t')
    player1._hand = [('7', 'clubs'), ('9', 'diamonds')]
    player2 = Player('o')
    player2._hand = [('7', 'hearts'), ('3', 'clubs')]
    player3 = Player('m')
    player3._hand = [('jack', 'diamonds'), ('jack', 'spades')]
    remaining_players = [player1, player2, player3]
    table = Table()
    table._cards = [
        ('4', 'hearts'), ('7', 'spades'), ('ace', 'diamonds'),
        ('2', 'clubs'), ('7', 'diamonds')]
    assert len(card_comparison.cards_comparison(remaining_players, table)) == 2


def test_card_comparison2():
    player1 = Player('t')
    player1._hand = [('7', 'clubs'), ('9', 'diamonds')]
    player2 = Player('o')
    player2._hand = [('7', 'hearts'), ('3', 'clubs')]
    player3 = Player('m')
    player3._hand = [('jack', 'diamonds'), ('jack', 'spades')]
    remaining_players = [player1, player2, player3]
    table = Table()
    table._cards = [
        ('4', 'hearts'), ('7', 'spades'), ('8', 'diamonds'),
        ('2', 'clubs'), ('7', 'diamonds')]
    assert len(card_comparison.cards_comparison(remaining_players, table)) == 1


def test_card_comparison3():
    player1 = Player('t')
    player1._hand = [('7', 'clubs'), ('9', 'diamonds')]
    player2 = Player('o')
    player2._hand = [('7', 'hearts'), ('queen', 'clubs')]
    player3 = Player('m')
    player3._hand = [('jack', 'diamonds'), ('jack', 'spades')]
    remaining_players = [player1, player2, player3]
    table = Table()
    table._cards = [
        ('4', 'hearts'), ('7', 'spades'), ('9', 'diamonds'),
        ('2', 'clubs'), ('7', 'diamonds')]
    assert len(card_comparison.cards_comparison(remaining_players, table)) == 1
