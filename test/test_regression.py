import pytest

from wavedrom import WaveDrom
from regressions import all


@pytest.fixture
def make_regression():
    def _make_regression(test):
        w = WaveDrom()
        w.lane.period = test.period
        w.lane.hscale = test.hscale
        w.lane.phase = test.phase
        output = w.parse_wave_lane(test.wave, test.period * test.hscale - 1)
        assert(output == test.expected)
    return _make_regression


def test_regression(make_regression):
    for test in all:
        make_regression(test)