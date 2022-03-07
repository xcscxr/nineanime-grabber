import re
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
from utils import tear_decode, gen_client
from constants import re_exp


# ============================================================

client = gen_client(referer='https://9anime.to/')

# ============================================================

def match_pattern(regex, url):
    pattern = re.compile(regex)
    match = pattern.search(url)
    c = match.groupdict()
    return match, c

# ============================================================

def vidstream(url: str):
    match, c = match_pattern(re_exp['VIDSTREAM_RE'], url)
    info_url = f"{c['scheme']}{c['host']}/info/{c['id']}"
    h = {'referer': url}
    data = client.get(info_url, headers=h).json()
    if 'media' in data:
        return data['media']['sources'][-1]['file']
    return False

# ============================================================

def mycloud(url: str):
    match, c = match_pattern(re_exp['MCLOUD_RE'], url)
    info_url = f"{c['scheme']}{c['host']}/info/{c['id']}"
    h = {'referer': url}
    data = client.get(info_url, headers=h).json()
    if 'media' in data:
        return data['media']['sources'][-1]['file']
    return False

# ============================================================

def videovard(url: str): # excluding ref headers
    match, c = match_pattern(re_exp['VIDEOVARD_RE'], url)
    url = f"https://{c['host']}/api/make/hash/{c['id']}"
    res = client.get(url).json()
    hash = res['hash']
    url = f"https://{c['host']}/api/player/setup"
    data = {
        'cmd': 'get_stream',
        'file_code': c['id'],
        'hash': hash
    }
    res = client.post(url, data=data).json()
    url = tear_decode(res['src'], res['seed'])
    return url

# ============================================================

def streamtape(url: str):
    match, c = match_pattern(re_exp['STREAMTAPE_RE'], url)
    url = f"https://{c['host']}/e/{c['id']}"
    res = client.get(url).text
    src = re.findall(r'''ById\('.+?=\s*(["']//[^;<]+)''', res)
    src_url = ''
    parts = src[-1].replace("'", '"').replace(' ', '').split('+')
    for part in parts:
        p1 = re.findall(r'"([^"]*)"', part)[0]
        p2 = 0
        if 'substring' in part:
            subs = re.findall(r'substring\((\d+)', part)
            for sub in subs:
                p2 += int(sub)
        src_url += p1[p2:]
    src_url += '&stream=1'
    src_url = 'https:' + src_url if src_url.startswith('//') else src_url
    res = client.head(src_url)
    print(src_url+'\n')
    src_url = res.headers.get('Location')
    return src_url

# ============================================================

def mp4upload(url: str): # incomplete :(
    match, c = match_pattern(re_exp['MP4UPLOAD_RE'], url)
    
    url = f"{c['scheme']}{c['host']}/{c['id']}"
    
    client = requests.Session()
    h = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'referer': url,
    }
    client.headers.update(h)
    
    res = client.get(url, verify=True)
    
    bs4 = BeautifulSoup(res.content, 'lxml')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }
    
    res = client.post(url, data=data, verify=True)
    
    bs4 = BeautifulSoup(res.content, 'lxml')
    inputs = bs4.find_all('input')
    data = { input.get('name'): input.get('value') for input in inputs }
    
    res = client.post(url, data=data, verify=False, allow_redirects=False)
    
    url = res.headers.get('Location')
    return url
    
# ============================================================
