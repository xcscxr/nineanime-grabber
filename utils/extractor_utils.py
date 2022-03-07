import json
import vidservers
from utils import gen_client, getLink, process_xpath

# -----------------------------------------------------------------------

def get_server_link(ep_number, server_id, episodes, servers, c):
    client = gen_client(referer=f"{c['scheme']}{c['host']}")
    sourceId = episodes[ep_number][server_id]
    
    url = f"{c['scheme']}{c['host']}/ajax/anime/episode?id={sourceId}"
    res = client.get(url).json()
    
    encryptedURL = res['url']
    
    server_link = getLink(encryptedURL)
    
    return server_link

# -----------------------------------------------------------------------

def get_dl(server_link: str, server_id, servers):
    dl = getattr(vidservers, servers[server_id].lower())(server_link)
    return dl

# -----------------------------------------------------------------------

def parse_servers(data: str):
    # server_id [ {server_id: server_name},... ]
    servers = process_xpath("//*[contains(@id, 'server')]", data)
    server_id = {}
    server_choices = []
    server_lookup = {}
    for server in servers:
        server_name = server.text_content().strip()
        id = server.get('data-id')
        server_id[id] = server_name
        server_choices.append(server_name)
        server_lookup[server_name] = id

    return server_id, server_choices, server_lookup

# -----------------------------------------------------------------------

def parse_episodes(data: str):
    # [ ep_num: { server_id: 'episode_id',... },... ]
    episodes_parsed = {}
    episodes = process_xpath("//a[@data-sources]", data)
    for ep in episodes:
        episodes_parsed[ep.get('data-base')] = json.loads(ep.get('data-sources'))
    
    return episodes_parsed
    
# -----------------------------------------------------------------------
