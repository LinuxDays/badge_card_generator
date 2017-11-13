Batch business card/badge templater
===================================

This Python script can be used to template business cards/badges to
be printed on a special paper, like those produced by
`Avery Zweckform`_. It was designed after
a few hours of frustration caused by trying to use the official Flash-based
design app.

Developed and used on Linux. Some Python (3.4+) knowledge is necessary, as there is a lot of variables and it would be cubersome to try to cover all of them by options. Apart from that, you need:

 - Inkscape (for designing and batch converting SVG to PDF)
 - ``pdfunite`` (for unifying PDF files into one; from Poppler package)

.. _Avery Zweckform: http://www.avery-zweckform.cz/

How to use
----------

Prepare the badge template
**************************

Use supplied files ``linuxdays-badge.svg`` and ``eduguest-card-template.svg`` as a sample. 

Create similar using Inkscape or any other editor. Make sure the document dimensions matches exactly the label dimension specified by vendor. For variable texts, usage of *Flowing text* is recommended as there is automatic line wrapping and overflowed text is cropped automatically. Always make enough room to accommodate the longest label.

Finally, change the ``id=`` attributes of elements with variable content to some reasonable name like ``name``, ``role``, etc.

If you want to concatenate two source fields into one label (like combining given name and surname into one field), use consecutive ``<tspan>`` tags like this:

::

  <tspan id="gn">GivenName</tspan><tspan> </tspan><tspan id="sn">Surname</tspan>

You should also prepare a *dummy* badge template, that would be used in case when number of badges to print would be less than number of labels on the sheet. As the vendor does not recommend printing the sheets more than once, it's advisable to prepare those *dummy* badges for something useful, like hand-written badges for last-moment registrations.

Prepare the sheet template
**************************

In case you want to use another sheet type, you need to customize sheet template. For Avery sheets, a Microsoft Word template can be downloaded from the vendor. It defines exact positions of the labels. Use this to create a SVG file containing a ``rect`` object on each position, with ``id=`` attribute named  ``pos0`` to ``posN``. Number the labels from top to bottom first, then from left to right. Also add a text field outside the labels with attribute ``id="annotation"``, that will be used for annotating the sheet.

After that, use provided ``template_to_linked.py`` utility to convert the template into a linked SVG, where each rectangle is replaced with a hyperlink linking the badge template created earlier.

::

  ./template_to_linked.py avery-L4784-template.svg avery-L4784-linked.svg 'linuxdays-badge-dummy.svg#layer1'

Prepare the source data
***********************

For source data, anything can be used as long as you are able to read it into Python. In provided examples, there is a tab-separated-values file ``linuxdays-badges.tsv``, that is read using Python csv_ module and a semicolon-separated-values file ``eduguest-accounts.txt`` read directly by Python code.

.. _csv: https://docs.python.org/3/library/csv.html

In the end, it's necessary to read the data into the list of `Named tuples`__ where each field name corresponds with the ``id`` attribute of SVG file that should be replaced. 

.. __: https://docs.python.org/3/library/collections.html#collections.namedtuple

Customize and run the script
****************************

Finally, adjust file names and number of rows in the main script ``linuxdays_badge_generator.py``:

 - adjust ``Record`` named tuple definition to define all the ``id`` attributes that should be templated
 - adjust names of input file and output path
 - adjust *dummy* badge name (please note that the path should be relative to the output directory)
 - adjust ``rows`` variable which defines number of rows sheets will be arranged to (this affects ordering of the labels)
 - run it!
 - make sure the resulting PDF is printed **without any scaling**. The labels ``TOP EDGE`` and ``LEFT EDGE`` should be touching edges of the sheet and therefore cropped by the printer.
