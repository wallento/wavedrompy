# WaveDromPy
WaveDrom compatible python module and command line.

This tool is intended for people who don't want to install the _Node.js_ environment just to use WaveDrom as simple command line.

This tool is a direct translation of original Javascript file _WaveDrom.js_ to Python. No extra feature added.

_WaveDromPy_ directly converts _WaveDrom_ compatible JSON files into SVG format.

[![Build Status](https://travis-ci.org/wallento/wavedrompy.svg?branch=master)](https://travis-ci.org/wallento/wavedrompy)
[![PyPI version](https://badge.fury.io/py/wavedrom.svg)](https://badge.fury.io/py/wavedrom)

## Usage
_WaveDromPy_ can be called directly:
```
  wavedrompy source < input.json > svg < output.svg >
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

`pip install wavedrom`

## AsciiDoctor example
An _AsciiDoctor_ example is provided to directly generate timing diagrams from _AsciiDoctor_ formatted documents.

