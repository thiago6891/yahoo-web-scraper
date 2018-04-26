from html.parser import HTMLParser


class PageParser(HTMLParser):
    def __init__(self):
        super(PageParser, self).__init__()
        self._in_trow = False
        self._in_tcol = False
        self._data = []
    
    def feed(self, html):
        price_str = 'regularMarketPrice":{"raw":'
        start_idx = html.find(price_str) + len(price_str)
        end_idx = html.find(',', start_idx)
        self._price = float(html[start_idx:end_idx])
        
        super(PageParser, self).feed(html)
    
    def handle_starttag(self, tag, attributes):
        if tag == 'tr':
            self._data.append([])
        elif tag == 'td':
            self._in_tcol = True
    
    def handle_data(self, data):
        if self._in_tcol and data != '+':
            self._data[-1].append(data)
        
    def handle_endtag(self, tag):
        if tag == 'tr':
            if len(self._data[-1]) == 0:
                self._data.pop()
            else:
                self._data[-1].append(self._price)
        
        if tag == 'td':
            self._in_tcol = False
    
    @property
    def data(self):
        return self._data
    
    @property
    def price(self):
        return self._price