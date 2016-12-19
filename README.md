# wavedrom.py
WaveDrom compatible python command line.

This tool is intended for people who don't want to install 'Node.js' just to use WaveDrom as simple command line.

_wavedrom.py_ directly converts _Wavedrom_ compatible JSON files into SVG format.

## Usage
_wavedrom.py_ command line is argument-compatible with original WaveDrom command line:

```
  WaveDrom.py source < input.json > svg < output.svg >
```

## Important notice

WaveDrom.py command line uses Python's JSON interpreter that is more restrictive than that of WaveDrom Web application.

 * All strings have to be written between quotes (""),
 * Extra commas (,) not supported at end of lists or dictionaries,
 * ONLY SVG output format supported so far

## AsciiDoctor example
An _AsciiDoctor_ example is provided for those who directly want to generate their timing diagrams from _AsciiDoctor_ formatted documents.

