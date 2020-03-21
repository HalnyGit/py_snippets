from xml.etree import ElementTree

with open('ClientTrades.xml', 'rt') as f:
	tree = ElementTree.parse(f)

root = tree.getroot()

print root.tag
print root.attrib


	