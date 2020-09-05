from bs4 import BeautifulSoup
import cfscrape
import os


class GetNovel:
    def __init__(self):
        pass

    def GetNvlId(self, NvlUrl_):
        nvlScrape = cfscrape.create_scraper()
        h_n_url = str(NvlUrl_)
        if h_n_url.find('www.novelupdates.com') != -1:
            print('Valid')
            resp = nvlScrape.get(str(NvlUrl_)).text
            n_info = BeautifulSoup(resp, 'lxml')
            nvl_i = n_info.find('link', {'rel': 'shortlink'})
            nvl_id = str(nvl_i['href']).replace(
                'https://www.novelupdates.com/?p=', '')
            return nvl_id

    def DecodeNovelString(self, STR_INPUT_):
        h_nvl = str(STR_INPUT_)
        self.novel_title, self.novel_url, self.novel_img = h_nvl.split(':`|')
        self.novel_id = self.GetNvlId(self.novel_url)

    def GetNovelLinks(self, SOUP_, LISTHOLDER_):
        results_list = SOUP_.find_all('a', {'class': 'a_search'})
        for each in results_list:
            results_title = each.find('span').text.strip()
            results_link = each['href']
            results_img = each.find(
                'img', {'class': 'search_profile_image'})['src']
            final_text = f"{results_title}:`|{results_link}:`|http:{results_img}"
            LISTHOLDER_.append(final_text)

    def GetNovelCh(self, CHSOUP_, CHLISTHOLDER_):
        nvl_Ch_list = CHSOUP_.find_all('a')
        for each_nvl in nvl_Ch_list:
            nvl_Ch_Title = each_nvl.findChild('span')
            if nvl_Ch_Title:
                nvl_Ch_Link = each_nvl['href']
                nvl_Ch_Title = nvl_Ch_Title['title']
                final_nvl_info = f"{nvl_Ch_Title}:`|http:{nvl_Ch_Link}"
                CHLISTHOLDER_.append(final_nvl_info)
        CHLISTHOLDER_.reverse()

    def ParseCh(self, arg):
        nvl_name = str(self.novel_title)
        nvl_name = ''.join(e for e in nvl_name if e.isalnum())
        nvlDir = f'Novels/{str(nvl_name)}'
        if not os.path.exists(nvlDir):
            os.makedirs(nvlDir)
        h_arg = list(arg)
        for each in h_arg:
            Ch_title, Ch_Url = str(each).split(':`|')
            chFile = open(f"{nvlDir}/{str(Ch_title)}.txt",
                          'w', encoding='utf-8')
            chParse = cfscrape.create_scraper()
            chRes = chParse.get(str(Ch_Url)).text
            chHtml = BeautifulSoup(chRes, 'lxml')
            nvlText = chHtml.find_all('p')
            for eNvl in nvlText:
                eParent = eNvl.parent.get('class')
                if eParent is None:
                    continue
                for eP in eParent:
                    if eP.find('comment') == -1:
                        chFile.write(f'{str(eNvl.text)}\n\n')
            chFile.close()
            print(f'{Ch_title} downloaded')

    def GetChLinks(self, NVL_INFO_):
        oF = open('nvl.log', 'w', encoding='utf-8')
        Nvl_Ch = []
        CHscraper = cfscrape.create_scraper()
        h_nvl_info = str(NVL_INFO_)
        self.DecodeNovelString(h_nvl_info)
        d = {'action': 'nd_getchapters',
             'mygrr': 0,
             'mypostid': self.novel_id}
        scpr = CHscraper.post(
            'https://www.novelupdates.com/wp-admin/admin-ajax.php', data=d).text
        nvl = BeautifulSoup(scpr, 'lxml')
        self.GetNovelCh(nvl, Nvl_Ch)
        oF.write(str(Nvl_Ch))
        return Nvl_Ch

    def SearchNovel(self, SearchVal_):
        list_Novels = []
        oF = open('Searchnvls.log', 'w', encoding='utf-8')
        scraper = cfscrape.create_scraper()
        api = 'https://www.novelupdates.com/wp-admin/admin-ajax.php'
        d = {'action': 'nd_ajaxsearchmain',
             'strType': 'desktop',
             'strOne': str(SearchVal_),
             'strSearchType': 'series'}
        response = scraper.post(api, d).text
        results = BeautifulSoup(response, 'lxml')
        self.GetNovelLinks(results, list_Novels)
        oF.write(str(list_Novels))
        return list_Novels


def main():
    searchKey = 'Is it Tough Being a Friend'
    q1 = GetNovel()
    listOfNovels = q1.SearchNovel(searchKey)
    print(listOfNovels)
    listOfChapters = q1.GetChLinks(listOfNovels[0])
    q1.ParseCh(listOfChapters)
    print('Our Work is Done!')


if __name__ == '__main__':
    main()
