import argparse
import json

from .wavedrom import WaveDrom
from .assign import Assign
from .version import version
from .bitfield import BitField


def render(index=0, source="", output=[]):
    source = json.loads(source)
    if source.get("signal"):
        return WaveDrom().renderWaveForm(index, source, output)
    elif source.get("assign"):
        return Assign().render(index, source, output)
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

        output = render(0, jinput)
        output.saveas(outputfile)
