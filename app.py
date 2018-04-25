from html.parser import HTMLParser
from urllib.request import urlopen


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
        if tag == 'tr' and len(self._data[-1]) == 0:
            self._data.pop()
        
        if tag == 'tr' and len(self._data) > 0:
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


if __name__ == '__main__':
    symbols = ['QD', 'MSFT', 'GOOG', 'TSLA', 'QQQ', 'GRVY']

    for sym in symbols:
        url = 'https://finance.yahoo.com/quote/' + sym + '/options?ltr=1'
        print('Opening', url)
        response = urlopen(url)
        print('Decoding HTML...')
        html = response.read().decode('utf-8')
        print('Parsing page...')
        parser = PageParser()
        parser.feed(html)

        print('Data for symbol', sym)
        for d in parser.data:
            print(d)
        print(parser.price)
