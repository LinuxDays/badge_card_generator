#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import argparse


def template_to_linked(infile, outfile, linktarget="dummy.svg#layer1"):
    """Edit SVG file. Replace all occurrences of rectangles with use tags
    linking (part of) to another SVG file.

    Parameters:
    infile -- path to input SVG file
    outfile -- path to output SVG file
    linktarget -- target of the use tags, like "/path/to/file.svg#layer1"
    """

    tpl = ET.parse(infile)
    ns = {
            'svg': 'http://www.w3.org/2000/svg',
            'xlink': 'http://www.w3.org/1999/xlink',
         }
    rects = tpl.findall('.//svg:rect', ns)
    for r in rects:
        r.tag = '{http://www.w3.org/2000/svg}use'
        r.attrib.pop('style')
        r.set('{{{}}}href'.format(ns['xlink']), linktarget)
    with open(outfile, 'wb') as outf:
        tpl.write(outf, encoding='utf-8', xml_declaration=True)


def main():
    parser = argparse.ArgumentParser(description="Create template with "
                                     "rectangles replaced by links "
                                     "to other SVG documents.")
    parser.add_argument("infile", help="input file name with rectangles "
                        "in place of the links")
    parser.add_argument("outfile", help="where to write output file")
    parser.add_argument("link", help="target to be linked "
                        "(default: \"%(default)s\")", nargs="?",
                        default="dummy.svg#layer1")
    args = parser.parse_args()
    template_to_linked(args.infile, args.outfile, args.link)

if __name__ == "__main__":
    main()
