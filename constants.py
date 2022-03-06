re_exp = {
    'SITE_REGEX': r"(?P<scheme>https?://)?(?P<host>(?:\S+.)?9anime\.(?:to|id|club|center))/?(?P<watch>watch)?/?(?P<slug>[-a-zA-Z0-9]+)\.?(?P<id>[-a-zA-Z0-9]+)?/?(?:ep-(?P<ep>[0-9]+))?",
    
    'VIDSTREAM_RE': r"(?P<scheme>https?://)?(?P<host>(?:\S+.)?(?:vidstreamz|vidstream|vizcloud2)\.(?:online|pro))/(?:embed|e)/(?P<id>[A-Z0-9]+)",

    'MCLOUD_RE': r"(?P<scheme>https?://)?(?P<host>(?:\S+.)?mcloud\.to)/(?:embed|e)/(?P<id>[a-zA-Z0-9]+)",

    'VIDEOVARD_RE': r"(?P<scheme>https?://)?(?P<host>(?:\S+.)?videovard\.(?:sx|to))/[ved]/(?P<id>[a-zA-Z0-9]+)",

    'STREAMTAPE_RE': r"(?P<scheme>https?://)?(?P<host>(?:\S+.)?s(?:tr)?(?:eam)?(?:ta?p?e?|cloud)\.(?:com|cloud|net|pe|site|link|cc|online))/(?:e|v)/(?P<id>[a-zA-Z0-9]+)",

    'MP4UPLOAD_RE': r"(?P<scheme>https?://)?(?P<host>(?:\S+.)?mp4upload\.com)/(?:embed-)?(?P<id>[a-zA-Z0-9]+)",
}