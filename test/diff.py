import re
from collections import namedtuple

import xmldiff
import xmldiff.main
from lxml import etree

from PIL import Image, ImageChops
import cairosvg
import io

UpdateAttribx = namedtuple("UpdateAttribx", 'node name value old')
MoveNodex = namedtuple("MoveNodex", 'node target position nodex targetx')


def main(f_out, f_out_py):
    parser = etree.XMLParser(remove_blank_text=True)
    orig_tree = etree.parse(f_out, parser)
    py_tree = etree.parse(f_out_py, parser)

    diff = xmldiff.main.diff_trees(orig_tree, py_tree)
    unknown = []

    for action in diff:
        if isinstance(action, xmldiff.actions.UpdateAttrib):
            node = orig_tree.xpath(action.node)[0]
            if node.tag[-3:] == "svg" and action.name == "viewBox":
                # The viewBox format differs, both are legal notations (space vs. comma-separated)
                if re.sub(r"\s+", ",", node.attrib[action.name]) == action.value:
                    continue
            elif re.sub(r"\s+", "", node.attrib[action.name]) == re.sub(r"\s+", "", action.value):
                # Whitespace differences are okay
                continue
            else:
                py = action.value
                js = node.attrib[action.name]
                if action.name in ["transform", "d", "x"]:
                    # Floating point and int differences
                    pattern_float = re.compile(r'(?<![\d.])([0-9]+)(?![\d.])')
                    pattern_comma = re.compile(r'\s*,\s*')
                    py = pattern_float.sub(r'\1.0', py)
                    js = pattern_float.sub(r'\1.0', js)
                    py = pattern_comma.sub(r',', py)
                    js = pattern_comma.sub(r',', js)
                    if py == js:
                        continue
            # Python >3.5, remove once we are over 2.7..
            # action = UpdateAttribx(**{ **action._asdict(), "old": node.attrib[action.name]})
            action_dict = action._asdict()
            action_dict["old"] = node.attrib[action.name]
            action = UpdateAttribx(**action_dict)
        elif isinstance(action, xmldiff.actions.InsertAttrib):
            node = orig_tree.xpath(action.node)[0]
            if node.tag[-3:] == "svg" and action.name in ["baseProfile", "version"]:
                # svgwrite adds more info to the svg element
                continue
        elif isinstance(action, xmldiff.actions.MoveNode):
            node = orig_tree.xpath(action.node)[0]
            node.getparent().remove(node)
            target = orig_tree.xpath(action.target)[0]
            target.insert(action.position, node)
            if node.tag.endswith("}style"):
                # This is okay
                continue
            action_dict = action._asdict()
            action_dict["nodex"] = etree.tostring(node)
            action_dict["targetx"] = etree.tostring(target)
            action = MoveNodex(**action_dict)
        elif isinstance(action, xmldiff.actions.UpdateTextIn):
            node = orig_tree.xpath(action.node)[0]
            if action.text is None:
                if node.tag[-2:] == "}g" and node.attrib["id"] == "groups_0":
                    # Upstream bug, reported: https://github.com/wavedrom/wavedrom/issues/251
                    continue
            elif node.text is None:
                pass
            elif re.sub(r"\s+", "", node.text) == re.sub(r"\s+", "", action.text):
                # Whitespace differences are okay
                continue
            action = action._replace(node=etree.tostring(node))
        elif isinstance(action, xmldiff.actions.InsertNode):
            # Not okay, but we must do the same to preserve the valid tree for further checks
            target = orig_tree.xpath(action.target)[0]
            node = target.makeelement(action.tag)
            target.insert(action.position, node)
            action = action._replace(target=etree.tostring(orig_tree.xpath(action.target)[0]))
        elif isinstance(action, xmldiff.actions.DeleteNode):
            node = orig_tree.xpath(action.node)[0]
            node.getparent().remove(node)
            action = action._replace(node=etree.tostring(node))

        unknown.append(action)
    return unknown

def diff_raster(f_out_js, f_out_py):
    with open(f_out_js, encoding="utf-8") as fileObj_svg_js:
        svg_js = fileObj_svg_js.read()

    with open(f_out_py, encoding="utf-8") as fileObj_svg_py:
        svg_py = fileObj_svg_py.read()

    png_js = cairosvg.svg2png(svg_js)
    png_py = cairosvg.svg2png(svg_py)

    image_js = Image.open(io.BytesIO(png_js))
    image_py = Image.open(io.BytesIO(png_py))

    return ImageChops.difference(image_js, image_py)
