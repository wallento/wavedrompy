# WaveDromPy
WaveDrom compatible python command line.

This tool is intended for people who don't want to install the _Node.js_ environment just to use WaveDrom as simple command line.

This tool is a direct translation of original Javascript file _WaveDrom.js_ to Python. No extra feature added.

_WaveDromPy_ directly converts _WaveDrom_ compatible JSON files into SVG format.

## Usage
_WaveDromPy_ can be called directly:
```
  python wavedrom.py source < input.json > svg < output.svg >
```
 or via the wrapper script _WaveDromEditor(.exe)_ for compatibility with the original WaveDrom command line:

```
  WaveDromEditor source < input.json > svg < output.svg >
```

_WaveDromEditor_  is a script wrapper to be used with Linux.
_WaveDromEditor.exe_ is a script wrapper to be used with Cygwin.

## Important notice

The command line uses Python's JSON interpreter that is more restrictive than that of original WaveDrom application.

 * All strings have to be written between quotes (""),
 * Extra comma (,) not supported at end of lists or dictionaries,
 * Only SVG output format supported so far,
 * _WaveDromPy_ doesn't support the schematic drawing feature yet,
 * _WaveDromPy_ was tested with Python V2.7.12 and Python V3.4.5 under both Cygwin and Ubuntu.

## Installation

`pip install git+https://github.com/K4zuki/wavedrompy.git`

<!-- Modify your PATH environment variable to add the _wavedrompy_ install directory.

If you have trouble running some scripts, try a _'dos2linux'_ command on them.

If necessary, apply a _'chmod a+x'_ on _WaveDromEditor_ and _WaveDromEditor.exe_ files.
-->

## AsciiDoctor example
An _AsciiDoctor_ example is provided to directly generate timing diagrams from _AsciiDoctor_ formatted documents.

