import pytest

from wavedrom import WaveDrom
from brick_regressions import all


def pytest_generate_tests(metafunc):
    metafunc.parametrize("test", all)


def test_regression(test):
    w = WaveDrom()
    w.lane.period = test.period
    w.lane.hscale = test.hscale
    w.lane.phase = test.phase
    output = w.parse_wave_lane(test.wave, test.period * test.hscale - 1)
    assert(output == test.expected)