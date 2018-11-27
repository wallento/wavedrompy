import pytest
from wavedrom import render

@pytest.fixture
def make_test():
    def _make_test(name):
        inputfile = "test/{}.json".format(name)

        with open(inputfile, "r") as f:
            jinput = f.read()

        output = render(jinput)

    return _make_test
