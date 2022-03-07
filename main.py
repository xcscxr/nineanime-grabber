from __future__ import print_function, unicode_literals

import re
from utils import getVrf
from parsers import search
from utils import (
    gen_client, 
    get_server_link, 
    get_dl, 
    parse_servers, 
    parse_episodes,
    select,
    rawselect,
    text_input
)
from constants import re_exp

# -----------------------------------------------------------------------

def finder(query: str, **kwargs):
    data = search(query, **kwargs)

    if not data['success']:
        return print(data['content'])
    
    if not len(data['content']):
        return print('Nothing found')
    
    item_choices = []
    choice_lookup = {}
    for num, item in data['content'].items():
        choice = f"{item['title']} [{item['info']}]"
        item_choices.append(choice)
        choice_lookup[choice] = num
    
    item = rawselect('Select an item:', item_choices).ask()
    item_input = choice_lookup[item]
    
    item = data['content'][int(item_input)]

    handle_url({'scheme': 'https://', 'host': '9anime.to', 'id': item['id']})

# -----------------------------------------------------------------------

def handle_url(c):
    invalid_msg = 'Invalid URL.'
    if 'scheme' not in c or not c['scheme']: c['scheme'] = 'http://'
    client = gen_client(referer=f"{c['scheme']}{c['host']}")

    url = f"{c['scheme']}{c['host']}/ajax/anime/servers"
    
    if 'id' not in c:
        return print(invalid_msg)
    try:
        vrf = getVrf(c['id'])
    except: return print(invalid_msg)
    
    params = {
        'id': c['id'],
        'vrf': vrf
    }
    
    res = client.get(url, params=params)
    if res.status_code == 404:
        return print(invalid_msg)
    
    servers, server_choices, server_lookup = parse_servers(res.json()['html'])
    episodes = parse_episodes(res.json()['html'])
    
    serverid_input = select('Select server:', server_choices).ask()
    serverid_input = server_lookup[serverid_input]
    
    episode_input = text_input('Enter episode number:').ask()

    server_link = get_server_link(episode_input, serverid_input, episodes, servers, c)
    
    print(f"\n\033[93m== [SERVER LINK] ==\033[0m")
    print('\033[93m'+server_link+'\033[0m')
    
    try: dl = get_dl(server_link, serverid_input, servers)
    except:
        print(f"\n\033[91m[ERROR]: Failed to fetch stream, retry with a different server\033[0m")
        return
    
    print(f"\n\033[92m== [DIRECT LINK] ==\033[0m")
    print('\033[92m'+dl+'\033[0m')
    
# -----------------------------------------------------------------------

def run():
    REGEX = re.compile(re_exp['SITE_REGEX'])
    query = text_input('Enter a query or a URL:').ask()

    match = REGEX.search(query)
    if match:
        c = match.groupdict()
        handle_url(c)
    else:
        finder(query)

if __name__ == "__main__":
    run()
