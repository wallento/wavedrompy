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
