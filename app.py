from html.parser import HTMLParser
from urllib.request import urlopen


class PageParser(HTMLParser):
    def __init__(self):
        super(PageParser, self).__init__()
        self._in_tbody = False
        self._in_trow = False
        self._in_tcol = False
        self._data = []
    
    def handle_starttag(self, tag, attributes):
        if tag == 'tbody':
            self._in_tbody = True
        elif tag == 'tr':
            self._in_trow = True
            self._data.append([])
        elif tag == 'td':
            self._in_tcol = True
    
    def handle_data(self, data):
        if self._in_tcol:
            self._data[-1].append(data)
        
    def handle_endtag(self, tag):
        if tag == 'tbody':
            self._in_tbody = False
        elif tag == 'tr':
            self._in_trow = False
        elif tag == 'td':
            self._in_tcol = False


if __name__ == '__main__':
    response = urlopen('http://finance.yahoo.com/q/op?s=QD')
    html = response.read().decode('utf-8')
    parser = PageParser()
    parser.feed(html)
    for d in parser._data:
        print(d)
