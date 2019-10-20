import os
import subprocess
import sys
from glob import glob
from os.path import splitext, basename

import wavedrom
import pytest
from diff import diff_raster
from diff import main as diff

files_basic = glob("test/files/signal_*.json")
files_subcycle = glob("test/files/subcycle_*.json")
files_assign = glob("test/files/assign_*.json")
files_bitfield = glob("test/files/bitfield_*.json")
files_tutorial = glob("test/files/tutorial_*.json")
files_issues = glob("test/files/issue_*.json")

files = files_basic + files_tutorial + files_issues


def pytest_generate_tests(metafunc):
    metafunc.parametrize("file", files)


def test_render(file):
    jinput = open(file).read()
    wavedrom.render(jinput)


@pytest.fixture(scope="session")
def wavedromdir(tmpdir_factory):
    if "WAVEDROMDIR" in os.environ:
        return os.environ["WAVEDROMDIR"]
    else:
        wavedromdir = tmpdir_factory.mktemp("wavedrom")
        subprocess.check_call("git clone https://github.com/wavedrom/wavedrom.git {}".format(wavedromdir), shell=True)
        subprocess.check_call("git reset --hard 1d4d25181d6660b5d069defcf04583158b51aa5c~1", cwd=str(wavedromdir), shell=True)
        subprocess.check_call("npm install", cwd=str(wavedromdir), shell=True)
        return wavedromdir


@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
def test_upstream(tmpdir,wavedromdir,file):
    base = splitext(basename(file))[0]
    f_out = "{}/{}.svg".format(tmpdir, base)
    f_out_py = "{}/{}_py.svg".format(tmpdir, base)

    subprocess.check_call("node {}/bin/cli.js -i {} > {}".format(wavedromdir, file, f_out), shell=True)
    wavedrom.render_file(file, f_out_py, strict_js_features=True)

    unknown = diff(f_out, f_out_py)

    if len(unknown) > 0:
        msg = "{} mismatch(es)\n".format(len(unknown))
        msg += "js file: {}\npy file: {}\n".format(f_out, f_out_py)
        msg += "\n".join([str(action) for action in unknown])
        pytest.fail(msg)

    img = diff_raster(f_out, f_out_py)

    if img.getbbox() is not None:
        pytest.fail("Raster image comparison failed for " + file)
