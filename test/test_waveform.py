from fixture import make_test


def test_waveform_tutorial(make_test):
    make_test("tutorial_0")
    make_test("tutorial_1")
    make_test("tutorial_1n")
    make_test("tutorial_2")
    make_test("tutorial_3")
    make_test("tutorial_4")
    make_test("tutorial_5")
    make_test("tutorial_6")
    make_test("tutorial_7")
    make_test("tutorial_8")
    make_test("tutorial_9")
    make_test("tutorial_10")
    make_test("tutorial_11")
    make_test("tutorial_12")


def test_waveform_sub_cycle(make_test):
    make_test("signal_sub_cycle")
    make_test("signal_sub_cycle_gaps")
