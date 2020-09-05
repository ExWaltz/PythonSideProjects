from googleapiclient.discovery import build
import codecs


def BuildYoutube(chId, ytFunc, event):
    request = ytFunc.search().list(
        part='snippet',
        channelId=chId,
        eventType=event,
        type="video"
    )
    response = request.execute()
    return (response)


def cleanUp():
    s = codecs.open('teststreams.log', 'r', 'utf-8')
    sl = []
    for lines in s:
        sl = s.read().splitlines()
        pass
    s.close()
    s = codecs.open('teststreams.log', 'w', 'utf-8')
    sl = list(dict.fromkeys(sl))
    sl = sorted(sl)
    for x in range(len(sl)):
        final = sl[x]
        s.write(final + '\n')
        pass
    s.close()
    pass


def main(eveType):
    api_key = 'AIzaSyBWKk6Tr6sZI0EEAEQMQJEO8nUyoIi3G_w'
    youtube = build('youtube', 'v3', developerKey=api_key)
    channels = ['UC1CfXB_kRs3C-zaeTG3oGyg', 'UCS9uQI-jC3DE0L4IpXyvr6w',
                'UCqm3BQLlJfvkTsX_hvm0UmA', 'UC1DCedRgGHBdm81E1llLhOQ', 'UChAnqc_AY5_I3Px5dig3X1Q', ]

    for each_channel in range(len(channels)):
        chResponse = BuildYoutube(channels[each_channel], youtube, eveType)
        streamInfo = []
        for searchResults in chResponse.get('items', []):
            streamInfo.append('%s : %s : %s : %s : https://www.youtube.com/watch?v=%s' % (searchResults['snippet']['liveBroadcastContent'], searchResults[
                              'snippet']['channelTitle'], searchResults['snippet']['publishTime'], searchResults['snippet']['title'], searchResults['id']['videoId']))
            pass

        streamsFile = codecs.open('streams.log', 'a', 'utf-8')
        for x in range(len(streamInfo)):
            streamsFile.write(streamInfo[x] + '\n')
            pass
        cleanUp()
        pass


if __name__ == "__main__":
    main('upcoming')
    main('live')
    pass
