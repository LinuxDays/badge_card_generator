#!/usr/bin/env python3

import os
import csv
import unicodedata
import re
from collections import namedtuple

import svgtemplate

Record = namedtuple('Record', ['name', 'role'])


def cardnamegen(record):
    slug = "{}-{}".format(record.name, record.role)
    slug = unicodedata.normalize('NFKD', slug)
    slug = slug.encode('ascii', 'ignore').decode('ascii').lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    return "card-{}.svg".format(slug)


def getrecords(f):
    with open(f, "r") as inf:
        reader = csv.DictReader(inf, dialect='excel-tab')
        for row in reader:
            name, role = (row[_].strip() for _ in ['name', 'role'])
            yield Record(name, role)


def main():
    infile = "linuxdays-badges.tsv"
    outdir = "./out/"
    rows = 2
    sheettpl = svgtemplate.SVGTemplate('avery-L4784-linked.svg', outdir)
    cardtpl = svgtemplate.SVGTemplate('linuxdays-badge.svg', outdir)
    cardtpl.fnamegen = cardnamegen
    cards = []

    print("Templating cards…")
    for rec in getrecords(infile):
        fname = cardtpl.templatetext(rec)
        cards.append(fname)
    cards = svgtemplate.reordercards(cards,
                                     dummycard='../linuxdays-badge-dummy.svg',
                                     rows=rows)

    print("Creating layouts…")
    sheets = svgtemplate.gensheets(cards, sheettpl, rows=rows)
    print("Converting to pdf…")
    os.chdir(outdir)
    svgtemplate.pdfsheets(sheets)
    print("Joining all together…")
    svgtemplate.pdfunite(sheets, 'linuxdays-badges-output.pdf')


if __name__ == "__main__":
    main()
