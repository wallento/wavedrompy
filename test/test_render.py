import os
import subprocess
import sys

import wavedrom
import pytest
from diff import main as diff

files_basic = ["signal0"]
files_subcycle = ["sub_cycle", "sub_cycle_gaps"]
files_assign = ["assign_"+n for n in ["74ls688", "binary2gray", "gray2binary", "iec60617", "xor"]]
files_bitfield = ["bitfield_{}".format(i) for i in range(1)]
files_tutorial = ["tutorial_{}".format(i) for i in range(13)] + ["tutorial_{}n".format(i) for i in range(2)]

files = files_basic + files_tutorial


def pytest_generate_tests(metafunc):
    metafunc.parametrize("file", files)


def test_render(file):
    jinput = open("test/files/{}.json".format(file)).read()
    wavedrom.render(jinput)


@pytest.fixture(scope="session")
def wavedromdir(tmpdir_factory):
    if "WAVEDROMDIR" in os.environ:
        return os.environ["WAVEDROMDIR"]
    else:
        wavedromdir = tmpdir_factory.mktemp("wavedrom")
        subprocess.check_call("git clone https://github.com/wavedrom/wavedrom.git {}".format(wavedromdir), shell=True)
        subprocess.check_call("npm install", cwd=str(wavedromdir), shell=True)
        return wavedromdir


@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
def test_upstream(tmpdir,wavedromdir,file):
    f_in = "test/files/{}.json".format(file)
    f_out = "{}/{}.svg".format(tmpdir, file)
    f_out_py = "{}/{}_py.svg".format(tmpdir, file)

    subprocess.check_call("{}/bin/cli.js -i {} > {}".format(wavedromdir, f_in, f_out), shell=True)
    wavedrom.render_file(f_in, f_out_py, strict_js_features=True)

    unknown = diff(f_out, f_out_py)

    if len(unknown) > 0:
        msg = "{} mismatch(es)\n".format(len(unknown))
        msg += "js file: {}\npy file: {}\n".format(f_out, f_out_py)
        msg += "\n".join([str(action) for action in unknown])
        pytest.fail(msg)
