import zipfile, re

rx_stripxml = re.compile('<[^>*?>', re.DOTALL | re.MULTILINE)

def convert_00(want_text=True):
	data = read('ClientTrades.xml')
	if want_text:
		data = ' '.join(rx_stripxml.sub(' ', data).split())
	return data

print convert_00()


