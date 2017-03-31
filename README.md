# WaveDrompy
WaveDrom compatible python command line.

This tool is intended for people who don't want to install the _Node.js_ environment just to use WaveDrom as simple command line.

This tool is a direct translation of original Javascript file _WaveDrom.js_ to Python. No extra feature added.

_WaveDrom.py_ directly converts _WaveDrom_ compatible JSON files into SVG format.

## Usage
The command line is argument-compatible with original WaveDrom command line:

```
  WaveDromEditor source < input.json > svg < output.svg >
```

## Important notice

The command line uses Python's JSON interpreter that is more restrictive than that of original WaveDrom application.

 * All strings have to be written between quotes (""),
 * Extra comma (,) not supported at end of lists or dictionaries,
 * Only SVG output format supported so far,
 * _WaveDrom.py_ doesn't support the schematic drawing feature yet,
 * _WaveDrom.py_ was tested with Python V2.7.12 and Python V3.4.5 under Cygwin and Ubuntu

## Installation

Modify your PATH variable to add the _wavedrompy_ install directory.

If you have trouble running some scripts, try a dos2linux command on them.

If necessary, apply a _chmod a+x_ on _WaveDromEditor_ and _WaveDromEditor.exe_ files.

## AsciiDoctor example
An _AsciiDoctor_ example is provided to directly generate timing diagrams from _AsciiDoctor_ formatted documents.

