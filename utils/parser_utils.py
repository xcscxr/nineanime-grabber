from lxml import html
import requests

# -----------------------------------------------------------------------

def gen_client(**kwargs):
    client = requests.Session()
    h_global = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0',
        **kwargs
    }
    client.headers.update(h_global)
    return client

# -----------------------------------------------------------------------

def process_xpath(xpath_str: str, data: str, raw = True):
    if not raw: return  data.xpath(xpath_str)
    doc = html.fromstring(data)
    return doc.xpath(xpath_str)

