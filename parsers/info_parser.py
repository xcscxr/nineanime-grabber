from utils import gen_client, process_xpath

def get_info(anime_id: str): # todo
    client = gen_client(referer='https://9anime.to')
    url = f"https://9anime.to/ajax/anime/tooltip/{anime_id}"
    
    res = client.get(url)
    
    title = process_xpath("//*[@class='title']", res.text).text_content()
    ep = process_xpath("//*[@class='ep']", res.text).text_content()
    tags = process_xpath("//*[@class='taglist']", res.text).text_content().strip()
    summary = process_xpath("//p", res.text).text_content()
    watch_url = process_xpath("//*[@class='watch']", res.text).get('href')
    meta = process_xpath("//*[@class='meta']", res.text).text_content()
    
    print(title)
    print(ep)
    print(tags)
    print(summary)
    print(watch_url)
    print(meta)
    