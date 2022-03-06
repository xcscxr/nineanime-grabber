from utils import (
    getVrf,
    process_xpath,
    gen_client
)

# -----------------------------------------------------------------------

def ret(success: bool, content):
    return {'success': success, 'content': content}

# -----------------------------------------------------------------------

def parse_search_results(data: str, view_all = False):    
    xpath_chunk = "//ul[@class='anime-list']" if view_all else ""
    links = process_xpath(xpath_chunk+'//a[./img]', data)
    images = process_xpath(xpath_chunk+'//a/img', data)
    title = process_xpath(xpath_chunk+'//*[@data-jtitle]', data)
    
    if view_all:
        info_bits = process_xpath(xpath_chunk+"//a[@class='poster']", data)
    else:
        info_bits = process_xpath("//a//div[@class='info']/span", data)
        
    search_results_parsed = {}
    
    count = 0
    for i in range(0, len(links)):
        obj = {
            'id': links[i].get('href').split('.')[-1],
            'link': links[i].get('href'),
            'title': title[i].text_content().replace('  ',' ').strip(),
            'info': info_bits[i].text_content().replace('  ',' ').strip(),
            'image': images[i].get('src'),
        }
        search_results_parsed[count] = obj
        count += 1
        
    return search_results_parsed
    
# -----------------------------------------------------------------------

def search_filter():
    pass

# -----------------------------------------------------------------------

def search(keyword: str, view_all = False, limit = 99):
    client = gen_client(referer='https://9anime.to/')
    
    url = 'https://9anime.to/ajax/anime/search'
    if view_all: url = 'https://9anime.to/search'
    
    params = {
        'vrf': getVrf(keyword),
        'keyword': keyword
    }
    
    if view_all:
        h = {'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest'}
    else:
        h = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'referer': url}
        
    res = client.get(url, params=params, headers=h)
    
    if not view_all:
        try: data = res.json()['html']
        except: return ret(False, 'Something went wrong.')
    else:
        data = res.text

    if not data.strip(): return ret(False, 'No results found.')
    
    data = parse_search_results(data, view_all)
    
    return ret(True, data)
