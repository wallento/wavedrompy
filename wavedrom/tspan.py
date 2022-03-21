# Copyright wavedrompy contributors.
# SPDX-License-Identifier: MIT

import sys

import svgwrite
from six import string_types
from svgwrite.base import BaseElement
from svgwrite.etree import etree
from .attrdict import AttrDict

if sys.version_info < (3, 0):
    from HTMLParser import HTMLParser
else:
    from html.parser import HTMLParser


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


class JsonMLElement(BaseElement):
    """Class that generates xml elements from jsonml."""
    def __init__(self, source, **extra):
        """Constructs from jsonml source."""
        self._jsonml = self.extract_element(source)
        self.elementname = self._jsonml.tagname
        self._jsonml.attributes.update(extra)
        super(JsonMLElement, self).__init__(**extra)

    def extract_element(self, e):
        """Extract AttrDict from jsonml

        This function non-recursively extracts an AttrDict from jsonml.
        This AttrDict has the three elements tagname, attributes and
        element_list according to the jsonml specification.

        :param e: element as jsonml list/tuple
        :return: AttrDict
        """
        if not isinstance(e, (list, tuple)):
            raise ValueError("JsonML must be a list")
        if len(e) == 0:
            raise ValueError("JsonML cannot be an empty list")
        if not isinstance(e[0], string_types):
            raise ValueError("JsonML tagname must be string")
        ret = AttrDict({"tagname": e[0], "attributes": {}, "element-list": []})
        if len(e) > 1:
            if isinstance(e[1], dict):
                ret.attributes = e[1]
                if len(e) > 2:
                    ret.element_list = e[2:]
            else:
                ret.element_list = e[1:]
        return ret

    def get_xml_element(self, e):
        """Generate xml element from jsonml AttrDict

        Recursively generates xml element from jsonml AttrDict.

        :param e: jsonml AttrDict
        :return: xml element
        """

        # create element
        element = etree.Element(e.tagname)
        # set element attributes
        for attribute, value in sorted(e.attributes.items()):
            # filter 'None' values
            if value is not None:
                value = self.value_to_string(value)
                if value:  # just add not empty attributes
                    element.set(attribute, value)
        # store the last xml sibling, because we may need to add
        # text to it's tail. This is to support the tagged text
        # style ("<tspan>a<tspan>b</tspan>c</tspan>")
        last = None
        for c in e.element_list:
            if isinstance(c, string_types):
                # Strings need special treatment for insertion
                # as those are not elements
                if last is None:
                    # No non-text element seen so far
                    if element.text is None:
                        # No other element seen so far
                        element.text = c
                    else:
                        # Append to other texts
                        element.text += c
                else:
                    # There was an element already
                    if last.tail is None:
                        # No text after that so far
                        last.tail = c
                    else:
                        # Append to other text
                        last.tail += c
            else:
                # Recurse
                last = self.get_xml_element(self.extract_element(c))
                element.append(last)

        return element

    def get_xml(self):
        return self.get_xml_element(self._jsonml)