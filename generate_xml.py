from lxml import etree
from lxml.builder import ElementMaker
import xml.etree.ElementTree as ET

m_root = ElementMaker()

format = m_root.format(
    m_root.child("child1"),
    m_root.child("child2"),
    m_root.child("child3"),
)

root = m_root.XML(
    format,
    type = "formats",
    version = "4"
)

root_w = ET.ElementTree(root)
root_w.write('gen_xml.xml')
# with open('xml_gen.xml', 'w') as xml_file:
#print(etree.tostring(root, encoding='utf-8', xml_declaration=True, pretty_print=True))


