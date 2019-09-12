# Copyright wavedrompy contributors.
# SPDX-License-Identifier: MIT

# Translated to Python from original file:
# https://github.com/drom/wavedrom/blob/master/src/WaveDrom.js

from collections import namedtuple
import svgwrite

from .base import SVGBase


class RenderState:
    def __init__(self, x=0, y=0, xmax=0):
        self.x = x
        self.y = y
        self.xmax = xmax

    def __str__(self):
        return "x={} y={}, xmax={}".format(self.x, self.y, self.xmax)


RenderObject = namedtuple("RenderObject", "name x y")


class Assign(SVGBase):
    def render_tree(self, tree, state):
        state.xmax = max(state.xmax, state.x)
        y = state.y
        for i in range(1, len(tree)):
            if isinstance(tree[i], list):
                state = self.render_tree(tree[i], RenderState(x=state.x+1, y=state.y, xmax=state.xmax))
            else:
                tree[i] = RenderObject(name=tree[i], x=state.x+1, y=state.y)
                state.y += 2
        tree[0] = RenderObject(name=tree[0], x=state.x, y=round((y+state.y-2)/2))
        state.x -= 1

        return state

    def draw_body(self, type, ymin, ymax):
        circle = ' M 4,0 C 4,1.1 3.1,2 2,2 0.9,2 0,1.1 0,0 c 0,-1.1 0.9,-2 2,-2 1.1,0 2,0.9 2,2 z'
        gates = {
            '~':  'M -11,-6 -11,6 0,0 z m -5,6 5,0' + circle,
            '=':  'M -11,-6 -11,6 0,0 z m -5,6 5,0',
            '&':  'm -16,-10 5,0 c 6,0 11,4 11,10 0,6 -5,10 -11,10 l -5,0 z',
            '~&': 'm -16,-10 5,0 c 6,0 11,4 11,10 0,6 -5,10 -11,10 l -5,0 z' + circle,
            '|':  'm -18,-10 4,0 c 6,0 12,5 14,10 -2,5 -8,10 -14,10 l -4,0 c 2.5,-5 2.5,-15 0,-20 z',
            '~|': 'm -18,-10 4,0 c 6,0 12,5 14,10 -2,5 -8,10 -14,10 l -4,0 c 2.5,-5 2.5,-15 0,-20 z' + circle,
            '^':  'm -21,-10 c 1,3 2,6 2,10 m 0,0 c 0,4 -1,7 -2,10 m 3,-20 4,0 c 6,0 12,5 14,10 -2,5 -8,10 -14,10 l -4,0 c 1,-3 2,-6 2,-10 0,-4 -1,-7 -2,-10 z',
            '~^': 'm -21,-10 c 1,3 2,6 2,10 m 0,0 c 0,4 -1,7 -2,10 m 3,-20 4,0 c 6,0 12,5 14,10 -2,5 -8,10 -14,10 l -4,0 c 1,-3 2,-6 2,-10 0,-4 -1,-7 -2,-10 z' + circle,
            '+':  'm -8,5 0,-10 m -5,5 10,0 m 3,0 c 0,4.418278 -3.581722,8 -8,8 -4.418278,0 -8,-3.581722 -8,-8 0,-4.418278 3.581722,-8 8,-8 4.418278,0 8,3.581722 8,8 z',
            '*':  'm -4,4 -8,-8 m 0,8 8,-8 m 4,4 c 0,4.418278 -3.581722,8 -8,8 -4.418278,0 -8,-3.581722 -8,-8 0,-4.418278 3.581722,-8 8,-8 4.418278,0 8,3.581722 8,8 z'
        }
        iec = {
            "BUF": 1, "INV": 1, "AND": '&',  "NAND": '&',
            "OR": '\u22651', "NOR": '\u22651', "XOR": '=1', "XNOR": '=1', "box": ''
        }
        circled = { "INV", "NAND", "NOR", "XNOR" }

        if ymax == ymin:
            ymax = 4
            ymin = -4

        if type in gates:
            return self.element.path(class_='gate', d=gates[type])
        elif type in iec:
            g = self.container.g()
            if type in circled:
                path = self.element.path(class_="gate", d="m -16,{} 16,0 0,{} -16,0 z {}".format(ymin-3, ymax-ymin+6, circle))
            else:
                path = self.element.path(class_="gate", d="m -16,{} 16,0 0,{} -16,0 z".format(ymin-3, ymax-ymin+6))
            g.add(path)
            tspan = self.element.tspan(iec[type], x=[-14], y=[4], class_='wirename')
            text = self.element.text('')
            text.add(tspan)
            g.add(text)
            return g
        else:
            tspan = self.element.tspan(type, x=[-14], y=[4], class_='wirename')
            text = self.element.text('')
            text.add(tspan)
            return text

    def draw_gate(self, spec):
        ret = self.container.g()

        ys = [s[1] for s in spec[2:]]

        ymin = min(ys)
        ymax = max(ys)

        g = self.container.g(transform="translate(16,0)")
        g.add(self.element.path(d="M {},{} {},{}".format(spec[2][0], ymin, spec[2][0], ymax), class_='wire'))
        ret.add(g)

        for s in spec[2:]:
            path = self.element.path(d="m {},{} 16,0".format(s[0], s[1]), class_='wire')
            ret.add(self.container.g().add(path))

        g = self.container.g(transform="translate({},{})".format(spec[1][0], spec[1][1]))
        g.add(self.element.title(spec[0]))
        g.add(self.draw_body(spec[0], ymin - spec[1][1], ymax - spec[1][1]))
        ret.add(g)

        return ret

    def draw_boxes(self, tree, xmax):
        ret = self.container.g()
        spec = []

        if isinstance(tree, list):
            spec.append(tree[0].name);
            spec.append([32 * (xmax - tree[0].x), 8 * tree[0].y]);
            for t in tree[1:]:
                if isinstance(t, list):
                    spec.append([32 * (xmax - t[0].x), 8 * t[0].y])
                else:
                    spec.append([32 * (xmax - t.x), 8 * t.y])

            ret.add(self.draw_gate(spec))

            for t in tree[1:]:
                ret.add(self.draw_boxes(t, xmax))
        else:
            fname = tree.name
            fx = 32 * (xmax - tree.x)
            fy = 8 * tree.y
            g = self.container.g(transform="translate({},{})".format(fx, fy))
            g.add(self.element.title(fname))
            g.add(self.element.path(d='M 2,0 a 2,2 0 1 1 -4,0 2,2 0 1 1 4,0 z'))
            tspan = self.element.tspan(fname, x=[-4], y=[4], class_='pinname')
            text = self.element.text('')
            text.add(tspan)
            g.add(text)
            ret.add(g)

        return ret

    def render(self, index = 0, source = {}, output = []):
        STYLE = ".pinname {font-size:12px; font-style:normal; font-variant:normal; font-weight:500; font-stretch:normal; text-align:center; text-anchor:end; font-family:Helvetica} .wirename {font-size:12px; font-style:normal; font-variant:normal; font-weight:500; font-stretch:normal; text-align:center; text-anchor:start; font-family:Helvetica} .wirename:hover {fill:blue} .gate {color:#000; fill:#ffc; fill-opacity: 1;stroke:#000; stroke-width:1; stroke-opacity:1} .gate:hover {fill:red !important; } .wire {fill:none; stroke:#000; stroke-width:1; stroke-opacity:1} .grid {fill:#fff; fill-opacity:1; stroke:none}"

        tree = source.get("assign")
        state = RenderState(x=0, y=2, xmax=0)

        for t in tree:
            state = self.render_tree(t, state)
            state.x += 1

        xmax = state.xmax + 3

        width = 32 * (xmax + 1) + 1
        height = 8 * (state.y + 1) - 7
        ilen = 4 * (xmax + 1)
        jlen = state.y + 1

        grid = self.container.g()

        for i in range(ilen+1):
            for j in range(jlen+1):
                grid.add(self.element.rect(height=1, width=1, x=(i * 8 - 0.5), y=(j * 8 - 0.5), class_='grid'))

        for t in tree:
            content = self.draw_boxes(t, xmax)


        attr = { 'viewBox': "0 0 {} {}".format(width, height)}
        template = svgwrite.Drawing(id="svgcontent_{index}".format(index=index), size=[width, height], **attr)
        template.defs.add(svgwrite.container.Style(content=STYLE))
        g = self.container.g(transform="translate(0.5,0.5)")
        g.add(grid)
        g.add(content)
        template.add(g)
        return template
