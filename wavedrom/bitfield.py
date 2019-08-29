# The MIT License (MIT)
#
# Copyright (c) 2011-2018 Aliaksei Chapyzhenka, BreizhGeek, Kazuki Yamamoto,
#                         Stefan Wallentowitz
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
if sys.version_info < (3, 0):
    from HTMLParser import HTMLParser
else:
    from html.parser import HTMLParser
from math import floor

import svgwrite

from .base import SVGBase


class Options:
    def __init__(self, vspace=80, hspace=640, lanes=2, bits=32, fontsize=14, bigendian=False, fontfamily='sans-serif',
                 fontweight='normal'):
        self.vspace = vspace if vspace > 19 else 80
        self.hspace = hspace if hspace > 39 else 640
        self.lanes = lanes if lanes > 0 else 2
        self.bits = bits if bits > 4 else 32
        self.fontsize = fontsize if fontsize > 5 else 14
        self.bigendian = bigendian
        self.fontfamily = fontfamily
        self.fontweight = fontweight

colors = {2: 0, 3: 80, 4: 170, 5: 45, 6: 126, 7: 215}

def type_style(t):
    if t in colors.keys():
        return ";fill:hsl({},100%,50%)".format(colors[t])
    else:
        return ''


class TspanParser(HTMLParser, object):
    tags = {
        'o': {'text_decoration': 'overline'},
        'ins': {'text_decoration': 'underline'},
        'sub': {'baseline_shift': 'sub'},
        'sup': {'baseline_shift': 'super'},
        'b': {'font_weight': 'bold'},
        'i': {'font_style': 'italic'},
        's': {'text_decoration': 'line-through'},
        'tt': {'font_family': 'monospace'},
    }

    def __init__(self):
        super(TspanParser, self).__init__()
        self.text = []
        self.state = []

    def handle_starttag(self, tag, attrs):
        self.state.append(tag)

    def handle_endtag(self, tag):
        if self.state.pop() != tag:
            raise RuntimeError("Unexpected closing tag: {}".format(tag))

    def get_style(self):
        return {k: v for d in [self.tags[t] for t in self.state] for k, v in d.items()}

    def handle_data(self, data):
        if len(self.state) == 0:
            self.text.append(svgwrite.text.TSpan(data))
        else:
            self.text.append(svgwrite.text.TSpan(data, **self.get_style()))

    def get_text(self):
        return self.text


class BitField(SVGBase):
    def tspan_parse(self, text):
        parser = TspanParser()
        parser.feed(text)
        return parser.get_text()

    def hline(self, len, x=0, y=0):
        return self.element.line(start=(x,y), end=(x+len,y))

    def vline(self, len, x=0, y=0):
        return self.element.line(start=(x,y), end=(x,y+len))

    def get_text(self, body, x, y=None):
        x_list = None
        if x:
            x_list = [x]
        y_list = None
        if y:
            y_list = [y]
        text = self.element.text('', x=x_list, y=y_list)
        for t in self.tspan_parse(str(body)):
            text.add(t)
        return text

    def get_label(self, attr, x, y, step=0, length=0):
        if isinstance(attr, int):
            attr = int(attr)
            res = []
            for i in range(length):
                val = (attr >> i) & 1
                xi = x + step * (length / 2 - i - 0.5)
                res.append(self.get_text(val, xi, y))
            return res
        else:
            return [self.get_text(attr, x, y)]

    def get_attrs(self, e, step, lsbm, msbm):
        x = step * (self.mod - ((msbm + lsbm) / 2) - 1)
        attr = e['attr']
        bits = e['bits']
        attrs = [attr]
        # 'attr' supports both a scalar and a list.
        if isinstance(attr, list):
            attrs = attr
        return [self.get_label(a, x, 16 * i, step, bits)
                for (i, a) in enumerate(attrs)]

    def labelArr(self, desc):
        step = self.opt.hspace / self.mod
        bits = self.container.g(transform="translate({},{})".format(step/2, self.opt.vspace/5))
        names = self.container.g(transform="translate({},{})".format(step/2, self.opt.vspace/2+4))
        attrs = self.container.g(transform="translate({},{})".format(step/2, self.opt.vspace))
        blanks = self.container.g(transform="translate(0,{})".format(self.opt.vspace/4))

        for e in desc:
            lsbm = 0
            msbm = self.mod - 1
            lsb = self.index * self.mod
            msb = (self.index + 1) * self.mod - 1

            if floor(e["lsb"] / self.mod) == self.index:
                lsbm = e["lsbm"]
                lsb = e["lsb"]
                if floor(e["msb"] / self.mod) == self.index:
                    msb = e["msb"]
                    msbm = e["msbm"]
            else:
                if floor(e["msb"] / self.mod) == self.index:
                    msb = e["msb"]
                    msbm = e["msbm"]
                else:
                    continue

            bits.add(self.get_text(lsb, x=[step*(self.mod-lsbm - 1)]))
            if lsbm != msbm:
                bits.add(self.get_text(msb, x=[step * (self.mod - msbm - 1)]))
            if e.get('name'):
                x = step*(self.mod-((msbm+lsbm)/2)-1)
                for n in self.get_label(e['name'], x, 0):
                    names.add(n)

            if not e.get('name') or e.get('type'):
                style = 'fill-opacity:0.1' + type_style(e.get('type', 0))
                insert = [step * (self.mod - msbm - 1), 0]
                size = [step * (msbm - lsbm + 1), self.opt.vspace/2]
                blanks.add(self.element.rect(insert=insert, size=size, style=style))
            if e.get('attr') is not None:
                for attr in self.get_attrs(e, step, lsbm, msbm):
                    for a in attr:
                        attrs.add(a)

        g = self.container.g()
        g.add(blanks)
        g.add(bits)
        g.add(names)
        g.add(attrs)
        return g

    def labels(self, desc):
        g = self.container.g(text_anchor='middle')
        g.add(self.labelArr(desc))
        return g

    def cage(self, desc):
        hspace = self.opt.hspace
        vspace = self.opt.vspace
        mod = self.mod

        g = self.container.g(stroke='black', stroke_width=1, stroke_linecap='round', transform="translate(0,{})".format(vspace/4))

        g.add(self.hline(hspace));
        g.add(self.vline(vspace / 2));
        g.add(self.hline(hspace, 0, vspace / 2));

        i = self.index * mod
        for j in range(mod, 0, -1):
            if j == mod or any([(e["lsb"] == i) for e in desc]):
                g.add(self.vline((vspace / 2), j * (hspace / mod)));
            else:
                g.add(self.vline((vspace / 16), j * (hspace / mod)));
                g.add(self.vline((vspace / 16), j * (hspace / mod), vspace * 7 / 16));
            i += 1

        return g

    def lane(self, desc):
        x = 4.5
        y = (self.opt.lanes-self.index-1)  * self.opt.vspace + 0.5
        g = self.container.g(transform = "translate({},{})".format(x, y),
                             text_anchor = "middle",
                             font_size = self.opt.fontsize,
                             font_family = self.opt.fontfamily,
                             font_weight = self.opt.fontweight)

        g.add(self.cage(desc))
        g.add(self.labels(desc))
        return g

    def get_max_attrs(self, desc):
        max_count = 0
        for e in desc:
            if 'attr' in e:
                if isinstance(e['attr'], list):
                    max_count = max(max_count, len(e['attr']))
                else:
                    max_count = max(max_count, 1)
        return max_count

    def render(self, desc, opt = Options()):
        self.opt = opt

        # Compute extra per-lane space needed if there are more than one attr
        # for any field.  This spaces all lanes uniformly, matching the lane
        # with the most attr's.
        extra_attrs = 0
        max_attrs = self.get_max_attrs(desc)
        if max_attrs > 1:
            extra_attrs = max_attrs - 1
        self.extra_attr_space = extra_attrs * 16

        width = opt.hspace + 9
        height = (opt.vspace + self.extra_attr_space) * opt.lanes + 5
        viewbox = { 'viewBox': "0 0 {} {}".format(width, height)}

        template = svgwrite.Drawing(id="svgcontent", size=[width, height], **viewbox)

        lsb = 0
        self.mod = int(opt.bits / opt.lanes)

        for e in desc:
            e["lsb"] = lsb
            e["lsbm"] = lsb % self.mod
            lsb += e['bits']
            e['msb'] = lsb - 1
            e['msbm'] = e['msb'] % self.mod

        for i in range(opt.lanes):
            self.index = i
            template.add(self.lane(desc))

        return template

    def renderJson(self, source):
        opt = Options()
        if source.get("options"):
            opt = Options(**source['options'])
        if source.get("reg"):
            return self.render(source['reg'], opt)
