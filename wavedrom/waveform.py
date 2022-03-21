# Copyright wavedrompy contributors.
# SPDX-License-Identifier: MIT

# Originally translated to Python from original file:
# https://github.com/drom/wavedrom/blob/master/src/WaveDrom.js
# Now many parts have been rewritten and diverged

import sys
import math
import re
from itertools import chain
import svgwrite
from .attrdict import AttrDict
from collections import deque

from six import string_types

from wavedrom.tspan import JsonMLElement
from . import waveskin, css
from .base import SVGBase


class WaveDrom(SVGBase):
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

    @staticmethod
    def stretch_bricks(wave, stretch):
        stretcher = {
            "Pclk": "111", "Nclk": "000",
            "pclk": "111", "nclk": "000",
            "0": "000", "1": "111", "x": "xxx", "d": "ddd", "u": "uuu", "z": "zzz",
            "2": "vvv-2", "3": "vvv-3", "4": "vvv-4", "5": "vvv-5", "6": "vvv-6",
            "7": "vvv-7", "8": "vvv-8", "9": "vvv-9"}

        if stretch == -0.5:
            # This is the only valid non-integer value, it essentially means halfing down. Further subsampling
            # does not work I think..
            return wave[0::2]
        else:
            stretch = int(stretch)

            def getBrick(w):
                if w in stretcher:
                    return stretcher[w]
                elif w[2] in stretcher:
                    return stretcher[w[2]]
                else:
                    return stretcher[w[-1]]

            if stretch > 0:
                return list(chain.from_iterable(([w] + [getBrick(w)]*stretch for w in wave)))
            else:
                return wave

    def gen_wave_brick(self, prev=None, this=None, stretch=0, repeat=0, subcycle=False):
        sharpedge_clk = { "p": "pclk", "n": "nclk", "P": "Pclk", "N": "Nclk" }
        sharpedge_sig = { "h": "pclk", "l": "nclk", "H": "Pclk", "L": "Nclk" }
        sharpedge = sharpedge_clk.copy()
        sharpedge.update(sharpedge_sig)

        # level: logical levels of symbols at wave
        level = {"=": "v", "2": "v", "3": "v", "4": "v", "5": "v", "6": "v",
                 "7": "v", "8": "v", "9": "v", "h": "1", "H": "1", "l": "0", "L": "0"}
        # translevel: Those are the levels at the end of a cycle (special for clocks)
        translevel = level.copy()
        translevel.update({"p": "0", "P": "0", "n": "1", "N": "1"})
        # data: Modifiers of wavebricks that add data
        data = {"=": "-2", "2": "-2", "3": "-3", "4": "-4", "5": "-5", "6":
                "-6", "7": "-7", "8": "-8", "9": "-9"}
        # clkinvert: The inverse brick to clock symbols
        clkinvert = {"p": "nclk", "n": "pclk", "P": "nclk", "N": "pclk"}
        # xclude: Those are actually identical levels, no transition
        xclude = {"hp": "111", "Hp": "111", "ln": "000", "Ln": "000",
                  "nh": "111", "Nh": "111", "pl": "000", "Pl": "000"}

        if this in sharpedge.keys():
            if prev is None:
                if this in sharpedge_clk.keys():
                    first = sharpedge[this]
                else:
                    first = level.get(this, this)*3
            else:
                first = xclude.get(prev+this, sharpedge[this])

            if this in sharpedge_clk.keys():
                wave = [first, clkinvert[this]] * (1 + repeat)
            else:
                wave = [first] + [level.get(this, this)*3]*(2 * repeat + 1)
        else:
            if prev is None:
                transition = level.get(this, this)*3 + data.get(this, "")
            else:
                transition = translevel.get(prev, prev) + 'm' + level.get(this, this) + data.get(prev, "") + data.get(this, "")
            value = level.get(this, this)*3 + data.get(this, "")
            wave = [transition, value] + [value, value] * repeat

        if subcycle:
            wave = wave[0:repeat+1]

        if not (stretch == -0.5 and this in sharpedge_clk.keys()):
            wave = self.stretch_bricks(wave, stretch)

        return wave

    def parse_wave_lane(self, text, stretch=0):
        R = []

        Stack = deque(text)

        This = None
        subCycle = False

        while len(Stack) > 0:
            Top = This
            This = Stack.popleft()
            repeat = 0
            if This == '|':
                This = 'x'
            if This == '<':
                subCycle = True
                This = Top
                Top = None
                if Stack[0] in ['.', '|']:
                    Stack.popleft()
                else:
                    continue
            if This == '>':
                subCycle = False
                This = Top
                Top = None
                if Stack and Stack[0] in ['.', '|']:
                    Stack.popleft()
                else:
                    continue
            while Stack and Stack[0] in ['.', '|']:
                Stack.popleft()
                repeat += 1
            R.extend(self.gen_wave_brick(Top, This, stretch, repeat, subCycle))

        for i in range(int(math.ceil(self.lane.phase))):
            R = R[1:]

        return R

    def parse_wave_lanes(self, sig=""):
        def data_extract(e):
            tmp = e.get("data")
            if tmp is not None:
                tmp = tmp.split() if isinstance(tmp, string_types) else tmp
            return tmp

        content = []
        for sigx in sig:
            self.lane.period = sigx.get("period", 1)
            self.lane.phase = sigx.get("phase", 0) * 2
            sub_content = []
            sub_content.append([sigx.get("name", " "), sigx.get("phase", 0)])
            if sigx.get("wave"):
                sub_content.append(self.parse_wave_lane(sigx["wave"], self.lane.period * self.lane.hscale - 1))
            else:
                sub_content.append(None)
            sub_content.append(data_extract(sigx))
            content.append(sub_content)

        return content

    def find_lane_markers(self, lanetext=""):

        lcount = 0
        gcount = 0
        ret = []
        for idx, val in enumerate(lanetext):
            if val in ["vvv-2", "vvv-3", "vvv-4", "vvv-5", "vvv-6", "vvv-7", "vvv-8", "vvv-9"]:
                lcount += 1
            else:
                if lcount != 0:
                    ret.append(gcount - ((lcount + 1) / 2))
                    lcount = 0

            gcount += 1

        if lcount != 0:
            ret.append(gcount - ((lcount + 1) / 2))

        return ret

    def render_lane_uses(self, val, g):
        if val[1]:
            for i in range(len(val[1])):
                b = self.container.use(href="#{}".format(val[1][i]))
                b.translate(i * self.lane.xs)
                g.add(b)

            if val[2] and len(val[2]):
                labels = self.find_lane_markers(val[1])
                if len(labels) != 0:
                    for k in range(len(labels)):
                        if val[2] and k < len(val[2]):
                            tx = int(labels[k]) * self.lane.xs + self.lane.xlabel
                            title = self.element.text("", x=[tx], y=[self.lane.ym], text_anchor="middle")
                            title.add(self.element.tspan(val[2][k]))
                            title["xml:space"] = "preserve"
                            g.add(title)

    def text_width(self, string, size=11):
        chars = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,34,47,74,74,118,89,25,44,44,52,78,37,
                 44,37,37,74,74,74,74,74,74,74,74,74,74,37,37,78,78,78,74,135,89,89,96,96,89,81,103,96,37,67,89,74,109,
                 96,103,89,103,96,89,81,96,89,127,89,87,81,37,37,37,61,74,44,74,74,67,74,74,37,74,74,30,30,67,30,112,74,
                 74,74,74,44,67,37,74,67,95,66,65,67,44,34,44,78,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                 0,0,0,0,0,0,37,43,74,74,74,74,34,74,44,98,49,74,78,0,98,73,53,73,44,44,44,77,71,37,44,44,49,74,111,111,
                 111,81,89,89,89,89,89,89,133,96,89,89,89,89,37,37,37,37,96,96,103,103,103,103,103,78,103,96,96,96,96,
                 87,89,81,74,74,74,74,74,74,118,67,74,74,74,74,36,36,36,36,74,74,74,74,74,74,74,73,81,74,74,74,74,65,74,
                 65,89,74,89,74,89,74,96,67,96,67,96,67,96,67,96,82,96,74,89,74,89,74,89,74,89,74,89,74,103,74,103,74,
                 103,74,103,74,96,74,96,74,37,36,37,36,37,36,37,30,37,36,98,59,67,30,89,67,67,74,30,74,30,74,39,74,44,
                 74,30,96,74,96,74,96,74,80,96,74,103,74,103,74,103,74,133,126,96,44,96,44,96,44,89,67,89,67,89,67,89,
                 67,81,38,81,50,81,37,96,74,96,74,96,74,96,74,96,74,96,74,127,95,87,65,87,81,67,81,67,81,67,30,84,97,91,
                 84,91,84,94,92,73,104,109,91,84,81,84,100,82,76,74,103,91,131,47,40,99,77,37,79,130,100,84,104,114,87,
                 126,101,87,84,93,84,69,84,46,52,82,52,82,114,89,102,96,100,98,91,70,88,88,77,70,85,89,77,67,84,39,65,
                 61,39,189,173,153,111,105,61,123,123,106,89,74,37,30,103,74,96,74,96,74,96,74,96,74,96,74,81,91,81,91,
                 81,130,131,102,84,103,84,87,78,104,81,104,81,88,76,37,189,173,153,103,84,148,90,100,84,89,74,133,118,
                 103,81]

        return sum([(chars[ord(c)] if ord(c) <= len(chars) else 114) for c in string])*size/100

    def render_wave_lane(self, content="", index=0):
        xmax = 0
        xgmax = 0
        glengths = []
        groups = []

        for j, val in enumerate(content):
            name = val[0][0].strip()
            if name is not None:
                dy = self.lane.y0 + j * self.lane.yo
                g = self.container.g(id="wavelane_{j}_{index}".format(j=j, index=index))
                g.translate(0, dy)
                title = self.element.text("", x=[self.lane.tgo], y=[self.lane.ym], text_anchor="end")
                title.add(self.element.tspan(name))
                title["xml:space"] = "preserve"
                title["class"] = "info"
                g.add(title)

                glengths.append(self.text_width(name))

                xoffset = val[0][1]
                xoffset = math.ceil(2 * xoffset) - 2 * xoffset if xoffset > 0 else -2 * xoffset
                gg = self.container.g(id="wavelane_draw_{j}_{index}".format(j=j, index=index))
                gg.translate(xoffset * self.lane.xs, 0)

                self.render_lane_uses(val, gg)

                if val[1] and len(val[1]) > xmax:
                    xmax = len(val[1])

                g.add(gg)
                groups.append(g)
        self.lane.xmax = xmax
        self.lane.xg = xgmax + 20
        return (glengths, groups)

    def captext(self, g, cxt, anchor, y):
        if cxt.get(anchor) and cxt[anchor].get("text"):
            tmark = self.element.text("", x=[float(cxt.xmax)*float(cxt.xs)/2], y=[y], text_anchor="middle", fill="#000")
            tmark["xml:space"] = "preserve"
            if isinstance(cxt[anchor]["text"], string_types):
                tmark.add(self.element.tspan(cxt[anchor]["text"]))
            else:
                tmark.add(JsonMLElement(cxt[anchor]["text"]))
            g.add(tmark)

    def ticktock(self, g, cxt, ref1, ref2, x, dx, y, length):
        L = []

        if cxt.get(ref1) is None or cxt[ref1].get(ref2) is None:
            return

        val = cxt[ref1][ref2]

        if isinstance(val, string_types):
            val = val.split()
        elif isinstance(val, (int, float, bool)):
            offset = int(val)
            val = []
            for i in range(length):
                val.append(i + offset)

        if type(val) is list:
            if len(val) == 0:
                return
            elif len(val) == 1:
                offset = val[0]
                if isinstance(offset, string_types):
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

                if isinstance(offset, string_types) or isinstance(step, string_types):
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
            tmark = self.element.text(tmp, x=[i * dx + x], y=[y], text_anchor="middle")
            tmark["class"] = "muted"
            tmark["xml:space"] = "preserve"
            g.add(tmark)

    def render_marks(self, content="", index=0):
        def get_elem(e):
            if len(e) == 3:
                ret = self.element[e[0]](e[2])
                ret.attribs = e[1]
            elif len(e) == 2:
                ret = self.element[e[0]](e[1])
            else:
                ret = self.element.tspan(e)
            return ret

        mstep = 2 * int(self.lane.hscale)
        mmstep = mstep * self.lane.xs
        marks = int(self.lane.xmax / mstep)
        gy = len(content) * int(self.lane.yo)

        g = self.container.g(id="gmarks_{}".format(index))

        for i in range(marks + 1):
            gg = self.element.path(id="gmark_{i}_{index}".format(i=i, index=index),
                                   d="m {dx},0 0,{gy}".format(dx=i * mmstep, gy=gy),
                                   style="stroke:#888;stroke-width:0.5;stroke-dasharray:1,3")
            g.add(gg)

        self.captext(g, self.lane, "head", -33 if (self.lane.yh0 > 0) else -13)
        self.captext(g, self.lane, "foot", gy + (45 if (self.lane.yf0 > 0) else 25))
        self.ticktock(g, self.lane, "head", "tick",          0, mmstep,      -5, marks + 1)
        self.ticktock(g, self.lane, "head", "tock", mmstep / 2, mmstep,      -5, marks)
        self.ticktock(g, self.lane, "foot", "tick",          0, mmstep, gy + 15, marks + 1)
        self.ticktock(g, self.lane, "foot", "tock", mmstep / 2, mmstep, gy + 15, marks)

        return g

    def render_labels(self, root, source, index):
        if source:
            gg = self.container.g(id="labels_{index}".format(index=index))

            for idx, val in enumerate(source):
                self.lane.period = val.get("period", 1)
                self.lane.phase = val.get("phase", 0) * 2

                dy = self.lane.y0 + idx * self.lane.yo
                g = self.container.g(id="labels_{i}_{index}".format(i=idx, index=index))
                g.translate(0, dy)

                label = val.get("label")
                if label:
                    pos = 0
                    for l in re.findall(r"([\.\w]|(?:\{\w+\}))(?:\((\d*\.?\d+)\))?", label):
                        if l[0] == ".":
                            pos += 1
                            continue

                        text = l[0]
                        try:
                            offset = float(l[1])
                        except ValueError:
                            offset = 0

                        m = re.match(r"\{(\w+)\}", l[0])
                        if m:
                            text = m.group(1)
                        x = int(float(self.lane.xs) * (2 * (pos + offset) * self.lane.period *
                                                       self.lane.hscale - self.lane.phase) + float(self.lane.xlabel))
                        y = int(idx * self.lane.yo + self.lane.y0 + float(self.lane.ys) * 0.5) - dy

                        lwidth = len(text) * self.font_width
                        lx = float(x) - float(lwidth) / 2
                        ly = int(y) - 5
                        underlabel = self.element.rect(insert=(lx, ly),
                                                       size=(lwidth, 8), style="fill:#FFF;")
                        g.add(underlabel)
                        lx = float(x)
                        ly = int(y) + 2
                        label = self.element.text(text, style="font-size:8px;", text_anchor="middle",
                                                  x=[lx], y=[ly])
                        g.add(label)
                        pos += 1
                gg.add(g)
            root.add(gg)

    def arc_shape(self, Edge, frm, to):
        dx = float(to.x) - float(frm.x)
        dy = float(to.y) - float(frm.y)
        lx = (float(frm.x) + float(to.x)) / 2
        ly = (float(frm.y) + float(to.y)) / 2

        const_style = AttrDict({
            "a": "marker-end:url(#arrowhead);stroke:#0041c4;stroke-width:1;fill:none",
            "b": "marker-end:url(#arrowhead);marker-start:url(#arrowtail);stroke:#0041c4;stroke-width:1;fill:none"
        })

        pattern = {
            "-": { },
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

        props = AttrDict({"lx": lx, "ly": ly, "style": "fill:none;stroke:#00F;stroke-width:1",
                           "d": "M {fx},{fy} {tx},{ty}".format(fx=frm.x, fy=frm.y, tx=to.x, ty=to.y)})

        if Edge.shape in pattern:
            props.d = pattern[Edge.shape].get("d", props.d)
            props.style = pattern[Edge.shape].get("style", props.style)

            if Edge.label:
                if Edge.shape in ["-~", "-~>", "<-~>"]:
                    props.lx = float(frm.x) + (float(to.x) - float(frm.x)) * 0.75
                elif Edge.shape in ["~-", "~->"]:
                    props.lx = float(frm.x) + (float(to.x) - float(frm.x)) * 0.25
                elif Edge.shape in ["-|", "-|>", "<-|>"]:
                    props.lx = float(to.x)
                elif Edge.shape in ["|-", "|->"]:
                    props.lx = float(frm.x)

        return props

    def render_arc(self, Edge, frm, to, shapeProps):
        return self.element.path(id="gmark_{frm}_{to}".format(frm=Edge.frm, to=Edge.to),
                                  d=shapeProps.d, style=shapeProps.style)

    def render_label(self, p, text):
        w = self.text_width(text,8) + 2
        g = self.container.g(transform = "translate({},{})".format(p.x, p.y))
        # todo: I don't think this is correct. reported:
        # https://github.com/wavedrom/wavedrom/issues/252
        rect = self.element.rect(insert=(int(0-w/2), -5), size=(w, 10), style="fill:#FFF;")
        label = self.element.text("", style="font-size:8px;", text_anchor="middle", y=[3])
        label.add(self.element.tspan(text))
        g.add(rect)
        g.add(label)
        return g

    def render_arcs(self, source, index, top):
        Edge = AttrDict({"words": [], "frm": 0, "shape": "", "to": 0, "label": ""})
        Events = AttrDict({})

        if source:
            for idx, val in enumerate(source):
                self.lane.period = val.get("period", 1)
                self.lane.phase = val.get("phase", 0) * 2
                text = val.get("node")
                if text:
                    Stack = list(text)
                    Stack.reverse()
                    pos = 0
                    step = 1
                    while len(Stack) > 0:
                        eventname = Stack.pop()
                        if eventname == "<":
                            step = 0.25
                            continue
                        elif eventname == ">":
                            step = 1
                            continue
                        x = int(float(self.lane.xs) * (2 * pos * self.lane.period *
                                                       self.lane.hscale - self.lane.phase) + float(self.lane.xlabel))
                        y = int(idx * self.lane.yo + self.lane.y0 + float(self.lane.ys) * 0.5)
                        if eventname != ".":
                            Events[eventname] = AttrDict({"x": str(x), "y": str(y)})
                        pos += step

            gg = self.container.g(id="wavearcs_{index}".format(index=index))

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

                    shapeProps = self.arc_shape(Edge, frm, to)
                    gg.add(self.render_arc(Edge, frm, to, shapeProps))

                    if Edge.label:
                        gg.add(self.render_label(AttrDict({"x": shapeProps.lx, "y": shapeProps.ly}), Edge.label))


            for k in Events:
                if k.islower() or k.isdigit():
                    if int(Events[k].x) > 0:
                        gg.add(self.render_label(AttrDict({"x": Events[k].x, "y": Events[k].y}), k))

            return gg

    def parse_config(self, source={}):
        self.lane.hscale = 1
        if self.lane.get("hscale0"):
            self.lane.hscale = self.lane.hscale0

        if source and source.get("config") and source.get("config").get("hscale"):
            hscale = round(source.get("config").get("hscale"))
            if hscale > 0:
                if hscale > 100:
                    hscale = 100
                self.lane.hscale = hscale

        self.lane.xmin_cfg = 0
        self.lane.xmax_cfg = sys.maxsize
        if source and "config" in source and "hbounds" in source["config"]:
            if len(source["config"]["hbounds"]) == 2:
                source["config"]["hbounds"][0] = math.floor(source["config"]["hbounds"][0])
                source["config"]["hbounds"][1] = math.ceil(source["config"]["hbounds"][0])
                if source["config"]["hbounds"][0] < source["config"]["hbounds"][1]:
                    self.lane.xmin_cfg = 2 * source["config"]["hbounds"][0]
                    self.lane.xmax_cfg = 2 * source["config"]["hbounds"][1]

        self.lane.yh0 = 0
        self.lane.yh1 = 0
        if source and source.get("head"):
            self.lane.head = source["head"]
            if "tick" in source["head"] or "tock" in source["head"]:
                self.lane.yh0 = 20
            if "tick" in source["head"]:
                source["head"]["tick"] += self.lane.xmin_cfg/2
            if "tock" in source["head"]:
                source["head"]["tock"] += self.lane.xmin_cfg/2
            if source.get("head").get("text"):
                self.lane.yh1 = 46
                self.lane.head["text"] = source["head"]["text"]

        self.lane.yf0 = 0
        self.lane.yf1 = 0
        if source and source.get("foot"):
            self.lane.foot = source["foot"]
            if "tick" in source["foot"] or "tock" in source["foot"]:
                self.lane.yf0 = 20
            if "tick" in source["foot"]:
                source["foot"]["tick"] += self.lane.xmin_cfg/2
            if "tock" in source["foot"]:
                source["foot"]["tock"] += self.lane.xmin_cfg/2
            if source.get("foot").get("text"):
                self.lane.yf1 = 46
                self.lane.foot["text"] = source["foot"]["text"]

    def rec(self, tmp=[], state={}):
        name = None
        delta = AttrDict({"x": 10})
        if isinstance(tmp[0], str) or isinstance(tmp[0], int):
            name = str(tmp[0])
            delta.x = 25

        state.x += delta.x
        for idx, val in enumerate(tmp):
            if isinstance(val, list):
                old_y = state.y
                self.rec(val, state)
                state["groups"].append({"x": state.xx,
                                        "y": old_y,
                                        "height": state.y - old_y,
                                        "name": state.name})
            elif isinstance(val, dict):
                state["lanes"].append(val)
                state["width"].append(state.x)
                state.y += 1

        state.xx = state.x
        state.x -= delta.x
        state.name = name

    def another_template(self, index, source):
        def get_container(elem):
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

        skinname = source.get("config", {"skin" : "default"}).get("skin", "default")
        skin = waveskin.WaveSkin.get(skinname, waveskin.WaveSkin["default"])

        template = svgwrite.Drawing(id="svgcontent_{index}".format(index=index))
        if index == 0:
            template.add(template.style(skin[2][2]))
            [template.defs.add(get_container(e)) for e in skin[3][1:]]
            self.lane.xs = int(skin[3][1][2][1]["width"])
            self.lane.ys = int(skin[3][1][2][1]["height"])
            self.lane.xlabel = int(skin[3][1][2][1]["x"])
            self.lane.ym = int(skin[3][1][2][1]["y"])

        template["class"] = "WaveDrom"
        template["overflow"] = "hidden"

        return template

    def insert_svg_template(self, index=0, parent=[], source={}):
        e = waveskin.WaveSkin["default"]

        if source.get("config") and source.get("config").get("skin"):
            if waveskin.WaveSkin.get(source.get("config").get("skin")):
                e = waveskin.WaveSkin[source.get("config").get("skin")]

        if index == 0:
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

    def render_waveform(self, index=0, source={}, output=[], strict_js_features=False):
        xmax = 0

        if source.get("signal"):
            template = self.another_template(index, source)
            waves = template.g(id="waves_{index}".format(index=index))
            lanes = template.g(id="lanes_{index}".format(index=index))
            groups = template.g(id="groups_{index}".format(index=index))
            self.parse_config(source)
            ret = AttrDict({"x": 0, "y": 0, "xmax": 0, "width": [], "lanes": [], "groups": []})
            self.rec(source["signal"], ret)  # parse lanes
            content = self.parse_wave_lanes(ret.lanes)
            (glengths, lanegroups) = self.render_wave_lane(content, index)
            for i, val in enumerate(glengths):
                xmax = max(xmax, (val + ret.width[i]))
            marks = self.render_marks(content, index)
            gaps = self.render_gaps(ret.lanes, index)
            if not strict_js_features:
                self.render_labels(lanes, ret.lanes, index)
            arcs = self.render_arcs(ret.lanes, index, source)

            # Render
            lanes.add(marks)
            [lanes.add(l) for l in lanegroups]
            lanes.add(arcs)
            lanes.add(gaps)

            self.render_groups(groups, ret.groups, index)
            self.lane.xg = int(math.ceil(float(xmax - self.lane.tgo) / float(self.lane.xs))) * self.lane.xs
            width = self.lane.xg + self.lane.xs * (self.lane.xmax + 1)
            height = len(content) * self.lane.yo + self.lane.yh0 + self.lane.yh1 + self.lane.yf0 + self.lane.yf1
            template["width"] = width
            template["height"] = height
            template.viewbox(0, 0, width, height)
            dx = self.lane.xg + 0.5
            dy = float(self.lane.yh0) + float(self.lane.yh1) + 0.5
            lanes.translate(dx, dy)

            waves.add(lanes)
            waves.add(groups)
            template.add(waves)
            return template

    def render_groups(self, root=[], groups=[], index=0):
        for i, val in enumerate(groups):
            dx = groups[i]["x"] + 0.5
            dy = groups[i]["y"] * self.lane.yo + 3.5 + self.lane.yh0 + self.lane.yh1
            h = int(groups[i]["height"] * self.lane.yo - 16)
            group = self.element.path(id="group_{i}_{index}".format(i=i, index=index),
                                      d="m {dx},{dy} c -3,0 -5,2 -5,5 l 0,{h} c 0,3 2,5 5,5".format(dx=dx, dy=dy, h=h),
                                      style="stroke:#0041c4;stroke-width:1;fill:none")

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
            root.add(label)

    def render_gap_uses(self, wave, g):
        subCycle = False

        if wave:
            Stack = deque(wave)
            pos = 0
            while len(Stack):
                next = Stack.popleft()
                if next == '<':
                    subCycle = True
                    continue
                if next == '>':
                    subCycle = False
                    continue
                if subCycle:
                    pos += self.lane.period
                else:
                    pos += 2 * self.lane.period
                if next == "|":
                    if subCycle:
                        dx = float(self.lane.xs) * (pos * float(self.lane.hscale) - float(self.lane.phase))
                    else:
                        dx = float(self.lane.xs) * ((pos - self.lane.period) * float(self.lane.hscale) - float(self.lane.phase))
                    b = self.container.use(href="#gap")
                    b.translate(dx)
                    g.add(b)

    def render_gaps(self, source, index):
        if source:
            gg = self.container.g(id="wavegaps_{index}".format(index=index))

            for idx, val in enumerate(source):
                self.lane.period = val.get("period", 1)
                self.lane.phase = int(val.get("phase", 0) * 2) + self.lane.xmin_cfg

                dy = self.lane.y0 + idx * self.lane.yo
                g = self.container.g(id="wavegap_{i}_{index}".format(i=idx, index=index))
                g.translate(0, dy)

                if "wave" in val:
                    self.render_gap_uses(val["wave"], g)

                gg.add(g)

            return gg

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

    # Backward compatibility
    genWaveBrick = gen_wave_brick
    parseWaveLane = parse_wave_lane
    parseWaveLanes = parse_wave_lanes
    findLaneMarkers = find_lane_markers
    renderWaveLane = render_wave_lane
    renderMarks = render_marks
    renderLabels = render_labels
    renderArcs = render_arcs
    parseConfig = parse_config
    anotherTemplate = another_template
    insertSVGTemplate = insert_svg_template
    renderWaveForm = render_waveform
    renderGroups = render_groups
    renderGaps = render_gaps
