# wavedrompy
WaveDrom compatible python command line.

This tool is intended for people who don't want to install the _Node.js_ environment just to use WaveDrom as simple command line.
This tool is a direct translation of javascript file _WaveDrom.js_ to python. No extra features added.

_wavedrom.py_ directly converts _WaveDrom_ compatible JSON files into SVG format.

## Usage
_WaveDromEditor_ command line is argument-compatible with original WaveDrom command line:

```
  _WaveDromEditor_ source < input.json > svg < output.svg >
```

## Important notice

_WaveDromEditor_ command line uses Python's JSON interpreter that is more restrictive than that of original WaveDrom application.

 * All strings have to be written between quotes (""),
 * Extra commas (,) not supported at end of lists or dictionaries,
 * Only SVG output format supported so far,
 * _WaveDrom.py_ doesn't support the schematic drawing feature yet,
 * _WaveDrom.py_ was tested under Python V2.7.12 and Python V3.4.5

## Installation

Modify your PATH variable to append the _wavedrompy_ root directory.

## AsciiDoctor example
An _AsciiDoctor_ example is provided to directly generate timing diagrams from _AsciiDoctor_ formatted documents.

