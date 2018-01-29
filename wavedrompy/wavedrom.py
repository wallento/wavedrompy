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
from wavedrompy import waveskin, css
import argparse
from attrdict import AttrDict
import svgwrite


class WaveDrom(object):

    container = AttrDict({
        "defs": svgwrite.container.Defs,
        "g": svgwrite.container.Group,
        "marker": svgwrite.container.Marker,
        "use": svgwrite.container.Use,
    })
    element = AttrDict({
        "rect": svgwrite.shapes.Rect,
        "path": svgwrite.path.Path,
        "text": svgwrite.text.Text,
        "tspan": svgwrite.text.TSpan,
    })

    def __init__(self):

        self.font_width = 7
        self.lane = AttrDict({
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
        })

    def genBrick(self, texts="", extra="", times=""):

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

    def genFirstWaveBrick(self, text="", extra="", times=""):

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

    def genWaveBrick(self, text="", extra="", times=""):

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

    def parseWaveLane(self, text="", extra=""):

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
            while len(Stack) and (Stack[0] in [".", "|"]):  # repeaters parser
                Stack = Stack[1:]
                Repeats += 1
            R.extend(self.genWaveBrick((Top + Next), extra, Repeats))

        for i in range(self.lane.phase):
            R = R[1:]
        return R

    def parseWaveLanes(self, sig=""):

        def data_extract(e):
            tmp = e.get("data")
            if tmp is not None:
                tmp = tmp.split() if self.is_type_str(tmp) else tmp
            return tmp

        content = []
        for sigx in sig:
            self.lane.period = sigx.get("period", 1)
            self.lane.phase = int(sigx.get("phase", 0) * 2)
            sub_content = []
            sub_content.append([sigx.get("name", " "), sigx.get("phase", 0)])
            if sigx.get("wave"):
                sub_content.append(self.parseWaveLane(sigx["wave"], int(self.lane.period * self.lane.hscale - 1)))
            else:
                sub_content.append(None)
            sub_content.append(data_extract(sigx))
            content.append(sub_content)

        return content

    def findLaneMarkers(self, lanetext=""):

        lcount = 0
        gcount = 0
        ret = []
        for idx, val in enumerate(lanetext):
            if val in ["vvv-2", "vvv-3", "vvv-4", "vvv-5"]:
                lcount += 1
            else:
                if lcount != 0:
                    ret.append(gcount - ((lcount + 1) / 2))
                    lcount = 0

            gcount += 1

        if lcount != 0:
            ret.append(gcount - ((lcount + 1) / 2))

        return ret

    def renderWaveLane(self, root=[], content="", index=0):
        """
        root=[]

        """
        xmax = 0
        xgmax = 0
        glengths = []
        svgns = "http://www.w3.org/2000/svg"
        xlinkns = "http://www.w3.org/1999/xlink"
        xmlns = "http://www.w3.org/XML/1998/namespace"
        for j, val in enumerate(content):
            name = val[0][0]
            if name:  # check name
                dy = self.lane.y0 + j * self.lane.yo
                g = self.container.g(id="wavelane_{j}_{index}".format(j=j, index=index))
                g.translate(0, dy)
                # g = [
                #     "g",
                #     {
                #         # "id": "_".join(["wavelane", str(j), str(index)]),
                #         # "transform": "".join(["translate(0,", str(self.lane.y0 + j * self.lane.yo), ")"])
                #         "id": "wavelane_{j}_{index}".format(j=j, index=index),
                #         "transform": "translate(0,{dy})".format(dy=dy),
                #     }
                # ]
                # root.append(g)
                title = self.element.text("", x=[self.lane.tgo], y=[self.lane.ym], text_anchor="end")
                title.add(self.element.tspan(name))
                title["xml:space"] = "preserve"
                title["class"] = "info"
                # title = [
                #     "text",
                #     {
                #         "x": self.lane.tgo,
                #         "y": self.lane.ym,
                #         "class": "info",
                #         "text-anchor": "end",
                #         "xml:space": "preserve"
                #     },
                #     ["tspan", name]
                # ]
                # g.append(title)
                g.add(title)

                glengths.append(len(name) * self.font_width + self.font_width)

                xoffset = val[0][1]
                xoffset = math.ceil(2 * xoffset) - 2 * xoffset if xoffset > 0 else -2 * xoffset
                gg = self.container.g(id="wavelane_draw_{j}_{index}".format(j=j, index=index))
                gg.translate(xoffset * self.lane.xs, 0)
                # gg = [
                #     "g",
                #     {
                #         "id": "wavelane_draw_{j}_{index}".format(j=j, index=index),
                #         "transform": "translate({x},0)".format(x=xoffset * self.lane.xs)
                #     }
                # ]
                # g.append(gg)

                if val[1]:
                    for i in range(len(val[1])):
                        b = self.container.use(href="#{}".format(val[1][i]))
                        b.translate(i * self.lane.xs)
                        # b = [
                        #     "use",
                        #     {
                        #         # "id": "use_" + str(i) + "_" + str(j) + "_" + str(index),
                        #         "xmlns:xlink": xlinkns,
                        #         "xlink:href": "#{}".format(val[1][i]),
                        #         "transform": "translate({})".format(i * self.lane.xs)
                        #     }
                        # ]
                        # gg.append(b)
                        gg.add(b)

                    if val[2] and len(val[2]):
                        labels = self.findLaneMarkers(val[1])
                        if len(labels) != 0:
                            for k in range(len(labels)):
                                if val[2] and k < len(val[2]):
                                    tx = int(labels[k]) * self.lane.xs + self.lane.xlabel
                                    title = self.element.text("", x=[tx], y=[self.lane.ym], text_anchor="middle")
                                    title.add(self.element.tspan(val[2][k]))
                                    title["xml:space"] = "preserve"
                                    # title = [
                                    #     "text",
                                    #     {
                                    #         "x": int(labels[k]) * self.lane.xs + self.lane.xlabel,
                                    #         "y": self.lane.ym,
                                    #         "text-anchor": "middle",
                                    #         "xml:space": "preserve"
                                    #     },
                                    #     ["tspan", val[2][k]]
                                    # ]
                                    # gg.append(title)
                                    gg.add(title)

                    if len(val[1]) > xmax:
                        xmax = len(val[1])
                g.add(gg)
                root.add(g)
        self.lane.xmax = xmax
        self.lane.xg = xgmax + 20
        return glengths

    def renderMarks(self, root=[], content="", index=0):

        def get_elem(e):
            if len(e) == 3:
                ret = self.element[e[0]](e[2])
                ret.attribs = e[1]
            elif len(e) == 2:
                ret = self.element[e[0]](e[1])
            else:
                ret = self.element.tspan(e)
            return ret

        def captext(g, cxt, anchor, y):

            if cxt.get(anchor) and cxt[anchor].get("text"):
                tmark = self.element.text("", x=[float(cxt.xmax) * float(cxt.xs) / 2],
                                          y=[y], text_anchor="middle", fill="#000")
                tmark["xml:space"] = "preserve"
                [tmark.add(get_elem(e)) for e in cxt[anchor]["text"][1:]]
                # print(cxt[anchor]["text"])  # list
                # cxt[anchor]["text"] = ["tspan",  # [0
                #                        ["tspan", {"class": "error h1"}, "error"],  # [1] case 1
                #                        ["tspan", "E=mc"],  # [2] case 2
                #                        "default",  # [3] case 3
                #                        ]
                # tmark = [
                #     "text",
                #     {
                #         "x": float(cxt.xmax) * float(cxt.xs) / 2,
                #         "y": y,
                #         "text-anchor": "middle",
                #         "fill": "#000",
                #         "xml:space": "preserve"
                #     }, cxt[anchor]["text"]
                # ]
                # g.append(tmark)
                g.add(tmark)

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
                tmark = self.element.text("", x=[i * dx + x], y=[y], text_anchor="middle")
                tmark["class"] = "muted"
                tmark["xml:space"] = "preserve"
                # tmark = [
                #     "text",
                #     {
                #         "x": i * dx + x,
                #         "y": y,
                #         "text-anchor": "middle",
                #         "class": "muted",
                #         "xml:space": "preserve"
                #     }, str(tmp)
                # ]
                # g.append(tmark)
                g.add(tmark)

        mstep = 2 * int(self.lane.hscale)
        mmstep = mstep * self.lane.xs
        marks = int(self.lane.xmax / mstep)
        gy = len(content) * int(self.lane.yo)

        # g = ["g", {"id": "gmarks_{}".format(index)}]
        g = self.container.g(id="gmarks_{}".format(index))
        root.add(g)
        # root.insert(0, g)

        for i in range(marks + 1):
            gg = self.element.path(id="gmark_{i}_{index}".format(i=i, index=index),
                                   d="m {dx},0 0,{gy}".format(dx=i * mmstep, gy=gy),
                                   style="stroke:#888;stroke-width:0.5;stroke-dasharray:1,3")
            # gg = [
            #     "path",
            #     {
            #         "id":    "gmark_{i}_{index}".format(i=i, index=index),
            #         "d":     "m {dx},0 0,{gy}".format(dx=i * mmstep, gy=gy),
            #         "style": "stroke:#888;stroke-width:0.5;stroke-dasharray:1,3"
            #     }
            # ]
            # g.append(gg)
            g.add(gg)

        captext(g, self.lane, "head", -33 if self.lane.yh0 else -13)
        captext(g, self.lane, "foot", gy + (45 if self.lane.yf0 else 25))
        ticktock(g, self.lane, "head", "tick",          0, mmstep,      -5, marks + 1)
        ticktock(g, self.lane, "head", "tock", mmstep / 2, mmstep,      -5, marks)
        ticktock(g, self.lane, "foot", "tick",          0, mmstep, gy + 15, marks + 1)
        ticktock(g, self.lane, "foot", "tock", mmstep / 2, mmstep, gy + 15, marks)
        return g

    def renderArcs(self, root, source, index, top):

        Stack = []
        Edge = AttrDict({"words": [], "frm": 0, "shape": "", "to": 0, "label": ""})
        Events = AttrDict({})
        svgns = "http://www.w3.org/2000/svg"
        xmlns = "http://www.w3.org/XML/1998/namespace"

        if source:
            for idx, val in enumerate(source):
                self.lane.period = val.get("period", 1)
                self.lane.phase = int(val.get("phase", 0) * 2)
                text = val.get("node")
                if text:
                    Stack = text
                    pos = 0
                    while len(Stack):
                        eventname = Stack[0]
                        Stack = Stack[1:]
                        x = int(float(self.lane.xs) * (2 * pos * self.lane.period *
                                                       self.lane.hscale - self.lane.phase) + float(self.lane.xlabel))
                        y = int(idx * self.lane.yo + self.lane.y0 + float(self.lane.ys) * 0.5)
                        if eventname != ".":
                            Events[eventname] = AttrDict({"x": str(x), "y": str(y)})
                        pos += 1

            # gg = ["g", {"id": "wavearcs_{index}".format(index=index)}]
            gg = self.container.g(id="wavearcs_{index}".format(index=index))
            # root.append(gg)

            const_style = AttrDict({
                "a": "marker-end:url(#arrowhead);stroke:#0041c4;stroke-width:1;fill:none",
                "b": "marker-end:url(#arrowhead);marker-start:url(#arrowtail);stroke:#0041c4;stroke-width:1;fill:none"
            })
            if top.get("edge"):
                for i, val in enumerate(top["edge"]):
                    Edge.words = val.split()
                    Edge.label = val[len(Edge.words[0]):]
                    Edge.label = Edge.label[1:]
                    Edge.frm = Edge.words[0][0]
                    Edge.to = Edge.words[0][-1]
                    Edge.shape = Edge.words[0][1:-1]
                    frm = AttrDict(Events[Edge.frm])
                    to = AttrDict(Events[Edge.to])
                    # gmark = [
                    #     "path",
                    #     {
                    #         "id": "gmark_{frm}_{to}".format(frm=Edge.frm, to=Edge.to),
                    #         "d": "M {fx},{fy} {tx},{ty}".format(fx=frm.x, fy=frm.y, tx=to.x, ty=to.y),
                    #         "style": "fill:none;stroke:#00F;stroke-width:1"
                    #     }
                    # ]
                    # gg.append(gmark)
                    dx = float(to.x) - float(frm.x)
                    dy = float(to.y) - float(frm.y)
                    lx = (float(frm.x) + float(to.x)) / 2
                    ly = (float(frm.y) + float(to.y)) / 2
                    pattern = {
                        "~": {"d": "M {fx},{fy} c {dx},{dy} {dxx},{dyy} {dxxx},{dyyy}".format(fx=frm.x, fy=frm.y,
                                                                                              dx=(0.7 * dx), dy=0,
                                                                                              dxx=(0.3 * dx), dyy=dy,
                                                                                              dxxx=dx, dyyy=dy)},
                        "-~": {"d": "M {fx},{fy} c {dx},{dy} {dxx},{dyy} {dxxx},{dyyy}".format(fx=frm.x, fy=frm.y,
                                                                                               dx=(0.7 * dx), dy=0,
                                                                                               dxx=dx, dyy=dy,
                                                                                               dxxx=dx, dyyy=dy)},
                        "~-": {"d": "M {fx},{fy} c {dx},{dy} {dxx},{dyy} {dxxx},{dyyy}".format(fx=frm.x, fy=frm.y,
                                                                                               dx=0, dy=0,
                                                                                               dxx=(0.3 * dx), dyy=dy,
                                                                                               dxxx=dx, dyyy=dy)},
                        "-|": {"d": "m {fx},{fy} {dx},{dy} {dxx},{dyy}".format(fx=frm.x, fy=frm.y,
                                                                               dx=dx, dy=0,
                                                                               dxx=0, dyy=dy)},
                        "|-": {"d": "m {fx},{fy} {dx},{dy} {dxx},{dyy}".format(fx=frm.x, fy=frm.y,
                                                                               dx=0, dy=dy,
                                                                               dxx=dx, dyy=0)},
                        "-|-": {"d": "m {fx},{fy} {dx},{dy} {dxx},{dyy} {dxxx},{dyyy}".format(fx=frm.x, fy=frm.y,
                                                                                              dx=(dx / 2), dy=0,
                                                                                              dxx=0, dyy=dy,
                                                                                              dxxx=(dx / 2), dyyy=0)},
                        "->": {"style": const_style.a},
                        "~>": {"style": const_style.a,
                               "d": "M {fx},{fy} c {dx},{dy} {dxx},{dyy} {dxxx},{dyyy}".format(fx=frm.x, fy=frm.y,
                                                                                               dx=(0.7 * dx), dy=0,
                                                                                               dxx=(0.3 * dx), dyy=dy,
                                                                                               dxxx=dx, dyyy=dy)},
                        "-~>": {"style": const_style.a,
                                "d": "M {fx},{fy} c {dx},{dy} {dxx},{dyy} {dxxx},{dyyy}".format(fx=frm.x, fy=frm.y,
                                                                                                dx=(0.7 * dx), dy=0,
                                                                                                dxx=dx, dyy=dy,
                                                                                                dxxx=dx, dyyy=dy)},
                        "~->": {"style": const_style.a,
                                "d": "M {fx},{fy} c {dx},{dy} {dxx},{dyy} {dxxx},{dyyy}".format(fx=frm.x, fy=frm.y,
                                                                                                dx=0, dy=0,
                                                                                                dxx=(0.3 * dx), dyy=dy,
                                                                                                dxxx=dx, dyyy=dy)},
                        "-|>": {"style": const_style.a,
                                "d": "m {fx},{fy} {dx},{dy} {dxx},{dyy}".format(fx=frm.x, fy=frm.y,
                                                                                dx=dx, dy=0,
                                                                                dxx=0, dyy=dy)},
                        "|->": {"style": const_style.a,
                                "d": "m {fx},{fy} {dx},{dy} {dxx},{dyy}".format(fx=frm.x, fy=frm.y,
                                                                                dx=0, dy=dy,
                                                                                dxx=dx, dyy=0
                                                                                )},
                        "-|->": {"style": const_style.a,
                                 "d": "m {fx},{fy} {dx},{dy} {dxx},{dyy} {dxxx},{dyyy}".format(fx=frm.x, fy=frm.y,
                                                                                               dx=(dx / 2), dy=0,
                                                                                               dxx=0, dyy=dy,
                                                                                               dxxx=(dx / 2), dyyy=0
                                                                                               )},
                        "<->": {"style": const_style.b},
                        "<~>": {"style": const_style.b,
                                "d": "M {fx},{fy} c {dx},{dy} {dxx},{dyy} {dxxx},{dyyy}".format(fx=frm.x, fy=frm.y,
                                                                                                dx=(0.7 * dx), dy=0,
                                                                                                dxx=(0.3 * dx), dyy=dy,
                                                                                                dxxx=dx, dyyy=dy
                                                                                                )},
                        "<-~>": {"style": const_style.b,
                                 "d": "M {fx},{fy} c {dx},{dy} {dxx},{dyy} {dxxx},{dyyy}".format(fx=frm.x, fy=frm.y,
                                                                                                 dx=(0.7 * dx), dy=0,
                                                                                                 dxx=dx, dyy=dy,
                                                                                                 dxxx=dx, dyyy=dy
                                                                                                 )},
                        "<-|>": {"style": const_style.b,
                                 "d": "m {fx},{fy} {dx},{dy} {dxx},{dyy}".format(fx=frm.x, fy=frm.y,
                                                                                 dx=dx, dy=0,
                                                                                 dxx=0, dyy=dy
                                                                                 )},
                        "<-|->": {"style": const_style.b,
                                  "d": "m {fx},{fy} {dx},{dy} {dxx},{dyy} {dxxx},{dyyy}".format(fx=frm.x, fy=frm.y,
                                                                                                dx=(dx / 2), dy=0,
                                                                                                dxx=0, dyy=dy,
                                                                                                dxxx=(dx / 2), dyyy=0,
                                                                                                )}
                    }
                    pat = pattern.get(Edge.shape, {"style": "fill:none;stroke:#00F;stroke-width:1",
                                                   "d": "M {fx},{fy} {tx},{ty}".format(fx=frm.x, fy=frm.y,
                                                                                       tx=to.x, ty=to.y)
                                                   })
                    # gmark[1].update(pat)
                    gmark = self.element.path(id="gmark_{frm}_{to}".format(frm=Edge.frm, to=Edge.to),
                                              d=pat.get("d", "M {fx},{fy} {tx},{ty}".format(fx=frm.x, fy=frm.y,
                                                                                            tx=to.x, ty=to.y)),
                                              style=pat.get("style", "fill:none;stroke:#00F;stroke-width:1"))
                    gg.add(gmark)

                    if Edge.label:
                        if Edge.shape in ["-~", "-~>", "<-~>"]:
                            lx = float(frm.x) + (float(to.x) - float(frm.x)) * 0.75
                        elif Edge.shape in ["~-", "~->"]:
                            lx = float(frm.x) + (float(to.x) - float(frm.x)) * 0.25
                        elif Edge.shape in ["-|", "-|>", "<-|>"]:
                            lx = float(to.x)
                        elif Edge.shape in ["|-", "|->"]:
                            lx = float(frm.x)
                        # if Edge.shape == "-~":
                        #     lx = float(frm.x) + (float(to.x) - float(frm.x)) * 0.75
                        # if Edge.shape == "-~>":
                        #     lx = float(frm.x) + (float(to.x) - float(frm.x)) * 0.75
                        # if Edge.shape == "<-~>":
                        #     lx = float(frm.x) + (float(to.x) - float(frm.x)) * 0.75
                        # if Edge.shape == "~-":
                        #     lx = float(frm.x) + (float(to.x) - float(frm.x)) * 0.25
                        # if Edge.shape == "~->":
                        #     lx = float(frm.x) + (float(to.x) - float(frm.x)) * 0.25
                        # if Edge.shape == "-|":
                        #     lx = float(to.x)
                        # if Edge.shape == "-|>":
                        #     lx = float(to.x)
                        # if Edge.shape == "<-|>":
                        #     lx = float(to.x)
                        # if Edge.shape == "|-":
                        #     lx = float(frm.x)
                        # if Edge.shape == "|->":
                        #     lx = float(frm.x)

                        lwidth = len(Edge.label) * self.font_width
                        label = self.element.text("", style="font-size:10px;", text_anchor="middle",
                                                  x=[int(lx)], y=[int(ly + 3)])
                        label.add(self.element.tspan(Edge.label))
                        # label = [
                        #     "text",
                        #     {
                        #         "style": "font-size:10px;",
                        #         "text-anchor": "middle",
                        #         "xml:space": "preserve",
                        #         "x": int(lx),
                        #         "y": int(ly + 3)
                        #     },
                        #     ["tspan", Edge.label]
                        # ]
                        underlabel = self.element.rect(insert=(int(lx - lwidth / 2), int(ly - 5)),
                                                       size=(lwidth, 9), style="fill:#FFF;")
                        # underlabel = [
                        #     "rect",
                        #     {
                        #         "height": 9,
                        #         "style": "fill:#FFF;",
                        #         "width": lwidth,
                        #         "x": int(lx - lwidth / 2),
                        #         "y": int(ly - 5)
                        #     }
                        # ]
                        # gg.append(underlabel)
                        # gg.append(label)
                        gg.add(underlabel)
                        gg.add(label)

            for k in Events:
                if k.islower():
                    if int(Events[k].x) > 0:
                        lwidth = len(k) * self.font_width
                        lx = float(Events[k].x) - float(lwidth) / 2
                        ly = int(Events[k].y) - 4
                        underlabel = self.element.rect(insert=(lx, ly),
                                                       size=(lwidth, 8), style="fill:#FFF;")
                        # underlabel = [
                        #     "rect",
                        #     {
                        #         "x": lx,
                        #         "y": ly,
                        #         "height": 8,
                        #         "width": lwidth,
                        #         "style": "fill:#FFF;"
                        #     }
                        # ]
                        # gg.append(underlabel)
                        gg.add(underlabel)
                        lx = int(Events[k].x)
                        ly = int(Events[k].y) + 2
                        label = self.element.text(k, style="font-size:8px;", text_anchor="middle",
                                                  x=[lx], y=[ly])
                        # label = [
                        #     "text",
                        #     {
                        #         "style": "font-size:8px;",
                        #         "x": lx,
                        #         "y": ly,
                        #         # "width": lwidth,
                        #         "text-anchor": "middle"
                        #     },
                        #     k
                        # ]
                        # gg.append(label)
                        gg.add(label)
            root.add(gg)
            # return root

    def parseConfig(self, source={}):
        """
        source = AttrDict()
        """

        self.lane.hscale = 1
        if self.lane.get("hscale0"):
            self.lane.hscale = self.lane.hscale0

        if source and source.get("config") and source.get("config").get("hscale"):
            hscale = round(source.get("config").get("hscale"))
            if hscale > 0:
                if hscale > 100:
                    hscale = 100
                self.lane.hscale = hscale

        self.lane.yh0 = 0
        self.lane.yh1 = 0
        if source and source.get("head"):
            self.lane.head = source["head"]
            if source.get("head").get("tick", 0) == 0:
                self.lane.yh0 = 20
            if source.get("head").get("tock", 0) == 0:
                self.lane.yh0 = 20
            if source.get("head").get("text"):
                self.lane.yh1 = 46
                self.lane.head["text"] = source["head"]["text"]

        self.lane.yf0 = 0
        self.lane.yf1 = 0
        if source and source.get("foot"):
            self.lane.foot = source["foot"]
            if source.get("foot").get("tick", 0) == 0:
                self.lane.yf0 = 20
            if source.get("foot").get("tock", 0) == 0:
                self.lane.yf0 = 20
            if source.get("foot").get("text"):
                self.lane.yf1 = 46
                self.lane.foot["text"] = source["foot"]["text"]

    def rec(self, tmp=[], state={}):
        """
        tmp = source["signal"] = []
        state = AttrDict({"x": 0, "y": 0, "xmax": 0, "width": [], "lanes": [], "groups": []})
        [
          {    "name": "clk",   "wave": "p..Pp..P"},
          ["Master",
            ["ctrl",
              {"name": "write", "wave": "01.0...."},
              {"name": "read",  "wave": "0...1..0"}
            ],
            {  "name": "addr",  "wave": "x3.x4..x", "data": "A1 A2"},
            {  "name": "wdata", "wave": "x3.x....", "data": "D1"   }
          ],
          {},
          ["Slave",
            ["ctrl",
              {"name": "ack",   "wave": "x01x0.1x"}
            ],
            {  "name": "rdata", "wave": "x.....4x", "data": "Q2"}
          ]
        ]
        """

        name = str(tmp[0])
        delta_x = 25

        state.x += delta_x
        for idx, val in enumerate(tmp):
            if type(val) is list:
                old_y = state.y
                self.rec(val, state)
                state["groups"].append({"x": state.xx,
                                        "y": old_y,
                                        "height": state.y - old_y,
                                        "name": state.name})
            elif type(val) is dict:
                state["lanes"].append(val)
                state["width"].append(state.x)
                state.y += 1

        state.xx = state.x
        state.x -= delta_x
        state.name = name

    def anotherTemplate(self, index, source):
        def get_container(elem):
            """
            elem = [
            "g",   # elem[0]
            {"id": "socket"},   # elem[1]
            [     # elem[2]
            "rect",   # elem[2][0]
            {"y": "15", "x": "6", "height": "20", "width": "20"}   # elem[2][1]
            ]
            ]
            ["g", {"id": "0mx"}, # elem[0:1]
             ["path", {"d": "M3,20 9,0 20,0", "class": "s1"}], # elem[2]
             ["path", {"d": "m20,15 -5,5", "class": "s2"}], # elem[3]
             ["path", {"d": "M20,10 10,20", "class": "s2"}],
             ["path", {"d": "M20,5 5,20", "class": "s2"}],
             ["path", {"d": "M20,0 4,16", "class": "s2"}],
             ["path", {"d": "M15,0 6,9", "class": "s2"}],
             ["path", {"d": "M10,0 9,1", "class": "s2"}],
             ["path", {"d": "m0,20 20,0", "class": "s1"}] # elem[9]
             ],
            """
            ctype = elem[0]
            ret = self.container[ctype]()
            ret.attribs = elem[1]

            def gen_elem(e):
                if e[0] == "path":
                    attr = e[1]
                    elem = self.element.path(d=attr["d"])
                    elem.attribs = attr
                elif e[0] == "rect":
                    attr = e[1]
                    x = attr["x"]
                    y = attr["y"]
                    w = attr["width"]
                    h = attr["height"]
                    elem = self.element.rect(insert=(x, y), size=(w, h))
                    elem.attribs = attr

                return elem
            [ret.add(gen_elem(e)) for e in elem[2:]]

            return ret
        # default.add_stylesheet("css/default.css", title="default")
        skin = waveskin.WaveSkin["default"]

        if source.get("config") and source.get("config").get("skin"):
            if waveskin.WaveSkin.get(source.get("config").get("skin")):
                skin = waveskin.WaveSkin[source.get("config").get("skin")]

        template = svgwrite.Drawing(id="svgcontent_{index}".format(index=index))
        if index == 0:
            template.defs.add(template.style(css.css.default))
            [template.defs.add(get_container(e)) for e in skin[3][1:]]
            self.lane.xs = int(skin[3][1][2][1]["width"])
            self.lane.ys = int(skin[3][1][2][1]["height"])
            self.lane.xlabel = int(skin[3][1][2][1]["x"])
            self.lane.ym = int(skin[3][1][2][1]["y"])

        return template

    def insertSVGTemplate(self, index=0, parent=[], source={}):
        """
        index = 0
        parent = []
        source = {}
        """
        e = waveskin.WaveSkin["default"]

        if source.get("config") and source.get("config").get("skin"):
            if waveskin.WaveSkin.get(source.get("config").get("skin")):
                e = waveskin.WaveSkin[source.get("config").get("skin")]

        if index == 0:
            # get unit size
            # ["rect", {"y": "15", "x": "6", "height": "20", "width": "20"}]
            self.lane.xs = int(e[3][1][2][1]["width"])
            self.lane.ys = int(e[3][1][2][1]["height"])
            self.lane.xlabel = int(e[3][1][2][1]["x"])
            self.lane.ym = int(e[3][1][2][1]["y"])

        else:
            e = ["svg",
                 {"id": "svg",
                  "xmlns": "http://www.w3.org/2000/svg",
                  "xmlns:xlink": "http://www.w3.org/1999/xlink",
                  "height": "0"},
                 [  # e[-1]
                     "g",  # e[-1][0]
                     {"id": "waves"},  # e[-1][1]
                     [  # e[-1][2]
                         "g",  # e[-1][2][0]
                         {"id": "lanes"}  # e[-1][2][1]
                     ],
                     [  # e[-1][3]
                         "g",  # e[-1][3][0]
                         {"id": "groups"}  # e[-1][3][1]
                     ]
                 ]
                 ]

        e[-1][1]["id"] = "waves_{index}".format(index=index)
        e[-1][2][1]["id"] = "lanes_{index}".format(index=index)
        e[-1][3][1]["id"] = "groups_{index}".format(index=index)
        e[1]["id"] = "svgcontent_{index}".format(index=index)
        e[1]["height"] = 0

        parent.extend(e)

    def renderWaveForm(self, index=0, source={}, output=[]):
        """
        index = 0
        source = {}
        output = []
        """

        xmax = 0
        root = []
        groups = []

        if source.get("signal"):
            # self.insertSVGTemplate(index, output, source)
            template = self.anotherTemplate(index, source)
            waves = template.g(id="waves_{index}".format(index=index))
            lanes = template.g(id="lanes_{index}".format(index=index))
            groups = template.g(id="groups_{index}".format(index=index))
            self.parseConfig(source)
            ret = AttrDict({"x": 0, "y": 0, "xmax": 0, "width": [], "lanes": [], "groups": []})
            self.rec(source["signal"], ret)  # parse lanes
            content = self.parseWaveLanes(ret.lanes)
            glengths = self.renderWaveLane(lanes, content, index)
            for i, val in enumerate(glengths):
                xmax = max(xmax, (val + ret.width[i]))
            # self.renderMarks(root, content, index)
            marks = self.renderMarks(lanes, content, index)
            self.renderArcs(lanes, ret.lanes, index, source)
            self.renderGaps(lanes, ret.lanes, index)
            self.renderGroups(groups, ret.groups, index)
            self.lane.xg = int(math.ceil(float(xmax - self.lane.tgo) / float(self.lane.xs))) * self.lane.xs
            width = self.lane.xg + self.lane.xs * (self.lane.xmax + 1)
            height = len(content) * self.lane.yo + self.lane.yh0 + self.lane.yh1 + self.lane.yf0 + self.lane.yf1
            # output[1] = {
            #     "id": "svgcontent_{}".format(index),
            #     "xmlns": "http://www.w3.org/2000/svg",
            #     "xmlns:xlink": "http://www.w3.org/1999/xlink",
            #     "width": str(width),
            #     "height": str(height),
            #     "viewBox": "0 0 {w} {h}".format(w=width, h=height),
            #     "overflow": "hidden"
            # }
            template["width"] = width
            template["height"] = height
            template.viewbox(0, 0, width, height)
            dx = self.lane.xg + 0.5
            dy = float(self.lane.yh0) + float(self.lane.yh1)
            lanes.translate(dx, dy)
            # output[-1][2][1]["transform"] = "translate({dx},{dy})".format(dx=dx, dy=dy)

            waves.add(lanes)
            waves.add(groups)
            template.add(waves)
            return template

        # output[-1][2].extend(root)
        # output[-1][3].extend(groups)

    def renderGroups(self, root=[], groups=[], index=0):

        svgns = "http://www.w3.org/2000/svg",
        xmlns = "http://www.w3.org/XML/1998/namespace"

        for i, val in enumerate(groups):
            dx = groups[i].x + 0.5
            dy = groups[i].y * self.lane.yo + 3.5 + self.lane.yh0 + self.lane.yh1
            h = int(groups[i]["height"] * self.lane.yo - 16)
            group = self.element.path(id="group_{i}_{index}".format(i=i, index=index),
                                      d="m {dx},{dy} c -3,0 -5,2 -5,5 l 0,{h}".format(dx=dx, dy=dy, h=h),
                                      style="stroke:#0041c4;stroke-width:1;fill:none")
            # group = [
            #     "path",
            #     {
            #         # "id": "group_" + str(i) + "_" + str(index),
            #         # "d": "m " + str(groups[i]["x"] + 0.5) + "," + str(groups[i]["y"] * self.lane.yo + 3.5 + self.lane.yh0 + self.lane.yh1) + " c -3,0 -5,2 -5,5 l 0," + str(int(groups[i]["height"] * self.lane.yo - 16)) + " c 0,3 2,5 5,5",
            #         "id": "group_{i}_{index}".format(i=i, index=index),
            #         "d": "m {dx},{dy} c -3,0 -5,2 -5,5 l 0,{h}".format(dx=dx, dy=dy, h=h),
            #         "style": "stroke:#0041c4;stroke-width:1;fill:none"
            #     }
            # ]
            # root.append(group)
            root.add(group)

            name = groups[i]["name"]
            x = int(groups[i]["x"] - 10)
            y = int(self.lane.yo * (groups[i]["y"] + (float(groups[i]["height"]) / 2)) +
                    self.lane.yh0 + self.lane.yh1)
            label = self.container.g()
            label.translate(x, y)
            gg = self.container.g()
            gg.rotate(270)
            t = self.element.text("", text_anchor="middle")
            t["class"] = "info"
            t["xml:space"] = "preserve"
            t.add(self.element.tspan(name))
            gg.add(t)
            label.add(gg)
            # label = [
            #     ["g",
            #      # {"transform": "translate(" + x + "," + y + ")"},
            #      {"transform": "translate({x},{y})".format(x=x, y=y)},
            #      ["g", {"transform": "rotate(270)"},
            #       "text",
            #       {
            #          "text-anchor": "middle",
            #          "class": "info",
            #          "xml:space": "preserve"
            #      },
            #          ["tspan", name]
            #      ]
            #      ]
            # ]
            # root.append(label)
            root.add(label)

    def renderGaps(self, root, source, index):

        Stack = []
        svgns = "http://www.w3.org/2000/svg",
        xlinkns = "http://www.w3.org/1999/xlink"

        if source:

            gg = self.container.g(id="wavegaps_{index}".format(index=index))
            # gg = [
            #     "g",
            #     {"id": "wavegaps_{index}".format(index=index)}
            # ]

            for idx, val in enumerate(source):
                self.lane.period = val.get("period", 1)
                self.lane.phase = int(val.get("phase", 0) * 2)

                dy = self.lane.y0 + idx * self.lane.yo
                g = self.container.g(id="wavegap_{i}_{index}".format(i=idx, index=index))
                g.translate(0, dy)
                # g = [
                #     "g",
                #     {
                #         # "id": "wavegap_" + str(i) + "_" + str(index),
                #         # "transform": "translate(0," + str(self.lane.y0 + i * self.lane.yo) + ")"
                #         "id": "wavegap_{i}_{index}".format(i=idx, index=index),
                #         "transform": "translate(0,{dy})".format(dy=dy)
                #     }
                # ]
                # gg.append(g)

                if val.get("wave"):
                    text = val["wave"]
                    Stack = text
                    pos = 0
                    while len(Stack):
                        c = Stack[0]
                        Stack = Stack[1:]
                        if c == "|":
                            dx = float(self.lane.xs) * ((2 * pos + 1) * float(self.lane.period)
                                                        * float(self.lane.hscale) - float(self.lane.phase))
                            b = self.container.use(href="#gap")
                            b.translate(dx)
                            # b = [
                            #     "use",
                            #     {
                            #         "xmlns:xlink": xlinkns,
                            #         "xlink:href": "#gap",
                            #         # "transform": "translate(" + str(int(float(self.lane.xs) * ((2 * pos + 1) * float(self.lane.period) * float(self.lane.hscale) - float(self.lane.phase)))) + ")"
                            #         "transform": "translate({dx})".format(dx=dx)
                            #     }
                            # ]
                            # g.append(b)
                            g.add(b)
                        pos += 1
                gg.add(g)

            # root.append(gg)
            root.add(gg)
            # return root

    def is_type_str(self, var):
        if sys.version_info[0] < 3:
            return type(var) in [str, unicode]
        else:
            return type(var) is str

    def convert_to_svg(self, root):

        svg_output = ""

        if type(root) is list:
            if len(root) >= 2 and type(root[1]) is dict:
                if len(root) == 2:
                    svg_output += "<{}{}/>\n".format(root[0], self.convert_to_svg(root[1]))
                elif len(root) >= 3:
                    svg_output += "<{}{}/>\n".format(root[0], self.convert_to_svg(root[1]))
                    if len(root) == 3:
                        svg_output += self.convert_to_svg(root[2])
                    else:
                        svg_output += self.convert_to_svg(root[2:])
                    svg_output += "</{}>\n".format(root[0])
            elif type(root[0]) is list:
                for eleml in root:
                    svg_output += self.convert_to_svg(eleml)
            else:
                svg_output += "<{}>\n".format(root[0])
                for eleml in root[1:]:
                    svg_output += self.convert_to_svg(eleml)
                svg_output += "</{}>\n".format(root[0])
        elif type(root) is dict:
            for elemd in root:
                svg_output += " {}=\"{}\"".format(elemd, root[elemd])
        else:
            svg_output += root

        return svg_output


def main(args=None):
    if not args:
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

        output = wavedrom.renderWaveForm(0, jinput)
        # wavedrom.renderWaveForm(0, jinput, output)

        # svg_output = wavedrom.convert_to_svg(output)
        # with open(outputfile, "w") as f:
        #     f.write(svg_output)
        output.saveas(outputfile)


if __name__ == "__main__":
    main()
