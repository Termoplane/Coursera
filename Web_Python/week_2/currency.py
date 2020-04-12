from bs4 import BeautifulSoup
from decimal import Decimal

def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp', {'date_req':date})  # Использовать переданный requests

    soup = BeautifulSoup(response.content, 'lxml')

    rates = {
        valute.charcode.string: (
            Decimal(valute.value.string.replace(',', '.')),
            int(valute.nominal.string)
        )
        for valute in soup('valute')
    }

    rates['RUR'] = (Decimal(1), 1)

    result =  amount * rates[cur_from][0] * rates[cur_to][1] / rates[cur_from][1] / rates[cur_to][0]
        
    return result.quantize(Decimal('.0001'))