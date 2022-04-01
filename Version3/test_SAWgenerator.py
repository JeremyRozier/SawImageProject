import SAWgenerator


def test_ever_used():
    plan = SAWgenerator.Ariane(10000)
    assert plan.ever_used([0, 0]) is True
    assert plan.ever_used([0, 1]) is False
    assert plan.ever_used([1, 0]) is False


def test_get_possibilities():
    plan = SAWgenerator.Ariane(10000)
    assert plan.get_possibilities() == ["N", "S", "E", "W"]
    plan.map.update({-1: {0: -1}})
    plan.map.update({1: {0: 1}})
    assert plan.get_possibilities() == ["S", "E", "W"]
    plan.map[1][0] = -1
    assert plan.get_possibilities() == ["E", "W"]


def test_see_infinity():
    plan = SAWgenerator.Ariane(10000)
    assert plan.see_infinity() == ["N", "S", "E", "W"]
    plan.map.update({-1: {0: -1}})
    plan.minmax_y[0] = [-1, 0]
    assert plan.see_infinity() == ["S", "E", "W"]


def test_remove_possibilities():
    plan = SAWgenerator.Ariane(10000)
    plan.ariadne_side = "right"
    plan.orientation = "N"
    plan.map.update({-1: {-1: -1}})
    assert plan.remove_possibilities(["N", "E", "W"]) == ["N", "E"]
    plan.map[-1].update({1: -1})
    assert plan.remove_possibilities(["N", "E", "W"]) == ["E"]
    plan.y = -2
    plan.x = 0
    plan.orientation = "S"
    assert plan.remove_possibilities(["S", "E", "W"]) == ["W"]
    plan.ariadne_side = "left"
    assert plan.remove_possibilities(["S", "E", "W"]) == ["E"]


def test_anchor_ariadne():
    plan = SAWgenerator.Ariane(10000)
    plan.anchor_ariadne("N")
    assert plan.map[-2][0] > 0
    assert plan.ariadne_coord[0] == [-2, 0]
    plan.anchor_ariadne("W")
    assert plan.map[0][-2] > 0
    assert plan.ariadne_coord[0] == [0, -2]


def test_look_for_ariadne():
    plan = SAWgenerator.Ariane(10000)
    plan.map.update({-1: {-1: 1}})
    plan.ariadne_coord = [[-1, -1]]
    worked = plan.look_for_ariadne("N")
    assert worked is True


def test_ariadne_line():
    plan = SAWgenerator.Ariane(10000)
    plan.ariadne_side = "right"
    plan.orientation = "N"
    plan.ariadne_line()
    assert plan.map[-1][1] == 1
    assert plan.ariadne_coord == [[-1, 1]]


def test_ariadne_turn():
    plan = SAWgenerator.Ariane(10000)
    plan.ariadne_side = "right"
    plan.orientation = "N"
    plan.ariadne_turn("W")
    assert plan.map[-1][-1] == 1
    assert plan.map[-1][0] == 2
    assert plan.map[-1][1] == 3
    assert plan.ariadne_coord == [[-1, -1], [-1, 0], [-1, 1]]


def test_move():
    plan = SAWgenerator.Ariane(10000)
    plan.orientation = "N"
    plan.move()
    assert plan.map[-1][0] == -1
    assert plan.minmax_y[0] == [-1, 0]
    assert plan.minmax_x[0] == [0, 0]
