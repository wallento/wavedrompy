# The MIT License (MIT)
#
# Copyright (c) 2018 Stefan Wallentowitz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import argparse
import json

from .waveform import WaveDrom
from .assign import Assign
from .version import version
from .bitfield import BitField


def render(source="", output=[]):
    source = json.loads(source)
    if source.get("signal"):
        return WaveDrom().renderWaveForm(0, source, output)
    elif source.get("assign"):
        return Assign().render(0, source, output)
    elif source.get("reg"):
        return BitField().renderJson(source)


def main(args=None):
    if not args:
        parser = argparse.ArgumentParser(description="")
        parser.add_argument("--input", "-i", help="<input wavedrom source filename>")
        parser.add_argument("--svg", "-s", help="<output SVG image file name>")
        args = parser.parse_args()

    output = []
    inputfile = args.input
    outputfile = args.svg

    if not inputfile or not outputfile:
        parser.print_help()
    else:
        with open(inputfile, "r") as f:
            jinput = f.read()

        output = render(jinput)
        output.saveas(outputfile)
