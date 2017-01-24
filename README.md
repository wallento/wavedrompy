# wavedrompy
WaveDrom compatible python command line.

This tool is intended for people who don't want to install the _Node.js_ heavy environment just to use WaveDrom as simple command line.
This tool is a direct translation of javascript file _WaveDrom.js_ to python. No extra features added.

_wavedrom.py_ directly converts _WaveDrom_ compatible JSON files into SVG format.

## Usage
_wavedrom.py_ command line is argument-compatible with original WaveDrom command line:

```
  WaveDrom.py source < input.json > svg < output.svg >
```

## Important notice

_WaveDrom.py_ command line uses Python's JSON interpreter that is more restrictive than that of WaveDrom Web application.

 * All strings have to be written between quotes (""),
 * Extra commas (,) not supported at end of lists or dictionaries,
 * ONLY SVG output format supported so far,
 * _WaveDrom.py_ doesn't support the schematic drawing feature yet,
 * _WaveDrom.py_ was tested under Python V2.7.12 and PythonV3.4.5

## AsciiDoctor example
An _AsciiDoctor_ example is provided for those who directly want to generate their timing diagrams from _AsciiDoctor_ formatted documents.

