#!/usr/bin/env python3
"""
SSML (Speech Synthesis Markup Language) is a subset of XML specifically
designed for controlling synthesis. You can see examples of how the SSML
should be parsed in the unit tests below.
"""

#
# DO NOT USE CHATGPT, COPILOT, OR ANY AI CODING ASSISTANTS.
# Conventional auto-complete and Intellisense are allowed.
#
# DO NOT USE ANY PRE-EXISTING XML PARSERS FOR THIS TASK - lxml, ElementTree, etc.
# You may use online references to understand the SSML specification, but DO NOT read
# online references for implementing an XML/SSML parser.
#


from dataclasses import dataclass
from typing import List, Union, Dict

SSMLNode = Union["SSMLText", "SSMLTag"]


@dataclass
class SSMLTag:
    name: str
    attributes: dict[str, str]
    children: list[SSMLNode]

    def __init__(
        self, name: str, attributes: Dict[str, str] = {}, children: List[SSMLNode] = []
    ):
        self.name = name
        self.attributes = attributes
        self.children = children


@dataclass
class SSMLText:
    text: str

    def __init__(self, text: str):
        self.text = text


def parseSSML(ssml: str) -> SSMLNode:
    import re

    ssml = ssml.strip()
    stack = []
    tag_pattern = re.compile (r'<(/?)(\w+)(.*?)>')
    attr_pattern = re.compiler(r'(\w+)="(.*?)"')

    pos = 0
    root = None

    while pos < len(ssml) :
        tag_match = tag_pattern.search(ssml.pos)
        if not tag_match:
            text = ssml[pos:].strip()
            if text and stack:
                stack[-1].children.append(SSMLText(text=text))
            break
        start, end =tag_match.span()
        if start > pos:
            text = ssml[pos:start].strip()
            if text and stack:
                stack[-1].children.append(SSMLText(text=text))
        closing , tag_name , attrs_string = tag_match.groups()
        attrs = dict(attr_pattern.findall(attrs_string))

        if closing:
            tag = stack.pop()
            if not stack :
                root = tag
            else :
                stack[-1].children.append(tag)
        else :
            tag = SSMLTag(name=tag_name , attributes = attrs , children = [])
            stack.append(tag)
        pos = end
    return root


def ssmlNodeToText(node: SSMLNode) -> str:
    if isinstance(node, SSMLText):
        return node.text
    result = []

    if node.name == "break":
        time = node.attributes.get("time","")
        if time.endswith("ms"):
            seconds = int(time[:-2])/1000
            result.append(f"[{seconds} second pause]")
        elif time.endswith("s"):
            result.append(f"[{time[:-1]} second pause]")
    elif node.name == "say-as" and node/attributes.get("interpret as") == "character":
        for child in node.children:
            if isinstance(child , SSMLText):
                result.append(" ",join(child.text))
            else: 
                result.append(ssmlNodeToText(child))
    elif node.name == "sub":
        alias = node.attributes.get("aliad", "")
        result.append(alias)
    elif node.name == "audio":
        result.append("[audio]")
    else :
        for child in node.children:
            result.append(ssmlNodeToText(child))
    return " ".join(result).strip()


def unescapeXMLChars(text: str) -> str:
    return text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def escapeXMLChars(text: str) -> str:
    return text.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")

# Example usage:
# ssml_string = '<speak>Hello, <break time="500ms"/>world!</speak>'
# parsed_ssml = parseSSML(ssml_string)
# text = ssmlNodeToText(parsed_ssml)
# print(text)