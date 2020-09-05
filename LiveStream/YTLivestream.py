import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime


class SearchEvents:
    def __init__(self):
        self.num_Tries = 0
        self.max_Tries = 3
        self.compInfo = []

    def _ExtractJson(self, URL_, SCRIPT_NUM_):
        try:
            response = requests.get(str(URL_)).text
            soup = BeautifulSoup(response, 'lxml')
            extract_jsn = soup.find_all('script')[SCRIPT_NUM_]
            extract_jsn = str(extract_jsn)[39:-119]
            hold_jsn = extract_jsn
            jsn_res = json.loads(hold_jsn)
            return jsn_res
        except Exception:
            raise Exception
            return self._ExtractJson(URL_, SCRIPT_NUM_)

    def _FindChannel(self, URL_):
        jsn = self._ExtractJson(URL_, 26)
        chnls_found = jsn.get('contents').get('twoColumnSearchResultsRenderer').get('primaryContents').get(
            'sectionListRenderer').get('contents')[0].get('itemSectionRenderer').get('contents')
        for each_chnls_found in chnls_found:
            if each_chnls_found.get('channelRenderer') is not None:
                results_chnl_id = each_chnls_found.get(
                    'channelRenderer').get('channelId')
                results_chnl_id = f"https://www.youtube.com/channel/{str(results_chnl_id)}"
                self.results_chnl_name = each_chnls_found.get(
                    'channelRenderer').get('title').get('simpleText')
                self.results_chnl_url = each_chnls_found.get("channelRenderer").get(
                    "navigationEndpoint").get("commandMetadata").get("webCommandMetadata").get("url")
                self.results_chnl_thmb = each_chnls_found.get("channelRenderer").get(
                    "thumbnail").get("thumbnails")[1].get('url')
                self.isFound = True
                self._GetChnlVids(results_chnl_id)
            elif self.num_Tries < self.max_Tries and not self.isFound:
                # Sometimes Channel doesn't show up so we try again
                self.num_Tries += 1
                return self._FindChannel(URL_)
            else:
                # Reset Tries
                self.num_Tries = self.max_Tries - self.max_Tries
                return

    # Get Only Upcoming and Live events
    def _GetVidInfo(self):
        try:
            for each_jsn in self.jsn_info:
                hold_each_jsn = each_jsn.get('videoRenderer')
                if each_jsn.get('videoRenderer'):
                    hold_each_jsn = each_jsn.get('videoRenderer')
                elif each_jsn.get('gridVideoRenderer'):
                    hold_each_jsn = each_jsn.get('gridVideoRenderer')
                if hold_each_jsn:
                    if hold_each_jsn.get('publishedTimeText') is None:
                        vid_title = hold_each_jsn.get(
                            'title').get('simpleText')
                        vid_id = hold_each_jsn.get('videoId')
                        vid_thmb = hold_each_jsn.get('thumbnail').get(
                            'thumbnails')[3].get('url')
                        # Livestream
                        if hold_each_jsn.get('shortViewCountText'):
                            if hold_each_jsn.get('shortViewCountText').get('runs'):
                                vid_date = "LIVE NOW!"
                        # Upcoming
                        if hold_each_jsn.get('upcomingEventData'):
                            vid_date = hold_each_jsn.get(
                                'upcomingEventData').get('startTime')
                            vid_date = datetime.fromtimestamp(int(vid_date))
                        self.compInfo.append([str(self.results_chnl_name), f"https://www.youtube.com{str(self.results_chnl_url)}", f"https:{self.results_chnl_thmb}", str(
                            vid_title), f"https://www.youtube.com/watch?v={str(vid_id)}", str(vid_date), str(vid_thmb)])
                        self.save_file.write(str(self.compInfo))

        except Exception as e:
            raise e
            return self._GetVidInfo()

    # Disabled because kinda redundant
    # def _SortChnlInfo(self, JSON_):
    #     hold_jsn = JSON_
    #     try:
    #         chnl_Info = hold_jsn.get('metadata').get('channelMetadataRenderer')
    #         if chnl_Info:
    #             chnl_title = chnl_Info.get('title')
    #             chnl_desc = chnl_Info.get('description')
    #             chnl_url = chnl_Info.get('channelUrl')
    #             chnl_thmb = chnl_Info.get('avatar').get(
    #                 'thumbnails')[0].get('url')
    #             final_info = f"{chnl_title}:`|{chnl_url}:`|{chnl_thmb}:`|{chnl_desc}|`~|\n"
    #             final_info = str(final_info).encode()
    #             final_info = final_info.decode()
    #             self.save_file.write(str(final_info))
    #     except Exception as e:
    #         raise e

    # The hell of nested dictionaries and list
    def _SortChnlVid(self, JSON_):
        jsn_dict = JSON_
        try:
            for e_jsn_dict in jsn_dict:
                jsn_list = e_jsn_dict.get('tabRenderer')
                if jsn_list:
                    jsn_f_list = jsn_list.get('content')
                    if jsn_f_list:
                        jsn_s_list = jsn_f_list.get(
                            'sectionListRenderer').get('contents')
                        for each_jsn_l in jsn_s_list:
                            hold_jsn_l = each_jsn_l.get(
                                'itemSectionRenderer').get('contents')
                            if hold_jsn_l:
                                for each_hold_jsn_l in hold_jsn_l:
                                    self.jsn_info = None
                                    if each_hold_jsn_l.get('channelFeaturedContentRenderer'):
                                        self.jsn_info = each_hold_jsn_l.get(
                                            'channelFeaturedContentRenderer')
                                        if each_hold_jsn_l.get('channelFeaturedContentRenderer').get('items'):
                                            self.jsn_info = each_hold_jsn_l.get(
                                                'channelFeaturedContentRenderer').get('items')
                                    if each_hold_jsn_l.get('shelfRenderer'):
                                        self.jsn_info = each_hold_jsn_l.get(
                                            'shelfRenderer').get('content')
                                        if each_hold_jsn_l.get('shelfRenderer').get('content').get('expandedShelfContentsRenderer'):
                                            self.jsn_info = each_hold_jsn_l.get('shelfRenderer').get(
                                                'content').get('expandedShelfContentsRenderer').get('items')
                                        elif each_hold_jsn_l.get('shelfRenderer').get('content').get('horizontalListRenderer'):
                                            self.jsn_info = each_hold_jsn_l.get('shelfRenderer').get(
                                                'content').get('horizontalListRenderer').get('items')
                                    if self.jsn_info:
                                        self._GetVidInfo()
        except Exception:
            raise Exception

    def RemoveDuplicates(self):
        s = open('VidResults.log', 'r', encoding='utf-8')
        valuedict = str(s.read()).splitlines()
        valuedict = list(dict.fromkeys(valuedict))
        s.close()
        s = open('VidResults.log', 'w', encoding='utf-8')
        for val in valuedict:
            s.write(f"{val}\n")
        s.close()

    def _GetChnlVids(self, CHNL_URL_):
        jsn = self._ExtractJson(CHNL_URL_, 27)
        jsn_vid = jsn.get('contents').get(
            'twoColumnBrowseResultsRenderer').get('tabs')
        # Get Channel Video
        self._SortChnlVid(jsn_vid)
        # Get Channel Info
        # self._SortChnlInfo(jsn)

    def _RequestWebsite(self, search_value):
        self.save_file = open('VidResults.log', 'a', encoding='utf-8')
        self.search_value = str(search_value).replace(' ', '+')
        self.isFound = False
        url = f"https://www.youtube.com/results?search_query={self.search_value}"
        self._FindChannel(url)
        self.save_file.close()
        self.RemoveDuplicates()
        return self.compInfo


def main():
    SearchEvents()._RequestWebsite("Matsuri ch.")


if __name__ == '__main__':
    main()
