# Copyright wavedrompy contributors.
# SPDX-License-Identifier: MIT

import svgwrite
from .attrdict import AttrDict

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
