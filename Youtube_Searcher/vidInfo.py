import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import pytz


# This code below only works for http://www.youtube.com/watch?v=XXXXXXXXX links.
# 
def _get_vid_info(vid_link):
    response = requests.get(vid_link).text
    soup = BeautifulSoup(response, 'lxml')
    script_list = soup.find_all('script')

    if str(vid_link).endswith('/'): vid_link = vid_link[:-1]
    vid_id = str(vid_link).split('/')[-1]

    for sc in script_list:
        if str(sc).find("responseContext") != -1:
            real_script = str(sc)   # Find the correct script that contains video informations
            break

    real_script = real_script[69:-10]   # Remove uncessary text and convert to json ready text
    with open(f"{str(vid_id).replace('watch?v=', '')}.log", "w", encoding="utf-8") as debug_sc:
        debug_sc.write(str(real_script))
    jsn = json.loads(real_script)

    vid_title = jsn.get('videoDetails').get('title')
    vid_date = jsn.get('microformat').get('playerMicroformatRenderer').get('publishDate')
    vid_views = jsn.get('videoDetails').get('viewCount')
    vid_length = jsn.get('videoDetails').get('lengthSeconds')
    vid_thumb = jsn.get('videoDetails').get('thumbnail').get('thumbnails')[-1].get('url')
    vid_type = "DEFAULT"
    vid_owner = jsn.get('videoDetails').get('author')

    if jsn.get('videoDetails').get('isLive'):
        vid_type = "LIVE"
    elif jsn.get('videoDetails').get('isUpcoming'):
        vid_type = "UPCOMING"

    return {vid_link: [vid_title, vid_date, vid_views, vid_length, vid_thumb, vid_type, vid_owner]}


if __name__ == '__main__':
    query = input("Search:\t") 
    upcom = _get_vid_info(str(query))
    print(upcom)
