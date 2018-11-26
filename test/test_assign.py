from fixture import make_test


def test_assign(make_test):
    make_test("assign_xor")
    make_test("assign_gray2binary")
    make_test("assign_binary2gray")
    make_test("assign_74ls688")
    make_test("assign_iec60617")
