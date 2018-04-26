import csv
from datetime import datetime
from urllib.request import urlopen

from page_parser import PageParser
from symbols_reader import SymbolsReader


OPTIONS_FILE_HEADER = [
    'Contract Name',
    'Last Trade Date',
    'Strike',
    'Last Price',
    'Bid',
    'Ask',
    'Change',
    'Change %',
    'Volume',
    'Open Interest',
    'Implied Volatility',
    'Stock Price',
]

ERRORS_FILE_HEADER = ['Symbol', 'Stock Price/Error']

BASE_URL = 'https://finance.yahoo.com/quote/{}/options?ltr=1'


def format_filename(name, date):
    return '{}_{}.csv'.format(name, date.strftime('%Y%m%d'))


if __name__ == '__main__':
    now = datetime.now()
    options_file = open(format_filename('options', now), 'w', newline='')
    errors_file = open(format_filename('errors', now), 'w', newline='')
    
    options_writer = csv.writer(options_file)
    errors_writer = csv.writer(errors_file)

    options_writer.writerow(OPTIONS_FILE_HEADER)
    errors_writer.writerow(ERRORS_FILE_HEADER)

    for sym in SymbolsReader.get_symbols():
        try:
            url = BASE_URL.format(sym)
            
            print('Opening', url)
            response = urlopen(url)
            
            print('Decoding HTML...')
            html = response.read().decode('utf-8')
            
            print('Parsing page...')
            parser = PageParser()
            parser.feed(html)

            if parser.data:
                for row in parser.data:
                    options_writer.writerow(row)
            else:
                errors_writer.writerow([sym, parser.price])
        except Exception as e:
            errors_writer.writerow([sym, e])
    
    options_file.close()
    errors_file.close()
