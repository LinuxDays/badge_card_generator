#!/usr/bin/env python3

import os
import fileinput
from collections import namedtuple

import svgtemplate

Account = namedtuple('Account', ['gn', 'sn', 'uid', 'password', 'validity'])


def main():
    outdir = "./out/"
    sheettpl = svgtemplate.SVGTemplate('avery-L4727-linked.svg', outdir)
    cardtpl = svgtemplate.SVGTemplate('eduguest-card-template.svg', outdir)
    cardtpl.fnamegen = lambda act: "card-{}.svg".format(act.uid)
    cards = []

    print("Templating cards…")
    delim = "; "
    for line in fileinput.input():
        if delim not in line:
            continue
        sn, gn, _, uid, password, validto, *_ = line.rstrip().split(delim)
        act = Account(gn, sn, uid, password, validto)
        print(act)
        fname = cardtpl.templatetext(act)
        cards.append(fname)

    print("Creating layouts…")
    sheets = svgtemplate.gensheets(cards, sheettpl,
                                   '../eduguest-card-dummy.svg',
                                   rows=1, ncards=10)
    print("Converting to pdf…")
    os.chdir(outdir)
    svgtemplate.pdfsheets(sheets)
    print("Joining all together…")
    svgtemplate.pdfunite(sheets, 'eduguest-cards-output.pdf')


if __name__ == "__main__":
    main()
