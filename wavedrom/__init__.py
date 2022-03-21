# Copyright wavedrompy contributors.
# SPDX-License-Identifier: MIT


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
    out = open(output, "w")
    render_write(open(source, "r"), out, strict_js_features=strict_js_features)
    out.close()


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--input", "-i", help="<input wavedrom source filename>",
                        required=True, type=argparse.FileType('r'))
    parser.add_argument("--svg", "-s", help="<output SVG image file name>",
                        nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    render_write(args.input, args.svg, False)
