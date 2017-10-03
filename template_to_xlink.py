import xml.etree.ElementTree as ET
tpl = ET.parse('avery-L4784-template.svg')
ns = {'svg': 'http://www.w3.org/2000/svg', 'xlink':'http://www.w3.org/1999/xlink'}
rects = tpl.findall('.//svg:rect', ns)
for r in rects:
 r.tag = '{http://www.w3.org/2000/svg}use'
 r.attrib.pop('style')
 r.set('{{{}}}href'.format(ns['xlink']), 'linuxdays-badge-dummy.svg#layer1')
with open('templatexlink.svg', 'wb') as outf:
 tpl.write(outf, encoding='utf-8', xml_declaration=True)
