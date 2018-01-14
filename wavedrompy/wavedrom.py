#!/usr/bin/python
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
from wavedrompy import waveskin
import argparse


class WaveDrom(object):
    font_width = 7

    lane = {
        "xs": 20,    # tmpgraphlane0.width
        "ys": 20,    # tmpgraphlane0.height
        "xg": 120,   # tmpgraphlane0.x
        "yg": 0,     # head gap
        "yh0": 0,     # head gap title
        "yh1": 0,     # head gap
        "yf0": 0,     # foot gap
        "yf1": 0,     # foot gap
        "y0": 5,     # tmpgraphlane0.y
        "yo": 30,    # tmpgraphlane1.y - y0
        "tgo": -10,   # tmptextlane0.x - xg
        "ym": 15,    # tmptextlane0.y - y0
        "xlabel": 6,     # tmptextlabel.x - xg
        "xmax": 1,
        "scale": 1,
        "head": {},
        "foot": {}
    }

    def __init__(self):
        return

    def genBrick(self, texts, extra, times):

        R = []
        if len(texts) == 4:
            for j in range(times):

                R.append(texts[0])

                for i in range(extra):
                    R.append(texts[1])

                R.append(texts[2])
                for i in range(extra):
                    R.append(texts[3])

            return R

        if len(texts) == 1:
            texts.append(texts[0])

        R.append(texts[0])
        for i in range(times * (2 * (extra + 1)) - 1):
            R.append(texts[1])
        return R

    def genFirstWaveBrick(self, text, extra, times):

        pattern = {
            "p": ["pclk", "111", "nclk", "000"],
            "n": ["nclk", "000", "pclk", "111"],
            "P": ["Pclk", "111", "nclk", "000"],
            "N": ["Nclk", "000", "pclk", "111"],
            "l": ["000"],
            "L": ["000"],
            "0": ["000"],
            "h": ["111"],
            "H": ["111"],
            "1": ["111"],
            "=": ["vvv-2"],
            "2": ["vvv-2"],
            "3": ["vvv-3"],
            "4": ["vvv-4"],
            "5": ["vvv-5"],
            "d": ["ddd"],
            "u": ["uuu"],
            "z": ["zzz"]
        }

        return self.genBrick(pattern.get(text,  ["xxx"]), extra, times)

    def genWaveBrick(self, text, extra, times):

        x1 = {"p": "pclk", "n": "nclk",
              "P": "Pclk", "N": "Nclk",
              "h": "pclk", "l": "nclk",
              "H": "Pclk", "L": "Nclk"}
        x2 = {"0": "0", "1": "1", "x": "x", "d": "d", "u": "u", "z": "z",
              "=": "v",  "2": "v",  "3": "v",  "4": "v",  "5": "v"}
        x3 = {"0": "", "1": "", "x": "", "d": "", "u": "", "z": "",
              "=": "-2", "2": "-2", "3": "-3", "4": "-4", "5": "-5"}
        y1 = {
            "p": "0", "n": "1",
            "P": "0", "N": "1",
            "h": "1", "l": "0",
            "H": "1", "L": "0",
            "0": "0", "1": "1",
            "x": "x", "d": "d", "u": "u", "z": "z",
            "=": "v", "2": "v", "3": "v", "4": "v", "5": "v"}

        y2 = {
            "p": "", "n": "",
            "P": "", "N": "",
            "h": "", "l": "",
            "H": "", "L": "",
            "0": "", "1": "",
            "x": "", "d": "", "u": "", "z": "",
            "=": "-2", "2": "-2", "3": "-3", "4": "-4", "5": "-5"}

        x4 = {
            "p": "111", "n": "000",
            "P": "111", "N": "000",
            "h": "111", "l": "000",
            "H": "111", "L": "000",
            "0": "000", "1": "111", "x": "xxx", "d": "ddd", "u": "uuu", "z": "zzz",
            "=": "vvv-2", "2": "vvv-2", "3": "vvv-3", "4": "vvv-4", "5": "vvv-5"}

        x5 = {"p": "nclk", "n": "pclk", "P": "nclk", "N": "pclk"}
        x6 = {"p": "000", "n": "111", "P": "000", "N": "111"}
        xclude = {"hp": "111", "Hp": "111", "ln": "000", "Ln": "000",
                  "nh": "111", "Nh": "111", "pl": "000", "Pl": "000"}

        # atext = text.split()
        atext = text

        tmp0 = x4.get(atext[1])
        tmp1 = x1.get(atext[1])
        if tmp1 is None:
            tmp2 = x2.get(atext[1])
            if tmp2 is None:
                # unknown
                return self.genBrick(["xxx"], extra, times)
            else:
                tmp3 = y1.get(atext[0])
                if tmp3 is None:
                    # unknown
                    return self.genBrick(["xxx"], extra, times)

                # soft curves
                return self.genBrick([tmp3 + "m" + tmp2 + y2[atext[0]] + x3[atext[1]], tmp0], extra, times)

        else:
            tmp4 = xclude.get(text)
            if tmp4 is not None:
                tmp1 = tmp4

            # sharp curves
            tmp2 = x5.get(atext[1])
            if tmp2 is None:
                # hlHL
                return self.genBrick([tmp1, tmp0], extra, times)
            else:
                # pnPN
                return self.genBrick([tmp1, tmp0, tmp2, x6[atext[1]]], extra, times)

    def parseWaveLane(self, text, extra):

        R = []
        Stack = text
        Next = Stack[0]
        Stack = Stack[1:]

        Repeats = 1
        while len(Stack) and (Stack[0] in [".", "|"]):  # repeaters parser
            Stack = Stack[1:]
            Repeats += 1

        R.extend(self.genFirstWaveBrick(Next, extra, Repeats))

        while len(Stack):
            Top = Next
            Next = Stack[0]
            Stack = Stack[1:]
            Repeats = 1
            while len(Stack) and (Stack[0] == "." or Stack[0] == "|"):  # repeaters parser
                Stack = Stack[1:]
                Repeats += 1
            R.extend(self.genWaveBrick((Top + Next), extra, Repeats))

        for i in range(self.lane["phase"]):
            R = R[1:]
        return R

    def parseWaveLanes(self, sig):

        def data_extract(e):
            tmp = e.get("data")
            if tmp is None:
                return None
            if self.is_type_str(tmp):
                tmp = tmp.split()
            return tmp

        content = []
        for sigx in sig:
            self.lane["period"] = sigx.get("period", 1)
            self.lane["phase"] = int(sigx.get("phase", 0) * 2)
            sub_content = []
            sub_content.append([sigx.get("name", " "), sigx.get("phase", 0)])
            sub_content.append(self.parseWaveLane(sigx["wave"], int(
                self.lane["period"] * self.lane["hscale"] - 1)) if sigx.get("wave") else None)
            sub_content.append(data_extract(sigx))
            content.append(sub_content)

        return content

    def findLaneMarkers(self, lanetext):

        lcount = 0
        gcount = 0
        ret = []
        for i in range(len(lanetext)):
            if lanetext[i] in ["vvv-2", "vvv-3", "vvv-4", "vvv-5"]:
                lcount += 1
            else:
                if lcount != 0:
                    ret.append(gcount - ((lcount + 1) / 2))
                    lcount = 0

            gcount += 1

        if lcount != 0:
            ret.append(gcount - ((lcount + 1) / 2))

        return ret

    def renderWaveLane(self, root, content, index):

        xmax = 0
        xgmax = 0
        glengths = []
        svgns = "http://www.w3.org/2000/svg"
        xlinkns = "http://www.w3.org/1999/xlink"
        xmlns = "http://www.w3.org/XML/1998/namespace"
        for j in range(len(content)):
            name = content[j][0][0]
            if name:  # check name
                g = [
                    "g",
                    {
                        "id": "_".join(["wavelane", str(j), str(index)]),
                        "transform": "".join(["translate(0,", str(self.lane["y0"] + j * self.lane["yo"]), ")"])
                    }
                ]
                root.append(g)
                title = [
                    "text",
                    {
                        "x": self.lane["tgo"],
                        "y": self.lane["ym"],
                        "class": "info",
                        "text-anchor": "end",
                        "xml:space": "preserve"
                    },
                    ["tspan", name]
                ]
                g.append(title)

                glengths.append(len(name) * self.font_width + self.font_width)

                xoffset = content[j][0][1]
                xoffset = math.ceil(2 * xoffset) - 2 * xoffset if xoffset > 0 else -2 * xoffset
                gg = [
                    "g",
                    {
                        "id": "_".join(["wavelane", "draw", str(j), str(index)]),
                        "transform": "".join(["translate(", str(xoffset * self.lane["xs"]), ", 0)"])
                    }
                ]
                g.append(gg)

                if content[j][1]:
                    for i in range(len(content[j][1])):
                        b = [
                            "use",
                            {
                                # "id": "use_" + str(i) + "_" + str(j) + "_" + str(index),
                                "xmlns:xlink": xlinkns,
                                "xlink:href": "#" + str(content[j][1][i]),
                                "transform": "translate(" + str(i * self.lane["xs"]) + ")"
                            }
                        ]
                        gg.append(b)

                    if content[j][2] and len(content[j][2]):
                        labels = self.findLaneMarkers(content[j][1])
                        if len(labels) != 0:
                            for k in range(len(labels)):
                                if content[j][2] and k < len(content[j][2]):
                                    title = [
                                        "text",
                                        {
                                            "x": int(labels[k]) * self.lane["xs"] + self.lane["xlabel"],
                                            "y": self.lane["ym"],
                                            "text-anchor": "middle",
                                            "xml:space": "preserve"
                                        },
                                        ["tspan", content[j][2][k]]
                                    ]
                                    gg.append(title)

                    if len(content[j][1]) > xmax:
                        xmax = len(content[j][1])

        self.lane["xmax"] = xmax
        self.lane["xg"] = xgmax + 20
        return glengths

    def renderMarks(self, root, content, index):

        def captext(g, cxt, anchor, y):

            if cxt.get(anchor) and cxt[anchor].get("text"):
                tmark = [
                    "text",
                    {
                        "x": float(cxt["xmax"]) * float(cxt["xs"]) / 2,
                        "y": y,
                        "text-anchor": "middle",
                        "fill": "#000",
                        "xml:space": "preserve"
                    }, cxt[anchor]["text"]
                ]
                g.append(tmark)

        def ticktock(g, cxt, ref1, ref2, x, dx, y, length):
            L = []

            if cxt.get(ref1) is None or cxt[ref1].get(ref2) is None:
                return

            val = cxt[ref1][ref2]
            if self.is_type_str(val):
                val = val.split()
            elif type(val) is int:
                offset = val
                val = []
                for i in range(length):
                    val.append(i + offset)

            if type(val) is list:
                if len(val) == 0:
                    return
                elif len(val) == 1:
                    offset = val[0]
                    if self.is_type_str(offset):
                        L = val
                    else:
                        for i in range(length):
                            L[i] = i + offset

                elif len(val) == 2:
                    offset = int(val[0])
                    step = int(val[1])
                    tmp = val[1].split(".")
                    if len(tmp) == 2:
                        dp = len(tmp[1])

                    if self.is_type_str(offset) or self.is_type_str(step):
                        L = val
                    else:
                        offset = step * offset
                        for i in range(length):
                            L[i] = "{0:.", dp, "f}".format(step * i + offset)

                else:
                    L = val

            else:
                return

            for i in range(length):
                tmp = L[i]
                tmark = [
                    "text",
                    {
                        "x": i * dx + x,
                        "y": y,
                        "text-anchor": "middle",
                        "class": "muted",
                        "xml:space": "preserve"
                    }, str(tmp)
                ]
                g.append(tmark)

        mstep = 2 * int(self.lane["hscale"])
        mmstep = mstep * self.lane["xs"]
        marks = int(self.lane["xmax"] / mstep)
        gy = len(content) * int(self.lane["yo"])

        g = ["g", {"id": "gmarks_" + str(index)}]
        root.insert(0, g)

        for i in range(marks + 1):
            gg = [
                "path",
                {
                    "id":    "gmark_" + str(i) + "_" + str(index),
                    "d":     "m " + str(i * mmstep) + "," + "0" + " 0," + str(gy),
                    "style": "stroke:#888;stroke-width:0.5;stroke-dasharray:1,3"
                }
            ]
            g.append(gg)

        captext(g, self.lane, "head", -33 if self.lane["yh0"] else -13)
        captext(g, self.lane, "foot", gy + (45 if self.lane["yf0"] else 25))

        ticktock(g, self.lane, "head", "tick",          0, mmstep,      -5, marks + 1)
        ticktock(g, self.lane, "head", "tock", mmstep / 2, mmstep,      -5, marks)
        ticktock(g, self.lane, "foot", "tick",          0, mmstep, gy + 15, marks + 1)
        ticktock(g, self.lane, "foot", "tock", mmstep / 2, mmstep, gy + 15, marks)

    def renderArcs(self, root, source, index, top):

        Stack = []
        Edge = {"words": [], "frm": 0, "shape": "", "to": 0, "label": ""}
        Events = {}
        svgns = "http://www.w3.org/2000/svg"
        xmlns = "http://www.w3.org/XML/1998/namespace"

        if source:
            for i in range(len(source)):
                self.lane["period"] = source[i].get("period", 1)
                self.lane["phase"] = int(source[i].get("phase", 0) * 2)
                text = source[i].get("node")
                if text:
                    Stack = text
                    pos = 0
                    while len(Stack):
                        eventname = Stack[0]
                        Stack = Stack[1:]
                        if eventname != ".":
                            Events[eventname] = {
                                "x": str(int(float(self.lane["xs"]) * (2 * pos * self.lane["period"] * self.lane["hscale"] - self.lane["phase"]) + float(self.lane["xlabel"]))),
                                "y": str(int(i * self.lane["yo"] + self.lane["y0"] + float(self.lane["ys"]) * 0.5))
                            }
                        pos += 1

            gg = ["g", {"id": "wavearcs_" + str(index)}]
            root.append(gg)

            if top.get("edge"):
                for i in range(len(top["edge"])):
                    Edge["words"] = top["edge"][i].split()
                    Edge["label"] = top["edge"][i][len(Edge["words"][0]):]
                    Edge["label"] = Edge["label"][1:]
                    Edge["frm"] = Edge["words"][0][0]
                    Edge["to"] = Edge["words"][0][-1]
                    Edge["shape"] = Edge["words"][0][1:-1]
                    frm = Events[Edge["frm"]]
                    to = Events[Edge["to"]]
                    gmark = [
                        "path",
                        {
                            "id": "gmark_" + Edge["frm"] + "_" + Edge["to"],
                            "d": "M " + frm["x"] + "," + frm["y"] + " " + to["x"] + "," + to["y"],
                            "style": "fill:none;stroke:#00F;stroke-width:1"
                        }
                    ]
                    gg.append(gmark)
                    dx = float(to["x"]) - float(frm["x"])
                    dy = float(to["y"]) - float(frm["y"])
                    lx = (float(frm["x"]) + float(to["x"])) / 2
                    ly = (float(frm["y"]) + float(to["y"])) / 2
                    pattern = {
                        "~": {"d": "M " + frm["x"] + "," + frm["y"] + " c " + str(0.7 * dx) + ", 0 " + str(0.3 * dx) + ", " + str(dy) + " " + str(dx) + ", " + str(dy)},
                        "-~": {"d": "M " + frm["x"] + "," + frm["y"] + " c " + str(0.7 * dx) + ", 0 " + str(dx) + ", " + str(dy) + " " + str(dx) + ", " + str(dy)},
                        "~-": {"d": "M " + frm["x"] + "," + frm["y"] + " c " + "0" + ", 0 " + str(0.3 * dx) + ", " + str(dy) + " " + str(dx) + ", " + str(dy)},
                        "-|": {"d": "m " + frm["x"] + "," + frm["y"] + " " + str(dx) + ",0 0," + str(dy)},
                        "|-": {"d": "m " + frm["x"] + "," + frm["y"] + " 0," + str(dy) + " " + str(dx) + ",0"},
                        "-|-": {"d": "m " + frm["x"] + "," + frm["y"] + " " + str(dx / 2) + ",0 0," + str(dy) + " " + str(dx / 2) + ",0"},
                        "->": {"style": "marker-end:url(#arrowhead);stroke:#0041c4;stroke-width:1;fill:none"},
                        "~>": {"style": "marker-end:url(#arrowhead);stroke:#0041c4;stroke-width:1;fill:none", "d": "M " + frm["x"] + "," + frm["y"] + " " + "c " + str(0.7 * dx) + ", 0 " + str(0.3 * dx) + ", " + str(dy) + " " + str(dx) + ", " + str(dy)},
                        "-~>": {"style": "marker-end:url(#arrowhead);stroke:#0041c4;stroke-width:1;fill:none", "d": "M " + frm["x"] + "," + frm["y"] + " " + "c " + str(0.7 * dx) + ", 0 " + str(dx) + ", " + str(dy) + " " + str(dx) + ", " + str(dy)},
                        "~->": {"style": "marker-end:url(#arrowhead);stroke:#0041c4;stroke-width:1;fill:none", "d": "M " + frm["x"] + "," + frm["y"] + " " + "c " + "0" + ", 0 " + str(0.3 * dx) + ", " + str(dy) + " " + str(dx) + ", " + str(dy)},
                        "-|>": {"style": "marker-end:url(#arrowhead);stroke:#0041c4;stroke-width:1;fill:none", "d": "m " + frm["x"] + "," + frm["y"] + " " + str(dx) + ",0 0," + str(dy)},
                        "|->": {"style": "marker-end:url(#arrowhead);stroke:#0041c4;stroke-width:1;fill:none", "d": "m " + frm["x"] + "," + frm["y"] + " 0," + str(dy) + " " + str(dx) + ",0"},
                        "-|->": {"style": "marker-end:url(#arrowhead);stroke:#0041c4;stroke-width:1;fill:none", "d": "m " + frm["x"] + "," + frm["y"] + " " + str(dx / 2) + ",0 0," + str(dy) + " " + str(dx / 2) + ",0"},
                        "<->": {"style": "marker-end:url(#arrowhead);marker-start:url(#arrowtail);stroke:#0041c4;stroke-width:1;fill:none"},
                        "<~>": {"style": "marker-end:url(#arrowhead);marker-start:url(#arrowtail);stroke:#0041c4;stroke-width:1;fill:none", "d": "M " + frm["x"] + "," + frm["y"] + " " + "c " + str(0.7 * dx) + ", 0 " + str(0.3 * dx) + ", " + str(dy) + " " + str(dx) + ", " + str(dy)},
                        "<-~>": {"style": "marker-end:url(#arrowhead);marker-start:url(#arrowtail);stroke:#0041c4;stroke-width:1;fill:none", "d": "M " + frm["x"] + "," + frm["y"] + " " + "c " + str(0.7 * dx) + ", 0 " + str(dx) + ", " + str(dy) + " " + str(dx) + ", " + str(dy)},
                        "<-|>": {"style": "marker-end:url(#arrowhead);marker-start:url(#arrowtail);stroke:#0041c4;stroke-width:1;fill:none", "d": "m " + frm["x"] + "," + frm["y"] + " " + str(dx) + ",0 0," + str(dy)},
                        "<-|->": {"style": "marker-end:url(#arrowhead);marker-start:url(#arrowtail);stroke:#0041c4;stroke-width:1;fill:none", "d": "m " + frm["x"] + "," + frm["y"] + " " + str(dx / 2) + ",0 0," + str(dy) + " " + str(dx / 2) + ",0"}
                    }
                    gmark[1].update(pattern.get(Edge["shape"], {"style": "fill:none;stroke:#00F;stroke-width:1"}))

                    if Edge["label"]:
                        if Edge["shape"] == "-~":
                            lx = float(frm["x"]) + (float(to["x"]) - float(frm["x"])) * 0.75
                        if Edge["shape"] == "~-":
                            lx = float(frm["x"]) + (float(to["x"]) - float(frm["x"])) * 0.25
                        if Edge["shape"] == "-|":
                            lx = float(to["x"])
                        if Edge["shape"] == "|-":
                            lx = float(frm["x"])
                        if Edge["shape"] == "-~>":
                            lx = float(frm["x"]) + (float(to["x"]) - float(frm["x"])) * 0.75
                        if Edge["shape"] == "~->":
                            lx = float(frm["x"]) + (float(to["x"]) - float(frm["x"])) * 0.25
                        if Edge["shape"] == "-|>":
                            lx = float(to["x"])
                        if Edge["shape"] == "|->":
                            lx = float(frm["x"])
                        if Edge["shape"] == "<-~>":
                            lx = float(frm["x"]) + (float(to["x"]) - float(frm["x"])) * 0.75
                        if Edge["shape"] == "<-|>":
                            lx = float(to["x"])

                        lwidth = len(Edge["label"]) * self.font_width
                        label = [
                            "text",
                            {
                                "style": "font-size:10px;",
                                "text-anchor": "middle",
                                "xml:space": "preserve",
                                "x": int(lx),
                                "y": int(ly + 3)
                            },
                            ["tspan", Edge["label"]]
                        ]
                        underlabel = [
                            "rect",
                            {
                                "height": 9,
                                "style": "fill:#FFF;",
                                "width": lwidth,
                                "x": int(lx - lwidth / 2),
                                "y": int(ly - 5)
                            }
                        ]
                        gg.append(underlabel)
                        gg.append(label)

            for k in Events:
                if k.islower():
                    if int(Events[k]["x"]) > 0:
                        lwidth = len(k) * self.font_width
                        underlabel = [
                            "rect",
                            {
                                "x": float(Events[k]["x"]) - float(lwidth) / 2,
                                "y": int(Events[k]["y"]) - 4,
                                "height": 8,
                                "width": lwidth,
                                "style": "fill:#FFF;"
                            }
                        ]
                        gg.append(underlabel)
                        label = [
                            "text",
                            {
                                "style": "font-size:8px;",
                                "x": int(Events[k]["x"]),
                                "y": int(Events[k]["y"]) + 2,
                                "width": lwidth,
                                "text-anchor": "middle"
                            },
                            k
                        ]
                        gg.append(label)

    def parseConfig(self, source):

        self.lane["hscale"] = 1
        if self.lane.get("hscale0"):
            self.lane["hscale"] = self.lane["hscale0"]

        if source and source.get("config") and source.get("config").get("hscale"):
            hscale = round(source.get("config").get("hscale"))
            if hscale > 0:
                if hscale > 100:
                    hscale = 100
                self.lane["hscale"] = hscale

        self.lane["yh0"] = 0
        self.lane["yh1"] = 0
        if source and source.get("head"):
            self.lane["head"] = source["head"]
            if source.get("head").get("tick", 0) == 0:
                self.lane["yh0"] = 20
            if source.get("head").get("tock", 0) == 0:
                self.lane["yh0"] = 20
            if source.get("head").get("text"):
                self.lane["yh1"] = 46
                self.lane["head"]["text"] = source["head"]["text"]

        self.lane["yf0"] = 0
        self.lane["yf1"] = 0
        if source and source.get("foot"):
            self.lane["foot"] = source["foot"]
            if source.get("foot").get("tick", 0) == 0:
                self.lane["yf0"] = 20
            if source.get("foot").get("tock", 0) == 0:
                self.lane["yf0"] = 20
            if source.get("foot").get("text"):
                self.lane["yf1"] = 46
                self.lane["foot"]["text"] = source["foot"]["text"]

    def rec(self, tmp, state):

        name = str(tmp[0])
        delta_x = 25

        state["x"] += delta_x
        for i in range(len(tmp)):
            if type(tmp[i]) is list:
                old_y = state["y"]
                self.rec(tmp[i], state)
                state["groups"].append({"x": state["xx"], "y": old_y, "height": state[
                                       "y"] - old_y, "name": state["name"]})
            elif type(tmp[i]) is dict:
                state["lanes"].append(tmp[i])
                state["width"].append(state["x"])
                state["y"] += 1

        state["xx"] = state["x"]
        state["x"] -= delta_x
        state["name"] = name

    def insertSVGTemplate(self, index, parent, source):

        e = waveskin.WaveSkin["default"]

        if source.get("config") and source.get("config").get("skin"):
            if waveskin.WaveSkin.get(source.get("config").get("skin")):
                e = waveskin.WaveSkin[source.get("config").get("skin")]

        if index == 0:
            self.lane["xs"] = int(e[3][1][2][1]["width"])
            self.lane["ys"] = int(e[3][1][2][1]["height"])
            self.lane["xlabel"] = int(e[3][1][2][1]["x"])
            self.lane["ym"] = int(e[3][1][2][1]["y"])

        else:
            e = ["svg", {"id": "svg", "xmlns": "http://www.w3.org/2000/svg", "xmlns:xlink": "http://www.w3.org/1999/xlink", "height": "0"},
                 ["g", {"id": "waves"},
                  ["g", {"id": "lanes"}],
                  ["g", {"id": "groups"}]
                  ]
                 ]

        e[-1][1]["id"] = "waves_" + str(index)
        e[-1][2][1]["id"] = "lanes_" + str(index)
        e[-1][3][1]["id"] = "groups_" + str(index)
        e[1]["id"] = "svgcontent_" + str(index)
        e[1]["height"] = 0

        parent.extend(e)

    def renderWaveForm(self, index, source, output):

        xmax = 0
        root = []
        groups = []

        if source.get("signal"):
            self.insertSVGTemplate(index, output, source)
            self.parseConfig(source)
            ret = {"x": 0, "y": 0, "xmax": 0, "width": [], "lanes": [], "groups": []}
            self.rec(source["signal"], ret)
            content = self.parseWaveLanes(ret["lanes"])
            glengths = self.renderWaveLane(root, content, index)
            for i in range(len(glengths)):
                xmax = max(xmax, (glengths[i] + ret["width"][i]))
            self.renderMarks(root, content, index)
            self.renderArcs(root, ret["lanes"], index, source)
            self.renderGaps(root, ret["lanes"], index)
            self.renderGroups(groups, ret["groups"], index)
            self.lane["xg"] = int(math.ceil(float(xmax - self.lane["tgo"]) / float(self.lane["xs"]))) * self.lane["xs"]
            width = (self.lane["xg"] + self.lane["xs"] * (self.lane["xmax"] + 1))
            height = len(content) * self.lane["yo"] + self.lane["yh0"] + \
                self.lane["yh1"] + self.lane["yf0"] + self.lane["yf1"]
            output[1] = {
                "id": "svgcontent_" + str(index),
                "xmlns": "http://www.w3.org/2000/svg",
                "xmlns:xlink": "http://www.w3.org/1999/xlink",
                "width": str(width),
                "height": str(height),
                "viewBox": "0 0 " + str(width) + " " + str(height),
                "overflow": "hidden"
            }
            output[-1][2][1]["transform"] = "translate(" + str(self.lane["xg"] + 0.5) + \
                ", " + str((float(self.lane["yh0"]) + float(self.lane["yh1"])) + 0.5) + ")"

        output[-1][2].extend(root)
        output[-1][3].extend(groups)

    def renderGroups(self, root, groups, index):

        svgns = "http://www.w3.org/2000/svg",
        xmlns = "http://www.w3.org/XML/1998/namespace"

        for i in range(len(groups)):
            group = [
                "path",
                {
                    "id":    "group_" + str(i) + "_" + str(index),
                    "d":     "m " + str(groups[i]["x"] + 0.5) + "," + str(groups[i]["y"] * self.lane["yo"] + 3.5 + self.lane["yh0"] + self.lane["yh1"]) + " c -3,0 -5,2 -5,5 l 0," + str(int(groups[i]["height"] * self.lane["yo"] - 16)) + " c 0,3 2,5 5,5",
                    "style": "stroke:#0041c4;stroke-width:1;fill:none"
                }
            ]
            root.append(group)

            name = groups[i]["name"]
            x = str(int(groups[i]["x"] - 10))
            y = str(int(self.lane["yo"] * (groups[i]["y"] + (float(groups[i]["height"]) / 2)) +
                        self.lane["yh0"] + self.lane["yh1"]))
            label = [
                ["g",
                 {"transform": "translate(" + x + "," + y + ")"},
                 ["g", {"transform": "rotate(270)"},
                  "text",
                  {
                     "text-anchor": "middle",
                     "class": "info",
                     "xml:space": "preserve"
                 },
                     ["tspan", name]
                 ]
                 ]
            ]
            root.append(label)

    def renderGaps(self, root, source, index):

        Stack = []
        svgns = "http://www.w3.org/2000/svg",
        xlinkns = "http://www.w3.org/1999/xlink"

        if source:

            gg = [
                "g",
                {"id": "wavegaps_" + str(index)}
            ]

            for i in range(len(source)):
                self.lane["period"] = source[i].get("period", 1)
                self.lane["phase"] = int(source[i].get("phase", 0) * 2)

                g = [
                    "g",
                    {
                        "id": "wavegap_" + str(i) + "_" + str(index),
                        "transform": "translate(0," + str(self.lane["y0"] + i * self.lane["yo"]) + ")"
                    }
                ]
                gg.append(g)

                if source[i].get("wave"):
                    text = source[i]["wave"]
                    Stack = text
                    pos = 0
                    while len(Stack):
                        c = Stack[0]
                        Stack = Stack[1:]
                        if c == "|":
                            b = [
                                "use",
                                {
                                    "xmlns:xlink": xlinkns,
                                    "xlink:href": "#gap",
                                    "transform": "translate(" + str(int(float(self.lane["xs"]) * ((2 * pos + 1) * float(self.lane["period"]) * float(self.lane["hscale"]) - float(self.lane["phase"])))) + ")"
                                }
                            ]
                            g.append(b)
                        pos += 1

            root.append(gg)

    def is_type_str(self, var):
        if sys.version_info[0] < 3:
            return type(var) is str or type(var) is unicode
        else:
            return type(var) is str

    def convert_to_svg(self, root):

        svg_output = ""

        if type(root) is list:
            if len(root) >= 2 and type(root[1]) is dict:
                if len(root) == 2:
                    svg_output += "<" + root[0] + self.convert_to_svg(root[1]) + "/>\n"
                elif len(root) >= 3:
                    svg_output += "<" + root[0] + self.convert_to_svg(root[1]) + ">\n"
                    if len(root) == 3:
                        svg_output += self.convert_to_svg(root[2])
                    else:
                        svg_output += self.convert_to_svg(root[2:])
                    svg_output += "</" + root[0] + ">\n"
            elif type(root[0]) is list:
                for eleml in root:
                    svg_output += self.convert_to_svg(eleml)
            else:
                svg_output += "<" + root[0] + ">\n"
                for eleml in root[1:]:
                    svg_output += self.convert_to_svg(eleml)
                svg_output += "</" + root[0] + ">\n"
        elif type(root) is dict:
            for elemd in root:
                svg_output += " " + elemd + "=\"" + str(root[elemd]) + "\""
        else:
            svg_output += root

        return svg_output


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--input", "-i", help="<input wavedrom source filename>")
    # parser.add_argument("--png", "-p", help="<output PNG image file name>")
    # parser.add_argument("--pdf", "-P", help="<output PDF file name>")
    parser.add_argument("--svg", "-s", help="<output SVG image file name>")
    args = parser.parse_args()

    output = []
    inputfile = args.input
    outputfile = args.svg

    wavedrom = WaveDrom()
    if not inputfile or not outputfile:
        parser.print_help()
    else:
        with open(inputfile, "r") as f:
            jinput = json.load(f)

        wavedrom.renderWaveForm(0, jinput, output)
        svg_output = wavedrom.convert_to_svg(output)

        with open(outputfile, "w") as f:
            f.write(svg_output)


if __name__ == "__main__":
    main()