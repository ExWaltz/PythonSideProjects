import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup


class YoutubeSearch:
    def __init__(self, search_yt):
        self.search_val = search_yt
        self.delimiter = ":`~|"
        self.main()

    def getChnl(self):
        # Channel results
        open_chnl_file = open('searchChnl.log', 'w', encoding='utf-8')
        jsn_chnl_id = self.jsn_chnl_id.get('channelId')
        jsn_chnl_title = self.jsn_sec_list[0].get(
            'channelRenderer').get('title').get('simpleText')
        jsn_chnl_thmb = self.jsn_sec_list[0].get('channelRenderer').get(
            'thumbnail').get('thumbnails')[0].get('url')
        jsn_chnl_thmb = str(jsn_chnl_thmb)[2:]
        open_chnl_file.write(
            f"{jsn_chnl_title}{self.delimiter}{jsn_chnl_thmb}{self.delimiter}www.youtube.com/channel/{str(jsn_chnl_id)}\n")
        open_chnl_file.close()

    def getVids(self, parent_jsn):
        try:
            # Get Video Owner
            search_vid_chnl_name = parent_jsn.get(
                'ownerText').get('runs')[0].get('text')
            search_vid_chnl_id = parent_jsn.get('ownerText').get('runs')[0].get(
                'navigationEndpoint').get('commandMetadata').get('webCommandMetadata').get('url')
            # Get Videos
            search_vid_id = parent_jsn.get('videoId')
            search_vid_thmb = parent_jsn.get(
                'thumbnail').get('thumbnails')[0].get('url')
            search_vid_thmb = str(search_vid_thmb)[8:]
            search_vid_title = parent_jsn.get(
                'title').get('runs')[0].get('text')
            # Check if Live Stream
            if parent_jsn.get('publishedTimeText') is None:
                # Get Live Stream Info
                try:
                    if parent_jsn.get('badges')[0].get('metadataBadgeRenderer').get('label') == 'LIVE NOW':
                        print('Live Now')
                        search_vid_date = parent_jsn.get('badges')[0].get(
                            'metadataBadgeRenderer').get('label')
                        search_vid_views = parent_jsn.get(
                            'viewCountText').get('runs')[0].get('text')
                        search_vid_length = parent_jsn.get(
                            'viewCountText').get('runs')[1].get('text')
                    elif parent_jsn.get('upcomingEventData') is not None:
                        print('Upcoming')
                        search_vid_date = parent_jsn.get(
                            'upcomingEventData').get('startTime')
                        search_vid_date = datetime.fromtimestamp(
                            int(search_vid_date))
                        search_vid_views = "Upcoming"
                        search_vid_length = "Live Stream"
                except Exception:
                    # Youtube upload music videos is confusing
                    search_vid_date = "Unspecified"
                    search_vid_views = parent_jsn.get(
                        'viewCountText').get('simpleText')
                    search_vid_length = parent_jsn.get(
                        'lengthText').get('simpleText')
            else:
                # Get Video Info
                search_vid_date = parent_jsn.get(
                    'publishedTimeText').get('simpleText')
                search_vid_views = parent_jsn.get(
                    'viewCountText').get('simpleText')
                search_vid_length = parent_jsn.get(
                    'lengthText').get('simpleText')
            # Seperator :`| for sorting data ;)
            self.open_file.write(
                f"{search_vid_chnl_name}{self.delimiter}www.youtube.com{str(search_vid_chnl_id)}{self.delimiter}{search_vid_title}{self.delimiter}{str(search_vid_thmb)}{self.delimiter}www.youtube.com/watch?v={str(search_vid_id)}{self.delimiter}{search_vid_date}{self.delimiter}{search_vid_views}{self.delimiter}{search_vid_length}\n")

        except Exception:
            raise Exception
            # Reset either because of slow net or I messed up
            return self.main()

    def main(self):
        self.open_file = open('searchRaw.log', 'w', encoding='utf-8')
        self.search_val = str(self.search_val).replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={self.search_val}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'lxml')
        script_list = soup.find_all('script')
        # real_script = str(script_list[32])

        # Debuging
        # debug_raw = open('html_raw.log', 'w', encoding='utf-8')
        # for sc in script_list:
        #     debug_raw.write(str(sc))
        #     debug_raw.write("\n\n\n")
        # debug_raw.close()

        for sc in script_list:
            if str(sc).find("responseContext") != -1:
                real_script = str(sc)
                break

        real_script = real_script[59:-10]
        self.open_file.write(real_script)
        self.open_file.close()
        # Debuging Purposes
        self.open_file = open('searchRaw.log', 'r', encoding='utf-8')
        hold_jsn = self.open_file.read()
        self.open_file.close()
        self.open_file = open('search.log', 'w', encoding='utf-8')
        jsn = json.loads(hold_jsn)
        jsn_fir_list = jsn['contents'].get('twoColumnSearchResultsRenderer').get(
            'primaryContents').get('sectionListRenderer').get('contents')
        self.jsn_sec_list = jsn_fir_list[0].get(
            'itemSectionRenderer').get('contents')
        self.jsn_chnl_id = self.jsn_sec_list[0].get('channelRenderer')

        if self.jsn_chnl_id is not None:
            print('channel found')
            self.getChnl()
        else:
            open_chnl_file = open('searchChnl.log', 'w', encoding='utf-8')
            open_chnl_file.write("")
            open_chnl_file.close()

        for search_result in self.jsn_sec_list:
            search_hold = search_result
            search_chnl_shelf = search_hold.get('shelfRenderer')
            search_vid_hold = search_hold.get('videoRenderer')

            if search_chnl_shelf is not None:
                print('found Channel vid')
                search_chnl_shelf_vids = search_chnl_shelf.get(
                    'content').get('verticalListRenderer').get('items')

                for shelf_item in search_chnl_shelf_vids:
                    shelf_hold_item = shelf_item.get('videoRenderer')

                    if shelf_hold_item is not None:
                        self.getVids(shelf_hold_item)

            if search_vid_hold is not None:
                self.getVids(search_vid_hold)

        self.open_file.close()


if __name__ == '__main__':
    query = input("Search:\t") 
    YoutubeSearch(str(query))
