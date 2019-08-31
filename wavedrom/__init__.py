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
import os
import sys

from .waveform import WaveDrom
from .assign import Assign
from .version import version
from .bitfield import BitField


def render(source="", output=[], strict_js_features = False):
    source = json.loads(source)
    if source.get("signal"):
        return WaveDrom().render_waveform(0, source, output, strict_js_features)
    elif source.get("assign"):
        return Assign().render(0, source, output)
    elif source.get("reg"):
        return BitField().renderJson(source)


def render_write(source, output, strict_js_features = False):
    jinput = source.read()
    out = render(jinput, strict_js_features=strict_js_features)
    out.write(output)


def render_file(source, output, strict_js_features = False):
    render_write(open(source, "r"), open(output, "w"), strict_js_features=strict_js_features)


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--input", "-i", help="<input wavedrom source filename>",
                        required=True, type=argparse.FileType('r'))
    parser.add_argument("--svg", "-s", help="<output SVG image file name>",
                        nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    render_write(args.input, args.svg, False)
