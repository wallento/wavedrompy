from fixture import make_test


def test_waveform_basic(make_test):
    make_test("waveform_0")
    make_test("waveform_1")
    make_test("waveform_1n")
    make_test("waveform_2")
    make_test("waveform_3")
    make_test("waveform_4")
    make_test("waveform_5")
    make_test("waveform_6")
    make_test("waveform_7")
    make_test("waveform_8")
    make_test("waveform_9")
    make_test("waveform_10")
    make_test("waveform_11")
    make_test("waveform_12")


def test_waveform_sub_cycle(make_test):
    make_test("waveform_sub_cycle")
    make_test("waveform_sub_cycle_gaps")
