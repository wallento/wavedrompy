# The MIT License (MIT)
#
# Copyright (c) 2016-2018 BreizhGeek, Kazuki Yamamoto, Stefan Wallentowitz
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

import svgwrite
from attrdict import AttrDict


class SVGBase(object):
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
        "title": svgwrite.base.Title,
        "line": svgwrite.shapes.Line,
    })
