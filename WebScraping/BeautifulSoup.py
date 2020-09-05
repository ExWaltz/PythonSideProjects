from bs4 import BeautifulSoup
import re
import requests
import codecs


def cleanUp():
    s = codecs.open("WebscrapeInfos1.log", 'r', 'utf-8')
    sl = []
    for lines in s:
        sl = s.read().splitlines()
        pass
    s.close()
    s = codecs.open("WebscrapeInfos1.log", 'w', 'utf-8')
    sl = list(dict.fromkeys(sl))
    sl = sorted(sl)
    for x in range(len(sl)):
        final = sl[x]
        s.write(final + '\n')
        pass
    s.close()
    pass


def main():
    opened_file = codecs.open("WebscrapeInfos1.log", "w", "utf-8")
    response = requests.get(
        "https://www.youtube.com/channel/UCFKOVgVbGmX65RxO3EtH3iw").text
    soup = BeautifulSoup(response, "lxml")
    strSoup = f"{soup}"
    pattern = re.compile(r'"videoId":"[^"]+"',)
    pattern2 = re.compile(
        r'"simpleText":"[^"]+"\},"publishedTimeText":\{"simpleText":"[^"]+"\},"viewCountText":\{"simpleText":"[^"]+"\}')
    results = pattern.finditer(strSoup)
    results2 = pattern2.finditer(strSoup)

    for result2 in results2:
        text = result2.group(0)
        opened_file.write(text.replace(
            '"videoId":', "https://www.youtube.com/watch?v=") + "\n")

    for result in results:
        text = result.group(0)
        opened_file.write(text.replace(
            '"videoId":', "https://www.youtube.com/watch?v=") + "\n")

    opened_file.close()
    cleanUp()


if __name__ == '__main__':
    main()
