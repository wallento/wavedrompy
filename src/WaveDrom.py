#! /usr/bin/env python
# The MIT License (MIT)
# 
# Copyright (c) 2011-2016 Aliaksei Chapyzhenka
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
# Translated to Python from original file:
# https://github.com/drom/wavedrom/blob/master/src/WaveDrom.js
#

import sys
import json
import math

font_width1 = 10
font_width2 = 7

lane = {
    "xs"     : 20,    # tmpgraphlane0.width
    "ys"     : 20,    # tmpgraphlane0.height
    "xg"     : 120,   # tmpgraphlane0.x
    "yg"     : 0,     # head gap
    "yh0"    : 0,     # head gap title
    "yh1"    : 0,     # head gap
    "yf0"    : 0,     # foot gap
    "yf1"    : 0,     # foot gap
    "y0"     : 5,     # tmpgraphlane0.y
    "yo"     : 30,    # tmpgraphlane1.y - y0
    "tgo"    : -10,   # tmptextlane0.x - xg
    "ym"     : 15,    # tmptextlane0.y - y0
    "xlabel" : 6,     # tmptextlabel.x - xg
    "xmax"   : 1,
    "scale"  : 1,
    "head"   : {},
    "foot"   : {}
}

WaveSkin=["svg",{"id":"svg","xmlns":"http://www.w3.org/2000/svg","xmlns:xlink":"http://www.w3.org/1999/xlink","height":"0"},["style",{"type":"text/css"},"text{font-size:11pt;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;text-align:center;fill-opacity:1;font-family:Helvetica}.muted{fill:#aaa}.warning{fill:#f6b900}.error{fill:#f60000}.info{fill:#0041c4}.success{fill:#00ab00}.h1{font-size:33pt;font-weight:bold}.h2{font-size:27pt;font-weight:bold}.h3{font-size:20pt;font-weight:bold}.h4{font-size:14pt;font-weight:bold}.h5{font-size:11pt;font-weight:bold}.h6{font-size:8pt;font-weight:bold}.s1{fill:none;stroke:#000;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none}.s2{fill:none;stroke:#000;stroke-width:0.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none}.s3{color:#000;fill:none;stroke:#000;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:1, 3;stroke-dashoffset:0;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate}.s4{color:#000;fill:none;stroke:#000;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0;marker:none;visibility:visible;display:inline;overflow:visible}.s5{fill:#fff;stroke:none}.s6{color:#000;fill:#ffffb4;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1px;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate}.s7{color:#000;fill:#ffe0b9;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1px;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate}.s8{color:#000;fill:#b9e0ff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1px;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate}.s9{fill:#000;fill-opacity:1;stroke:none}.s10{color:#000;fill:#fff;fill-opacity:1;fill-rule:nonzero;stroke:none;stroke-width:1px;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate}.s11{fill:#0041c4;fill-opacity:1;stroke:none}.s12{fill:none;stroke:#0041c4;stroke-width:1;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none}"],
["defs",["g",{"id":"socket"},["rect",{"y":"15","x":"6","height":"20","width":"20"}]],
["g",{"id":"pclk"},["path",{"d":"M0,20 0,0 20,0","class":"s1"}]],
["g",{"id":"nclk"},["path",{"d":"m0,0 0,20 20,0","class":"s1"}]],
["g",{"id":"000"},["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"0m0"},["path",{"d":"m0,20 3,0 3,-10 3,10 11,0","class":"s1"}]],
["g",{"id":"0m1"},["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"0mx"},["path",{"d":"M3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m20,15 -5,5","class":"s2"}],
["path",{"d":"M20,10 10,20","class":"s2"}],
["path",{"d":"M20,5 5,20","class":"s2"}],
["path",{"d":"M20,0 4,16","class":"s2"}],
["path",{"d":"M15,0 6,9","class":"s2"}],
["path",{"d":"M10,0 9,1","class":"s2"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"0md"},["path",{"d":"m8,20 10,0","class":"s3"}],
["path",{"d":"m0,20 5,0","class":"s1"}]],
["g",{"id":"0mu"},["path",{"d":"m0,20 3,0 C 7,10 10.107603,0 20,0","class":"s1"}]],
["g",{"id":"0mz"},["path",{"d":"m0,20 3,0 C 10,10 15,10 20,10","class":"s1"}]],
["g",{"id":"111"},["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"1m0"},["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}]],
["g",{"id":"1m1"},["path",{"d":"M0,0 3,0 6,10 9,0 20,0","class":"s1"}]],
["g",{"id":"1mx"},["path",{"d":"m3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}],
["path",{"d":"m20,15 -5,5","class":"s2"}],
["path",{"d":"M20,10 10,20","class":"s2"}],
["path",{"d":"M20,5 8,17","class":"s2"}],
["path",{"d":"M20,0 7,13","class":"s2"}],
["path",{"d":"M15,0 6,9","class":"s2"}],
["path",{"d":"M10,0 5,5","class":"s2"}],
["path",{"d":"M3.5,1.5 5,0","class":"s2"}]],
["g",{"id":"1md"},["path",{"d":"m0,0 3,0 c 4,10 7,20 17,20","class":"s1"}]],
["g",{"id":"1mu"},["path",{"d":"M0,0 5,0","class":"s1"}],
["path",{"d":"M8,0 18,0","class":"s3"}]],
["g",{"id":"1mz"},["path",{"d":"m0,0 3,0 c 7,10 12,10 17,10","class":"s1"}]],
["g",{"id":"xxx"},["path",{"d":"m0,20 20,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}],
["path",{"d":"M0,5 5,0","class":"s2"}],
["path",{"d":"M0,10 10,0","class":"s2"}],
["path",{"d":"M0,15 15,0","class":"s2"}],
["path",{"d":"M0,20 20,0","class":"s2"}],
["path",{"d":"M5,20 20,5","class":"s2"}],
["path",{"d":"M10,20 20,10","class":"s2"}],
["path",{"d":"m15,20 5,-5","class":"s2"}]],
["g",{"id":"xm0"},["path",{"d":"M0,0 4,0 9,20","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}],
["path",{"d":"M0,5 4,1","class":"s2"}],
["path",{"d":"M0,10 5,5","class":"s2"}],
["path",{"d":"M0,15 6,9","class":"s2"}],
["path",{"d":"M0,20 7,13","class":"s2"}],
["path",{"d":"M5,20 8,17","class":"s2"}]],
["g",{"id":"xm1"},["path",{"d":"M0,0 20,0","class":"s1"}],
["path",{"d":"M0,20 4,20 9,0","class":"s1"}],
["path",{"d":"M0,5 5,0","class":"s2"}],
["path",{"d":"M0,10 9,1","class":"s2"}],
["path",{"d":"M0,15 7,8","class":"s2"}],
["path",{"d":"M0,20 5,15","class":"s2"}]],
["g",{"id":"xmx"},["path",{"d":"m0,20 20,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}],
["path",{"d":"M0,5 5,0","class":"s2"}],
["path",{"d":"M0,10 10,0","class":"s2"}],
["path",{"d":"M0,15 15,0","class":"s2"}],
["path",{"d":"M0,20 20,0","class":"s2"}],
["path",{"d":"M5,20 20,5","class":"s2"}],
["path",{"d":"M10,20 20,10","class":"s2"}],
["path",{"d":"m15,20 5,-5","class":"s2"}]],
["g",{"id":"xmd"},["path",{"d":"m0,0 4,0 c 3,10 6,20 16,20","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}],
["path",{"d":"M0,5 4,1","class":"s2"}],
["path",{"d":"M0,10 5.5,4.5","class":"s2"}],
["path",{"d":"M0,15 6.5,8.5","class":"s2"}],
["path",{"d":"M0,20 8,12","class":"s2"}],
["path",{"d":"m5,20 5,-5","class":"s2"}],
["path",{"d":"m10,20 2.5,-2.5","class":"s2"}]],
["g",{"id":"xmu"},["path",{"d":"M0,0 20,0","class":"s1"}],
["path",{"d":"m0,20 4,0 C 7,10 10,0 20,0","class":"s1"}],
["path",{"d":"M0,5 5,0","class":"s2"}],
["path",{"d":"M0,10 10,0","class":"s2"}],
["path",{"d":"M0,15 10,5","class":"s2"}],
["path",{"d":"M0,20 6,14","class":"s2"}]],
["g",{"id":"xmz"},["path",{"d":"m0,0 4,0 c 6,10 11,10 16,10","class":"s1"}],
["path",{"d":"m0,20 4,0 C 10,10 15,10 20,10","class":"s1"}],
["path",{"d":"M0,5 4.5,0.5","class":"s2"}],
["path",{"d":"M0,10 6.5,3.5","class":"s2"}],
["path",{"d":"M0,15 8.5,6.5","class":"s2"}],
["path",{"d":"M0,20 11.5,8.5","class":"s2"}]],
["g",{"id":"ddd"},["path",{"d":"m0,20 20,0","class":"s3"}]],
["g",{"id":"dm0"},["path",{"d":"m0,20 10,0","class":"s3"}],
["path",{"d":"m12,20 8,0","class":"s1"}]],
["g",{"id":"dm1"},["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"dmx"},["path",{"d":"M3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m20,15 -5,5","class":"s2"}],
["path",{"d":"M20,10 10,20","class":"s2"}],
["path",{"d":"M20,5 5,20","class":"s2"}],
["path",{"d":"M20,0 4,16","class":"s2"}],
["path",{"d":"M15,0 6,9","class":"s2"}],
["path",{"d":"M10,0 9,1","class":"s2"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"dmd"},["path",{"d":"m0,20 20,0","class":"s3"}]],
["g",{"id":"dmu"},["path",{"d":"m0,20 3,0 C 7,10 10.107603,0 20,0","class":"s1"}]],
["g",{"id":"dmz"},["path",{"d":"m0,20 3,0 C 10,10 15,10 20,10","class":"s1"}]],
["g",{"id":"uuu"},["path",{"d":"M0,0 20,0","class":"s3"}]],
["g",{"id":"um0"},["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}]],
["g",{"id":"um1"},["path",{"d":"M0,0 10,0","class":"s3"}],
["path",{"d":"m12,0 8,0","class":"s1"}]],
["g",{"id":"umx"},["path",{"d":"m3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}],
["path",{"d":"m20,15 -5,5","class":"s2"}],
["path",{"d":"M20,10 10,20","class":"s2"}],
["path",{"d":"M20,5 8,17","class":"s2"}],
["path",{"d":"M20,0 7,13","class":"s2"}],
["path",{"d":"M15,0 6,9","class":"s2"}],
["path",{"d":"M10,0 5,5","class":"s2"}],
["path",{"d":"M3.5,1.5 5,0","class":"s2"}]],
["g",{"id":"umd"},["path",{"d":"m0,0 3,0 c 4,10 7,20 17,20","class":"s1"}]],
["g",{"id":"umu"},["path",{"d":"M0,0 20,0","class":"s3"}]],
["g",{"id":"umz"},["path",{"d":"m0,0 3,0 c 7,10 12,10 17,10","class":"s4"}]],
["g",{"id":"zzz"},["path",{"d":"m0,10 20,0","class":"s1"}]],
["g",{"id":"zm0"},["path",{"d":"m0,10 6,0 3,10 11,0","class":"s1"}]],
["g",{"id":"zm1"},["path",{"d":"M0,10 6,10 9,0 20,0","class":"s1"}]],
["g",{"id":"zmx"},["path",{"d":"m6,10 3,10 11,0","class":"s1"}],
["path",{"d":"M0,10 6,10 9,0 20,0","class":"s1"}],
["path",{"d":"m20,15 -5,5","class":"s2"}],
["path",{"d":"M20,10 10,20","class":"s2"}],
["path",{"d":"M20,5 8,17","class":"s2"}],
["path",{"d":"M20,0 7,13","class":"s2"}],
["path",{"d":"M15,0 6.5,8.5","class":"s2"}],
["path",{"d":"M10,0 9,1","class":"s2"}]],
["g",{"id":"zmd"},["path",{"d":"m0,10 7,0 c 3,5 8,10 13,10","class":"s1"}]],
["g",{"id":"zmu"},["path",{"d":"m0,10 7,0 C 10,5 15,0 20,0","class":"s1"}]],
["g",{"id":"zmz"},["path",{"d":"m0,10 20,0","class":"s1"}]],
["g",{"id":"gap"},["path",{"d":"m7,-2 -4,0 c -5,0 -5,24 -10,24 l 4,0 C 2,22 2,-2 7,-2 z","class":"s5"}],
["path",{"d":"M-7,22 C -2,22 -2,-2 3,-2","class":"s1"}],
["path",{"d":"M-3,22 C 2,22 2,-2 7,-2","class":"s1"}]],
["g",{"id":"0mv-3"},["path",{"d":"M9,0 20,0 20,20 3,20 z","class":"s6"}],
["path",{"d":"M3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"1mv-3"},["path",{"d":"M2.875,0 20,0 20,20 9,20 z","class":"s6"}],
["path",{"d":"m3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"xmv-3"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s6"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,5 3.5,1.5","class":"s2"}],
["path",{"d":"M0,10 4.5,5.5","class":"s2"}],
["path",{"d":"M0,15 6,9","class":"s2"}],
["path",{"d":"M0,20 4,16","class":"s2"}]],
["g",{"id":"dmv-3"},["path",{"d":"M9,0 20,0 20,20 3,20 z","class":"s6"}],
["path",{"d":"M3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"umv-3"},["path",{"d":"M3,0 20,0 20,20 9,20 z","class":"s6"}],
["path",{"d":"m3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"zmv-3"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s6"}],
["path",{"d":"m6,10 3,10 11,0","class":"s1"}],
["path",{"d":"M0,10 6,10 9,0 20,0","class":"s1"}]],
["g",{"id":"vvv-3"},["path",{"d":"M20,20 0,20 0,0 20,0","class":"s6"}],
["path",{"d":"m0,20 20,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"vm0-3"},["path",{"d":"M0,20 0,0 3,0 9,20","class":"s6"}],
["path",{"d":"M0,0 3,0 9,20","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"vm1-3"},["path",{"d":"M0,0 0,20 3,20 9,0","class":"s6"}],
["path",{"d":"M0,0 20,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0","class":"s1"}]],
["g",{"id":"vmx-3"},["path",{"d":"M0,0 0,20 3,20 6,10 3,0","class":"s6"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m20,15 -5,5","class":"s2"}],
["path",{"d":"M20,10 10,20","class":"s2"}],
["path",{"d":"M20,5 8,17","class":"s2"}],
["path",{"d":"M20,0 7,13","class":"s2"}],
["path",{"d":"M15,0 7,8","class":"s2"}],
["path",{"d":"M10,0 9,1","class":"s2"}]],
["g",{"id":"vmd-3"},["path",{"d":"m0,0 0,20 20,0 C 10,20 7,10 3,0","class":"s6"}],
["path",{"d":"m0,0 3,0 c 4,10 7,20 17,20","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"vmu-3"},["path",{"d":"m0,0 0,20 3,0 C 7,10 10,0 20,0","class":"s6"}],
["path",{"d":"m0,20 3,0 C 7,10 10,0 20,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"vmz-3"},["path",{"d":"M0,0 3,0 C 10,10 15,10 20,10 15,10 10,10 3,20 L 0,20","class":"s6"}],
["path",{"d":"m0,0 3,0 c 7,10 12,10 17,10","class":"s1"}],
["path",{"d":"m0,20 3,0 C 10,10 15,10 20,10","class":"s1"}]],
["g",{"id":"vmv-3-3"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s6"}],
["path",{"d":"M3,0 0,0 0,20 3,20 6,10 z","class":"s6"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"vmv-3-4"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s7"}],
["path",{"d":"M3,0 0,0 0,20 3,20 6,10 z","class":"s6"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"vmv-3-5"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s8"}],
["path",{"d":"M3,0 0,0 0,20 3,20 6,10 z","class":"s6"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"vmv-4-3"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s6"}],
["path",{"d":"M3,0 0,0 0,20 3,20 6,10 z","class":"s7"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"vmv-4-4"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s7"}],
["path",{"d":"M3,0 0,0 0,20 3,20 6,10 z","class":"s7"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"vmv-4-5"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s8"}],
["path",{"d":"M3,0 0,0 0,20 3,20 6,10 z","class":"s7"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"vmv-5-3"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s6"}],
["path",{"d":"M3,0 0,0 0,20 3,20 6,10 z","class":"s8"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"vmv-5-4"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s7"}],
["path",{"d":"M3,0 0,0 0,20 3,20 6,10 z","class":"s8"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"vmv-5-5"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s8"}],
["path",{"d":"M3,0 0,0 0,20 3,20 6,10 z","class":"s8"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"0mv-4"},["path",{"d":"M9,0 20,0 20,20 3,20 z","class":"s7"}],
["path",{"d":"M3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"1mv-4"},["path",{"d":"M2.875,0 20,0 20,20 9,20 z","class":"s7"}],
["path",{"d":"m3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"xmv-4"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s7"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,5 3.5,1.5","class":"s2"}],
["path",{"d":"M0,10 4.5,5.5","class":"s2"}],
["path",{"d":"M0,15 6,9","class":"s2"}],
["path",{"d":"M0,20 4,16","class":"s2"}]],
["g",{"id":"dmv-4"},["path",{"d":"M9,0 20,0 20,20 3,20 z","class":"s7"}],
["path",{"d":"M3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"umv-4"},["path",{"d":"M3,0 20,0 20,20 9,20 z","class":"s7"}],
["path",{"d":"m3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"zmv-4"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s7"}],
["path",{"d":"m6,10 3,10 11,0","class":"s1"}],
["path",{"d":"M0,10 6,10 9,0 20,0","class":"s1"}]],
["g",{"id":"0mv-5"},["path",{"d":"M9,0 20,0 20,20 3,20 z","class":"s8"}],
["path",{"d":"M3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"1mv-5"},["path",{"d":"M2.875,0 20,0 20,20 9,20 z","class":"s8"}],
["path",{"d":"m3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"xmv-5"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s8"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,5 3.5,1.5","class":"s2"}],
["path",{"d":"M0,10 4.5,5.5","class":"s2"}],
["path",{"d":"M0,15 6,9","class":"s2"}],
["path",{"d":"M0,20 4,16","class":"s2"}]],
["g",{"id":"dmv-5"},["path",{"d":"M9,0 20,0 20,20 3,20 z","class":"s8"}],
["path",{"d":"M3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"umv-5"},["path",{"d":"M3,0 20,0 20,20 9,20 z","class":"s8"}],
["path",{"d":"m3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"zmv-5"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s8"}],
["path",{"d":"m6,10 3,10 11,0","class":"s1"}],
["path",{"d":"M0,10 6,10 9,0 20,0","class":"s1"}]],
["g",{"id":"vvv-4"},["path",{"d":"M20,20 0,20 0,0 20,0","class":"s7"}],
["path",{"d":"m0,20 20,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"vm0-4"},["path",{"d":"M0,20 0,0 3,0 9,20","class":"s7"}],
["path",{"d":"M0,0 3,0 9,20","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"vm1-4"},["path",{"d":"M0,0 0,20 3,20 9,0","class":"s7"}],
["path",{"d":"M0,0 20,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0","class":"s1"}]],
["g",{"id":"vmx-4"},["path",{"d":"M0,0 0,20 3,20 6,10 3,0","class":"s7"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m20,15 -5,5","class":"s2"}],
["path",{"d":"M20,10 10,20","class":"s2"}],
["path",{"d":"M20,5 8,17","class":"s2"}],
["path",{"d":"M20,0 7,13","class":"s2"}],
["path",{"d":"M15,0 7,8","class":"s2"}],
["path",{"d":"M10,0 9,1","class":"s2"}]],
["g",{"id":"vmd-4"},["path",{"d":"m0,0 0,20 20,0 C 10,20 7,10 3,0","class":"s7"}],
["path",{"d":"m0,0 3,0 c 4,10 7,20 17,20","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"vmu-4"},["path",{"d":"m0,0 0,20 3,0 C 7,10 10,0 20,0","class":"s7"}],
["path",{"d":"m0,20 3,0 C 7,10 10,0 20,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"vmz-4"},["path",{"d":"M0,0 3,0 C 10,10 15,10 20,10 15,10 10,10 3,20 L 0,20","class":"s7"}],
["path",{"d":"m0,0 3,0 c 7,10 12,10 17,10","class":"s1"}],
["path",{"d":"m0,20 3,0 C 10,10 15,10 20,10","class":"s1"}]],
["g",{"id":"vvv-5"},["path",{"d":"M20,20 0,20 0,0 20,0","class":"s8"}],
["path",{"d":"m0,20 20,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"vm0-5"},["path",{"d":"M0,20 0,0 3,0 9,20","class":"s8"}],
["path",{"d":"M0,0 3,0 9,20","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"vm1-5"},["path",{"d":"M0,0 0,20 3,20 9,0","class":"s8"}],
["path",{"d":"M0,0 20,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0","class":"s1"}]],
["g",{"id":"vmx-5"},["path",{"d":"M0,0 0,20 3,20 6,10 3,0","class":"s8"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m20,15 -5,5","class":"s2"}],
["path",{"d":"M20,10 10,20","class":"s2"}],
["path",{"d":"M20,5 8,17","class":"s2"}],
["path",{"d":"M20,0 7,13","class":"s2"}],
["path",{"d":"M15,0 7,8","class":"s2"}],
["path",{"d":"M10,0 9,1","class":"s2"}]],
["g",{"id":"vmd-5"},["path",{"d":"m0,0 0,20 20,0 C 10,20 7,10 3,0","class":"s8"}],
["path",{"d":"m0,0 3,0 c 4,10 7,20 17,20","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"vmu-5"},["path",{"d":"m0,0 0,20 3,0 C 7,10 10,0 20,0","class":"s8"}],
["path",{"d":"m0,20 3,0 C 7,10 10,0 20,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"vmz-5"},["path",{"d":"M0,0 3,0 C 10,10 15,10 20,10 15,10 10,10 3,20 L 0,20","class":"s8"}],
["path",{"d":"m0,0 3,0 c 7,10 12,10 17,10","class":"s1"}],
["path",{"d":"m0,20 3,0 C 10,10 15,10 20,10","class":"s1"}]],
["g",{"id":"Pclk"},["path",{"d":"M-3,12 0,3 3,12 C 1,11 -1,11 -3,12 z","class":"s9"}],
["path",{"d":"M0,20 0,0 20,0","class":"s1"}]],
["g",{"id":"Nclk"},["path",{"d":"M-3,8 0,17 3,8 C 1,9 -1,9 -3,8 z","class":"s9"}],
["path",{"d":"m0,0 0,20 20,0","class":"s1"}]],
["g",{"id":"vvv-2"},["path",{"d":"M20,20 0,20 0,0 20,0","class":"s10"}],
["path",{"d":"m0,20 20,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"vm0-2"},["path",{"d":"M0,20 0,0 3,0 9,20","class":"s10"}],
["path",{"d":"M0,0 3,0 9,20","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"vm1-2"},["path",{"d":"M0,0 0,20 3,20 9,0","class":"s10"}],
["path",{"d":"M0,0 20,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0","class":"s1"}]],
["g",{"id":"vmx-2"},["path",{"d":"M0,0 0,20 3,20 6,10 3,0","class":"s10"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m20,15 -5,5","class":"s2"}],
["path",{"d":"M20,10 10,20","class":"s2"}],
["path",{"d":"M20,5 8,17","class":"s2"}],
["path",{"d":"M20,0 7,13","class":"s2"}],
["path",{"d":"M15,0 7,8","class":"s2"}],
["path",{"d":"M10,0 9,1","class":"s2"}]],
["g",{"id":"vmd-2"},["path",{"d":"m0,0 0,20 20,0 C 10,20 7,10 3,0","class":"s10"}],
["path",{"d":"m0,0 3,0 c 4,10 7,20 17,20","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"vmu-2"},["path",{"d":"m0,0 0,20 3,0 C 7,10 10,0 20,0","class":"s10"}],
["path",{"d":"m0,20 3,0 C 7,10 10,0 20,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"vmz-2"},["path",{"d":"M0,0 3,0 C 10,10 15,10 20,10 15,10 10,10 3,20 L 0,20","class":"s10"}],
["path",{"d":"m0,0 3,0 c 7,10 12,10 17,10","class":"s1"}],
["path",{"d":"m0,20 3,0 C 10,10 15,10 20,10","class":"s1"}]],
["g",{"id":"0mv-2"},["path",{"d":"M9,0 20,0 20,20 3,20 z","class":"s10"}],
["path",{"d":"M3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"1mv-2"},["path",{"d":"M2.875,0 20,0 20,20 9,20 z","class":"s10"}],
["path",{"d":"m3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"xmv-2"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s10"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,5 3.5,1.5","class":"s2"}],
["path",{"d":"M0,10 4.5,5.5","class":"s2"}],
["path",{"d":"M0,15 6,9","class":"s2"}],
["path",{"d":"M0,20 4,16","class":"s2"}]],
["g",{"id":"dmv-2"},["path",{"d":"M9,0 20,0 20,20 3,20 z","class":"s10"}],
["path",{"d":"M3,20 9,0 20,0","class":"s1"}],
["path",{"d":"m0,20 20,0","class":"s1"}]],
["g",{"id":"umv-2"},["path",{"d":"M3,0 20,0 20,20 9,20 z","class":"s10"}],
["path",{"d":"m3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,0 20,0","class":"s1"}]],
["g",{"id":"zmv-2"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s10"}],
["path",{"d":"m6,10 3,10 11,0","class":"s1"}],
["path",{"d":"M0,10 6,10 9,0 20,0","class":"s1"}]],
["g",{"id":"vmv-3-2"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s10"}],
["path",{"d":"M3,0 0,0 0,20 3,20 6,10 z","class":"s6"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"vmv-4-2"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s10"}],
["path",{"d":"M3,0 0,0 0,20 3,20 6,10 z","class":"s7"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"vmv-5-2"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s10"}],
["path",{"d":"M3,0 0,0 0,20 3,20 6,10 z","class":"s8"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"vmv-2-3"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s6"}],
["path",{"d":"M3,0 0,0 0,20 3,20 6,10 z","class":"s10"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"vmv-2-4"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s7"}],
["path",{"d":"M3,0 0,0 0,20 3,20 6,10 z","class":"s10"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"vmv-2-5"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s8"}],
["path",{"d":"M3,0 0,0 0,20 3,20 6,10 z","class":"s10"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"vmv-2-2"},["path",{"d":"M9,0 20,0 20,20 9,20 6,10 z","class":"s10"}],
["path",{"d":"M3,0 0,0 0,20 3,20 6,10 z","class":"s10"}],
["path",{"d":"m0,0 3,0 6,20 11,0","class":"s1"}],
["path",{"d":"M0,20 3,20 9,0 20,0","class":"s1"}]],
["g",{"id":"arrow0"},["path",{"d":"m-12,-3 9,3 -9,3 c 1,-2 1,-4 0,-6 z","class":"s11"}],
["path",{"d":"M0,0 -15,0","class":"s12"}]],
["marker",{"id":"arrowhead","style":"fill:#0041c4","markerHeight":"7","markerWidth":"10","markerUnits":"strokeWidth","viewBox":"0 -4 11 8","refX":"15","refY":"0","orient":"auto"},["path",{"d":"M0 -4 11 0 0 4z"}]],
["marker",{"id":"arrowtail","style":"fill:#0041c4","markerHeight":"7","markerWidth":"10","markerUnits":"strokeWidth","viewBox":"-11 -4 11 8","refX":"-15","refY":"0","orient":"auto"},["path",{"d":"M0 -4 -11 0 0 4z"}]]],
["g",{"id":"waves"},["g",{"id":"lanes"}],
["g",{"id":"groups"}]]];

def genBrick (texts, extra, times) :
    
    R = []
    if len( texts ) == 4 :
        for j in range( times ):
            
            R.append(texts[0])
            
            for i in range ( extra ):
                R.append(texts[1])
            
            R.append(texts[2])
            for i in range ( extra ):
                R.append(texts[3])
                    
        return R
    
    if len( texts ) == 1 :
        texts.append(texts[0])
    
    R.append(texts[0])
    for i in range (times * (2 * (extra + 1)) - 1) :
        R.append(texts[1])
    return R

def genFirstWaveBrick (text, extra, times) :
    
    pattern = {
        'p': ['pclk', '111', 'nclk', '000'], 
        'n': ['nclk', '000', 'pclk', '111'], 
        'P': ['Pclk', '111', 'nclk', '000'], 
        'N': ['Nclk', '000', 'pclk', '111'], 
        'l': ['000'],
        'L': ['000'],
        '0': ['000'],
        'h': ['111'],
        'H': ['111'],
        '1': ['111'],
        '=': ['vvv-2'],
        '2': ['vvv-2'],
        '3': ['vvv-3'],
        '4': ['vvv-4'],
        '5': ['vvv-5'],
        'd': ['ddd'],
        'u': ['uuu'],
        'z': ['zzz']
        }
    
    return genBrick( pattern.get( text,  ['xxx'] )  , extra, times );

def genWaveBrick (text, extra, times) :
    
    x1 = {'p':'pclk', 'n':'nclk', 'P':'Pclk', 'N':'Nclk', 'h':'pclk', 'l':'nclk', 'H':'Pclk', 'L':'Nclk'}
    x2 = {'0':'0', '1':'1', 'x':'x', 'd':'d', 'u':'u', 'z':'z', '=':'v',  '2':'v',  '3':'v',  '4':'v',  '5':'v' }
    x3 = {'0': '', '1': '', 'x': '', 'd': '', 'u': '', 'z': '', '=':'-2', '2':'-2', '3':'-3', '4':'-4', '5':'-5'}
    y1 = {
        'p':'0', 'n':'1',
        'P':'0', 'N':'1',
        'h':'1', 'l':'0',
        'H':'1', 'L':'0',
        '0':'0', '1':'1', 'x':'x', 'd':'d', 'u':'u', 'z':'z', '=':'v', '2':'v', '3':'v', '4':'v', '5':'v'}
    
    y2 = {
        'p': '', 'n': '',
        'P': '', 'N': '',
        'h': '', 'l': '',
        'H': '', 'L': '',
        '0': '', '1': '', 'x': '', 'd': '', 'u': '', 'z': '', '=':'-2', '2':'-2', '3':'-3', '4':'-4', '5':'-5'}
    
    x4 = {
        'p': '111', 'n': '000',
        'P': '111', 'N': '000',
        'h': '111', 'l': '000',
        'H': '111', 'L': '000',
        '0': '000', '1': '111', 'x': 'xxx', 'd': 'ddd', 'u': 'uuu', 'z': 'zzz',
        '=': 'vvv-2', '2': 'vvv-2', '3': 'vvv-3', '4': 'vvv-4', '5': 'vvv-5'}
    
    x5 = {'p':'nclk', 'n':'pclk', 'P':'nclk', 'N':'pclk'}
    x6 = {'p': '000', 'n': '111', 'P': '000', 'N': '111'}
    xclude = {'hp':'111', 'Hp':'111', 'ln': '000', 'Ln': '000', 'nh':'111', 'Nh':'111', 'pl': '000', 'Pl':'000'}

    #atext = text.split()
    atext = text

    tmp0 = x4.get(atext[1])
    tmp1 = x1.get(atext[1])
    if tmp1 == None :
        tmp2 = x2.get(atext[1])
        if tmp2 == None :
            # unknown
            return genBrick(['xxx'], extra, times)
        else :
            tmp3 = y1.get(atext[0])
            if tmp3 == None :
                # unknown
                return genBrick(['xxx'], extra, times)
            
            # soft curves
            return genBrick([tmp3 + 'm' + tmp2 + y2[atext[0]] + x3[atext[1]], tmp0], extra, times)
        
    else :
        tmp4 = xclude.get(text)
        if tmp4 != None :
            tmp1 = tmp4
        
        # sharp curves
        tmp2 = x5.get(atext[1])
        if tmp2 == None :
            # hlHL
            return genBrick([tmp1, tmp0], extra, times)
        else :
            # pnPN
            return genBrick([tmp1, tmp0, tmp2, x6[atext[1]]], extra, times)
        
def parseWaveLane (text, extra) :
    
    R = []
    Stack = text
    Next   = Stack[0]
    Stack  = Stack[1:]

    Repeats = 1
    while len(Stack) and ( Stack[0] == '.' or Stack[0] == '|' ): # repeaters parser
        Stack=Stack[1:]
        Repeats += 1
    
    R.extend(genFirstWaveBrick(Next, extra, Repeats))

    while len(Stack) :
        Top = Next
        Next = Stack[0]
        Stack = Stack[1:]
        Repeats = 1
        while len(Stack) and ( Stack[0] == '.' or Stack[0] == '|' ) : # repeaters parser
            Stack=Stack[1:]
            Repeats += 1
        R.extend(genWaveBrick((Top + Next), extra, Repeats))
    
    for i in range( lane['phase'] ):
        R = R[1:]
    return R

def parseWaveLanes (sig) :
    
    def data_extract (e) :
        tmp = e.get('data')
        if tmp == None : return None 
        if type (tmp) is str or type(tmp) is unicode: tmp=tmp.split()
        return tmp

    content = []
    for sigx in sig :
        lane['period'] = sigx.get('period',1)
        lane['phase']  = int( sigx.get('phase',0 ) * 2 )
        sub_content=[]
        sub_content.append( [sigx.get('name',' '), sigx.get('phase',0 ) ] )
        sub_content.append( parseWaveLane( sigx['wave'], int(lane['period'] * lane['hscale'] - 1 ) ) if sigx.get('wave') else None )
        sub_content.append( data_extract(sigx) )
        content.append(sub_content)

    return content

def findLaneMarkers (lanetext) :
    
    lcount = 0
    gcount = 0
    ret = []
    for i in range( len( lanetext ) ) :
        if lanetext[i] == 'vvv-2' or lanetext[i] == 'vvv-3' or lanetext[i] == 'vvv-4' or lanetext[i] == 'vvv-5' :
            lcount += 1
        else :
            if lcount !=0 :
                ret.append(gcount - ((lcount + 1) / 2))
                lcount = 0
        
        gcount += 1
    
    if lcount != 0 :
        ret.append(gcount - ((lcount + 1) / 2))
    
    return ret

def renderWaveLane (root, content, index) :

    xmax     = 0
    xgmax    = 0
    glengths = []
    svgns    = 'http://www.w3.org/2000/svg'
    xlinkns  = 'http://www.w3.org/1999/xlink'
    xmlns    = 'http://www.w3.org/XML/1998/namespace'
    for j in range( len(content) ):
        name = content[j][0][0]
        if name : # check name
            g = [
                'g',
                {
                    'id': 'wavelane_' + str(j) + '_' + str(index),
                    'transform': 'translate(0,' + str(lane['y0'] + j * lane['yo']) + ')'
                }
            ]
            root.append(g)
            title = [
                'text',
                {
                    'x': lane['tgo'],
                    'y': lane['ym'],
                    'class': 'info',
                    'text-anchor': 'end',
                    'xml:space': 'preserve'
                },
                ['tspan', name]
            ]
            g.append(title)

            glengths.append( len(name) * font_width1 + font_width1 )
            
            xoffset = content[j][0][1]
            xoffset = math.ceil(2 * xoffset) - 2 * xoffset if xoffset > 0 else  -2 * xoffset
            gg = [
                'g',
                {
                    'id': 'wavelane_draw_' + str(j) + '_' + str(index),
                    'transform': 'translate(' + str( xoffset * lane['xs'] ) + ', 0)'
                }
            ]
            g.append(gg)

            if content[j][1] :
                for i in range( len(content[j][1]) ) :
                    b = [
                       'use',
                       {
                           #'id': 'use_' + str(i) + '_' + str(j) + '_' + str(index),
                           'xmlns:xlink':xlinkns,
                           'xlink:href': '#' + str( content[j][1][i] ),
                           'transform': 'translate(' + str(i * lane['xs']) + ')'
                       }
                    ]
                    gg.append(b)
                
                if content[j][2] and len(content[j][2]) :
                    labels = findLaneMarkers(content[j][1])
                    if len(labels) != 0 :
                        for k in range( len(labels) ) :
                            if content[j][2] and k < len(content[j][2]) :
                                title = [
                                    'text',
                                    {
                                        'x': int(labels[k]) * lane['xs'] + lane['xlabel'],
                                        'y': lane['ym'],
                                        'text-anchor': 'middle',
                                        'xml:space': 'preserve'
                                    },
                                    ['tspan',content[j][2][k]]
                                ]
                                gg.append(title)
                            
                
                if len(content[j][1]) > xmax :
                    xmax = len(content[j][1])
                
    lane['xmax'] = xmax
    lane['xg'] = xgmax + 20
    return glengths

def renderMarks (root, content, index) :

    def captext ( g, cxt, anchor, y ) :
    
        if cxt.get(anchor) and cxt[anchor].get('text') :
            tmark = [
                'text',
                {
                    'x': float( cxt['xmax'] ) * float( cxt['xs'] ) / 2,
                    'y': y,
                    'text-anchor': 'middle',
                    'fill': '#000',
                    'xml:space': 'preserve'
                }, cxt[anchor]['text']
            ]
            g.append(tmark)

    def ticktock ( g, cxt, ref1, ref2, x, dx, y, length ) :
        L = []
    
        if cxt.get(ref1) == None or cxt[ref1].get(ref2) == None :
            return

        val = cxt[ref1][ref2]
        if type( val ) is str or type( val ) is unicode :
            val = val.split()
        elif type( val ) is int :
            offset = val
            val = []
            for i in range ( length ) :
                val.append(i + offset)

        if type( val ) is list :
            if len( val ) == 0 :
                return
            elif len( val ) == 1 :
                offset = val[0]
                if type(offset) is str or type(offset) is unicode:
                    L = val
                else :
                    for i in range ( length ) :
                        L[i] = i + offset
                    
            elif len( val ) == 2:
                offset = int(val[0])
                step   = int(val[1])
                tmp = val[1].split('.')
                if len( tmp ) == 2 :
                    dp = len( tmp[1] )
                
                if ( type(offset) is str or type( offset ) is unicode ) or ( type(step) is str or type(step) is unicode ) :
                    L = val
                else :
                    offset = step * offset
                    for i in range( length ) :
                        L[i] = "{0:.",dp,"f}".format(step * i + offset)
                    
            else :
                L = val
            
        else :
           return
        
        for i in range( length ) :
            tmp = L[i]
            tmark = [
                'text',
                {
                    'x': i * dx + x,
                    'y': y,
                    'text-anchor': 'middle',
                    'class': 'muted',
                    'xml:space': 'preserve'
                }, str(tmp)
            ]
            g.append(tmark)

    mstep  = 2 * int(lane['hscale'])
    mmstep = mstep * lane['xs']
    marks  = int(lane['xmax']) / mstep
    gy     = len( content ) * int(lane['yo'])

    g = ['g', {'id': 'gmarks_' + str(index)}]
    root.insert(0,g)

    for i in range( marks + 1):
        gg = [
            'path',
            {
                'id':    'gmark_' + str(i) + '_' + str(index),
                'd':     'm ' + str(i * mmstep) + ',' + '0' + ' 0,' + str(gy),
                'style': 'stroke:#888;stroke-width:0.5;stroke-dasharray:1,3'
            }
        ]
        g.append( gg )

    captext(g, lane, 'head', -33 if lane['yh0'] else -13 )
    captext(g, lane, 'foot', gy + ( 45 if lane['yf0'] else 25 ) )
    
    ticktock( g, lane, 'head', 'tick',          0, mmstep,      -5, marks + 1)
    ticktock( g, lane, 'head', 'tock', mmstep / 2, mmstep,      -5, marks)
    ticktock( g, lane, 'foot', 'tick',          0, mmstep, gy + 15, marks + 1)
    ticktock( g, lane, 'foot', 'tock', mmstep / 2, mmstep, gy + 15, marks)

def renderArcs (root, source, index, top) :

    Stack = []
    Edge = {'words': [], 'frm': 0, 'shape': '', 'to': 0, 'label': ''}
    Events = {}
    svgns = 'http://www.w3.org/2000/svg'
    xmlns = 'http://www.w3.org/XML/1998/namespace'

    if source :
        for i in range (len (source) ) :
            lane['period'] = source[i].get('period',1)
            lane['phase']  = int( source[i].get('phase',0 ) * 2 )
            text = source[i].get('node')
            if text:
                Stack = text
                pos = 0
                while len( Stack ) :
                    eventname = Stack[0]
                    Stack=Stack[1:]
                    if eventname != '.' :                 
                        Events[eventname] = {
                            'x' : str( int( float( lane['xs'] ) * (2 * pos * lane['period'] * lane['hscale'] - lane['phase'] ) + float( lane['xlabel'] ) ) ),
                            'y' : str( int( i * lane['yo'] + lane['y0'] + float( lane['ys'] ) * 0.5 ) )
                        }
                    pos += 1

        gg = [ 'g', { 'id' : 'wavearcs_' + str( index ) } ]
        root.append(gg)

        if top.get('edge') :
            for i in range( len ( top['edge'] ) ) :
                Edge['words'] = top['edge'][i].split()
                Edge['label'] = top['edge'][i][len(Edge['words'][0]):]
                Edge['label'] = Edge['label'][1:]
                Edge['frm']   = Edge['words'][0][0]
                Edge['to']    = Edge['words'][0][-1]
                Edge['shape'] = Edge['words'][0][1:-1]
                frm  = Events[Edge['frm']]
                to   = Events[Edge['to']]
                gmark = [ 
                  'path',
                   { 
                     'id': 'gmark_' + Edge['frm'] + '_' + Edge['to'],
                     'd': 'M ' + frm['x'] + ',' + frm['y'] + ' ' + to['x']   + ',' + to['y'],
                     'style': 'fill:none;stroke:#00F;stroke-width:1' 
                   }
                ]
                gg.append(gmark)
                dx = float( to['x'] ) - float( frm['x'] )
                dy = float( to['y'] ) - float( frm['y'] )
                lx = (float(frm['x']) + float(to['x'])) / 2
                ly = (float(frm['y']) + float(to['y'])) / 2
                pattern = {
                    '~'    : {'d': 'M ' + frm['x'] + ',' + frm['y'] + ' c ' + str(0.7 * dx) + ', 0 ' + str(0.3 * dx) + ', ' + str(dy) + ' ' + str(dx) + ', ' + str(dy) },
                    '-~'   : {'d': 'M ' + frm['x'] + ',' + frm['y'] + ' c ' + str(0.7 * dx) + ', 0 ' +       str(dx) + ', ' + str(dy) + ' ' + str(dx) + ', ' + str(dy) },
                    '~-'   : {'d': 'M ' + frm['x'] + ',' + frm['y'] + ' c ' + '0'           + ', 0 ' + str(0.3 * dx) + ', ' + str(dy) + ' ' + str(dx) + ', ' + str(dy) },
                    '-|'   : {'d': 'm ' + frm['x'] + ',' + frm['y'] + ' ' + str(dx) + ',0 0,' + str(dy)},
                    '|-'   : {'d': 'm ' + frm['x'] + ',' + frm['y'] + ' 0,' + str(dy) + ' ' + str(dx) + ',0'},
                    '-|-'  : {'d': 'm ' + frm['x'] + ',' + frm['y'] + ' ' + str(dx / 2) + ',0 0,' + str(dy) + ' ' + str(dx / 2) + ',0'},
                    '->'   : {'style': 'marker-end:url(#arrowhead);stroke:#0041c4;stroke-width:1;fill:none'},
                    '~>'   : {'style': 'marker-end:url(#arrowhead);stroke:#0041c4;stroke-width:1;fill:none', 'd': 'M ' + frm['x'] + ',' + frm['y'] + ' ' + 'c ' + str(0.7 * dx) + ', 0 ' + str(0.3 * dx) + ', ' + str(dy) + ' ' + str(dx) + ', ' + str(dy)},
                    '-~>'  : {'style': 'marker-end:url(#arrowhead);stroke:#0041c4;stroke-width:1;fill:none', 'd': 'M ' + frm['x'] + ',' + frm['y'] + ' ' + 'c ' + str(0.7 * dx) + ', 0 ' +     str(dx) + ', ' + str(dy) + ' ' + str(dx) + ', ' + str(dy)},
                    '~->'  : {'style': 'marker-end:url(#arrowhead);stroke:#0041c4;stroke-width:1;fill:none', 'd': 'M ' + frm['x'] + ',' + frm['y'] + ' ' + 'c ' + '0'     + ', 0 ' + str(0.3 * dx) + ', ' + str(dy) + ' ' + str(dx) + ', ' + str(dy)},
                    '-|>'  : {'style': 'marker-end:url(#arrowhead);stroke:#0041c4;stroke-width:1;fill:none', 'd': 'm ' + frm['x'] + ',' + frm['y'] + ' ' + str(dx) + ',0 0,' + str(dy)},
                    '|->'  : {'style': 'marker-end:url(#arrowhead);stroke:#0041c4;stroke-width:1;fill:none', 'd': 'm ' + frm['x'] + ',' + frm['y'] + ' 0,' + str(dy) + ' ' + str(dx) + ',0'},
                    '-|->' : {'style': 'marker-end:url(#arrowhead);stroke:#0041c4;stroke-width:1;fill:none', 'd': 'm ' + frm['x'] + ',' + frm['y'] + ' ' + str(dx / 2) + ',0 0,' + str(dy) + ' ' + str(dx / 2) + ',0'},
                    '<->'  : {'style': 'marker-end:url(#arrowhead);marker-start:url(#arrowtail);stroke:#0041c4;stroke-width:1;fill:none'},
                    '<~>'  : {'style': 'marker-end:url(#arrowhead);marker-start:url(#arrowtail);stroke:#0041c4;stroke-width:1;fill:none','d': 'M ' + frm['x'] + ',' + frm['y'] + ' ' + 'c ' + str(0.7 * dx) + ', 0 ' + str(0.3 * dx) + ', ' + str(dy) + ' ' + str(dx) + ', ' + str(dy)},
                    '<-~>' : {'style': 'marker-end:url(#arrowhead);marker-start:url(#arrowtail);stroke:#0041c4;stroke-width:1;fill:none','d': 'M ' + frm['x'] + ',' + frm['y'] + ' ' + 'c ' + str(0.7 * dx) + ', 0 ' +     str(dx) + ', ' + str(dy) + ' ' + str(dx) + ', ' + str(dy)},
                    '<-|>' : {'style': 'marker-end:url(#arrowhead);marker-start:url(#arrowtail);stroke:#0041c4;stroke-width:1;fill:none','d': 'm ' + frm['x'] + ',' + frm['y'] + ' ' + str(dx) + ',0 0,' + str(dy)},
                    '<-|->': {'style': 'marker-end:url(#arrowhead);marker-start:url(#arrowtail);stroke:#0041c4;stroke-width:1;fill:none','d': 'm ' + frm['x'] + ',' + frm['y'] + ' ' + str(dx / 2) + ',0 0,' + str(dy) + ' ' + str(dx / 2) + ',0'}
                }
                gmark[1].update( pattern.get( Edge['shape'], { 'style': 'fill:none;stroke:#F00;stroke-width:1' } ) )
                
                if Edge['label']:
                    if Edge['shape'] == '-~' :
                         lx = float(frm['x']) + (float(to['x']) - float(frm['x'])) * 0.75
                    if Edge['shape'] == '~-' : 
                         lx = float(frm['x']) + (float(to['x']) - float(frm['x'])) * 0.25
                    if Edge['shape'] == '-|' :
                         lx = float(to['x'])
                    if Edge['shape'] == '|-' : 
                         lx = float(frm['x'])
                    if Edge['shape'] == '-~>': 
                         lx = float(frm['x']) + (float(to['x']) - float(frm['x'])) * 0.75
                    if Edge['shape'] == '~->': 
                         lx = float(frm['x']) + (float(to['x']) - float(frm['x'])) * 0.25
                    if Edge['shape'] == '-|>' : 
                         lx = float(to['x'])
                    if Edge['shape'] == '|->' : 
                         lx = float(frm['x'])
                    if Edge['shape'] == '<-~>': 
                         lx = float(frm['x']) + (float(to['x']) - float(frm['x'])) * 0.75
                    if Edge['shape'] =='<-|>' : 
                         lx = float(to['x'])

                    lwidth = len( Edge['label'] ) * font_width2
                    label = [
                        'text',
                        {
                            'style': 'font-size:10px;',
                            'text-anchor': 'middle',
                            'xml:space': 'preserve',
                            'x': int( lx ),
                            'y': int( ly + 3 )
                        },
                        [ 'tspan', Edge['label'] ]
                    ]
                    underlabel = [
                        'rect',
                        {
                            'height': 9,
                            'style': 'fill:#FFF;',
                            'width': lwidth,
                            'x': int( lx - lwidth / 2 ),
                            'y': int( ly - 5 )
                        }
                    ]
                    gg.append(underlabel)
                    gg.append(label)
         
        for k in Events: 
            if k.islower() :
                if Events[k]['x'] > 0 :
                    lwidth = len( k ) * font_width2
                    underlabel = [
                        'rect',
                        {
                            'x': float( Events[k]['x'] ) - float(lwidth) / 2,
                            'y': int( Events[k]['y'] ) - 4,
                            'height': 8,
                            'width': lwidth,
                            'style': 'fill:#FFF;'
                        }
                    ]
                    gg.append(underlabel)
                    label = [
                        'text',
                        {
                            'style': 'font-size:8px;',
                            'x': int( Events[k]['x'] ),
                            'y': int( Events[k]['y'] ) + 2,
                            'width': lwidth,
                            'text-anchor': 'middle'
                        },
                        k
                    ]
                    gg.append(label)

def parseConfig (source) :
        
    lane['hscale'] = 1
    if lane.get('hscale0') :
        lane['hscale'] = lane['hscale0']    

    if source and source.get('config') and source.get('config').get('hscale'):
        hscale = round(source.get('config').get('hscale'))
        if hscale > 0 :
            if hscale > 100 : hscale = 100
            lane['hscale'] = hscale
        
    lane['yh0'] = 0
    lane['yh1'] = 0    
    if source and source.get('head') :
        lane['head'] = source['head']
        if source.get('head').get('tick',0) == 0 : lane['yh0'] = 20 
        if source.get('head').get('tock',0) == 0 : lane['yh0'] = 20 
        if source.get('head').get('text') : lane['yh1'] = 46; lane['head']['text'] = source['head']['text'] 
    
    lane['yf0'] = 0
    lane['yf1'] = 0    
    if source and source.get('foot') :
        lane['foot'] = source['foot']
        if source.get('foot').get('tick',0) == 0 : lane['yf0'] = 20 
        if source.get('foot').get('tock',0) == 0 : lane['yf0'] = 20 
        if source.get('foot').get('text') : lane['yf1'] = 46; lane['foot']['text'] = source['foot']['text']

def rec (tmp, state) :

    name = ''
    delta_x = 10

    if type( tmp[0] ) is str or type( tmp[0] ) is unicode :
        name = tmp[0]
        delta_x = 25
     
    if type( tmp[0] ) is int :
        name = str( tmp[0] )
        delta_x = 25
    
    state['x'] += delta_x
    for i in range( len( tmp ) ) :
       if type( tmp[i] ) is list :
           old_y = state['y']
           rec( tmp[i], state )
           state['groups'].append( {'x':state['xx'], 'y':old_y, 'height':state['y'] - old_y, 'name': state['name'] } )
       elif type( tmp[i] ) is dict :
           state['lanes'].append(tmp[i])
           state['width'].append(state['x'])
           state['y'] += 1
    
    state['xx'] = state['x']
    state['x'] -= delta_x
    state['name'] = name

def insertSVGTemplate (index, parent, source) :
    
    if source.get('config') and source.get('config').get('skin') and source.get('config').get('skin').get('waveSkin') :
        e =  source.get('config').get('skin').get('waveSkin')   
    else :
        e = WaveSkin
    
    if index == 0 :
        lane['xs']     = int( e[3][1][2][1]['width'] )
        lane['ys']     = int( e[3][1][2][1]['height'] )
        lane['xlabel'] = int( e[3][1][2][1]['x'] )
        lane['ym']     = int( e[3][1][2][1]['y'] )
        
    else :
        e = ['svg', {'id': 'svg', 'xmlns': 'http://www.w3.org/2000/svg', 'xmlns:xlink': 'http://www.w3.org/1999/xlink', 'height': '0'},
            ['g', {'id': 'waves'},
                ['g', {'id': 'lanes'}],
                ['g', {'id': 'groups'}]
            ]
        ]

    e[-1][1]['id']    = 'waves_'      + str(index)
    e[-1][2][1]['id'] = 'lanes_'      + str(index)
    e[-1][3][1]['id'] = 'groups_'     + str(index)
    e[1]['id']        = 'svgcontent_' + str(index)
    e[1]['height']    = 0

    parent.extend(e)

def renderWaveForm (index, source, output) :
       
    xmax = 0
    root = []
    groups = []
    
    if source.get('signal'):
        insertSVGTemplate(index, output, source)
        parseConfig( source )
        ret = {'x':0, 'y':0, 'xmax':0, 'width':[], 'lanes':[], 'groups':[] }
        rec( source['signal'], ret )
        content  = parseWaveLanes(ret['lanes'])
        glengths = renderWaveLane(root, content, index)
        for i in range( len( glengths ) ):
            xmax = max(xmax, ( glengths[i] + ret['width'][i] ))
        renderMarks(root, content, index)
        renderArcs(root, ret['lanes'], index, source)
        renderGaps(root, ret['lanes'], index)
        renderGroups(groups, ret['groups'], index)
        lane['xg'] = int( math.ceil( ( xmax - lane['tgo']) / lane['xs'] ) * lane['xs'] )        
        width  = (lane['xg'] + lane['xs'] * (lane['xmax'] + 1) )
        height = len(content) * lane['yo'] + lane['yh0'] + lane['yh1'] + lane['yf0'] + lane['yf1']
        output[1]={
            'id'         :'svgcontent_' + str(index), 
            'xmlns'      :"http://www.w3.org/2000/svg", 
            'xmlns:xlink':"http://www.w3.org/1999/xlink", 
            'width'      :str(width), 
            'height'     :str(height), 
            'viewBox'    :'0 0 ' + str(width) + ' ' + str(height),            
            'overflow'   :"hidden"
        }
        output[-1][2][1]['transform']='translate(' + str(lane['xg'] + 0.5) + ', ' + str((float(lane['yh0']) + float(lane['yh1'])) + 0.5) + ')'
    
    output[-1][2].extend(root)
    output[-1][3].extend(groups)

def renderGroups (root, groups, index) :

    svgns = 'http://www.w3.org/2000/svg',
    xmlns = 'http://www.w3.org/XML/1998/namespace'

    for i in range( len( groups ) ) :
        group = [
                'path',
                {
                    'id':    'group_' + str(i) + '_' + str(index),
                    'd':     'm ' + str( groups[i]['x'] + 0.5 ) + ',' + str( groups[i]['y']* lane['yo'] + 3.5 + lane['yh0'] + lane['yh1'] ) + ' c -3,0 -5,2 -5,5 l 0,' + str( int( groups[i]['height'] * lane['yo'] - 16 ) ) + ' c 0,3 2,5 5,5',
                    'style': 'stroke:#0041c4;stroke-width:1;fill:none'
                }
            ]
        root.append(group)

        name = groups[i]['name']
        x = str( int( groups[i]['x'] - 10 ) )
        y = str( int( lane['yo'] * (groups[i]['y'] + (float(groups[i]['height']) / 2)) + lane['yh0'] + lane['yh1'] ) )
        label = [
           ['g', 
               {'transform': 'translate(' + x + ',' + y + ')'}, 
               ['g', {'transform': 'rotate(270)'}, 
                   'text',
                   {
                       'text-anchor': 'middle',
                       'class': 'info',
                       'xml:space' : 'preserve'
                   },
                   ['tspan',name]
               ]
          ]
        ]
        root.append(label)

def renderGaps (root, source, index) :

    Stack = []
    svgns   = 'http://www.w3.org/2000/svg',
    xlinkns = 'http://www.w3.org/1999/xlink'

    if source:

        gg = [
            'g',
            { 'id': 'wavegaps_' + str(index) }
        ]

        for i in range( len( source )):
            lane['period'] = source[i].get('period',1)
            lane['phase']  = int( source[i].get('phase',0 ) * 2 )

            g = [
                'g',
                {
                    'id': 'wavegap_' + str(i) + '_' + str(index),
                    'transform': 'translate(0,' + str(lane['y0'] + i * lane['yo']) + ')'
                }
            ]
            gg.append(g)

            if source[i].get('wave'):
                text = source[i]['wave']
                Stack = text
                pos = 0
                while len( Stack ) :
                    c = Stack [0]
                    Stack = Stack[1:]
                    if c == '|' :
                        b = [
                           'use',
                           {
                               'xmlns:xlink':xlinkns,
                               'xlink:href':'#gap',
                               'transform': 'translate(' + str(int(float(lane['xs']) * ((2 * pos + 1) * float(lane['period']) * float(lane['hscale']) - float(lane['phase'])))) + ')'
                           }
                        ]
                        g.append(b)
                    pos += 1

        root.append( gg )

def convert_to_svg( root ) :

    svg_output = ''

    if type( root ) is list: 
        if len(root) >= 2 and type( root[1] ) is dict:
           if len( root ) == 2 :
               svg_output += '<' + root[0] + convert_to_svg( root[1] ) + '/>\n'
           elif len( root ) >= 3 :
               svg_output += '<' + root[0] + convert_to_svg( root[1] ) + '>\n'
               if len( root ) == 3:
                   svg_output += convert_to_svg( root[2] )
               else:
                   svg_output += convert_to_svg( root[2:]  )
               svg_output += '</' + root[0] + '>\n'
        elif type( root[0] ) is list:
           for eleml in root: 
               svg_output += convert_to_svg( eleml )
        else:
           svg_output += '<' + root[0] + '>\n'
           for eleml in root[1:]: 
               svg_output += convert_to_svg( eleml )
           svg_output += '</' + root[0] + '>\n'
    elif type( root ) is dict:
        for elemd in root :
           svg_output += ' ' + elemd + '="' + str(root[elemd]) + '"'
    else:
        svg_output += root

    return svg_output

if __name__ == '__main__':

    if len( sys.argv ) != 5:
        print 'Usage : ' + sys.argv[0] + ' source <input.json> svg <output.svg>' 
        exit(1)
        
    if sys.argv[3] != 'svg' :
        print 'Error: only svg format supported.'
        exit(1)
    
    output=[]
    inputfile  = sys.argv[2]
    outputfile = sys.argv[4]
    with open(inputfile,'r') as f:
       jinput = json.load(f)
    renderWaveForm(0,jinput,output)
    svg_output = convert_to_svg(output)
    with open(outputfile,'w') as f:
       f.write( svg_output )
