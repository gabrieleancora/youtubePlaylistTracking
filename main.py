import requests
#import feedparser
from time import sleep
from datetime import datetime


YOUTUBE_PLAYLIST_ID = ''
YOUTUBE_API_TOKEN = ''

def main():
    global YOUTUBE_API_TOKEN, YOUTUBE_PLAYLIST_ID
    # scheme:
    # VIDEOID;VIDEO TITLE;CHANNEL TITLE;DATE PUBLISHED
    savedVideosFile = open('savedVideos.txt', 'r+')
    logFile = open('logFile.txt', 'a+')
    # obtains video list
    loop = True
    listaVideoID = []
    NEXTPAGE = ''
    while(loop):
        requestURL = (f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50{NEXTPAGE}&playlistId={YOUTUBE_PLAYLIST_ID}&key={YOUTUBE_API_TOKEN}')
        risposta = requests.get(requestURL)
        listaVideo = risposta.json()
        for video in listaVideo['items']:
            videoID = video['contentDetails']['videoId']
            listaVideoID.append(videoID)
        if 'nextPageToken' in listaVideo:
            NEXTPAGE = '&pageToken=' + listaVideo['nextPageToken']
            print('continua a cercare in playlist')
        else:
            print('fine playlist')
            loop = False
                
    listaVideoSalvati = savedVideosFile.read().splitlines()
    listaIDSalvati = [LVS.split(';')[0] for LVS in listaVideoSalvati]
    for videoID in listaVideoID:
        if videoID not in listaIDSalvati:
            videoRequest = (f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails&id={videoID}&key={YOUTUBE_API_TOKEN}')
            rispostaVideo = requests.get(videoRequest)
            videoJSON = rispostaVideo.json()['items'][0]
            newVideo = videoJSON['id'] + ';' + videoJSON['snippet']['title'].replace(';', ',') + ';' + videoJSON['snippet']['channelTitle'] + ';' + videoJSON['snippet']['publishedAt'] + "\n"
            savedVideosFile.write(newVideo)
            logWrite = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ " Aggiunto " + videoJSON['snippet']['title'] + " - ID: " + videoJSON['id'] + "\n"
            logFile.write(logWrite)
            print('Aggiunto ' + videoJSON['id'])
        # controlla esistenza in savedVideos
        # se non esiste aggiungi in savedVideos con query per le info e segna l'aggiunta
        # print(videoID)
    # ora fai il controllo inverso
    # se esiste in savedVideos.txt ma non in listaVideoID, segna la rimozione
    # rimuovi da savedVideos.txt

    #file.close()

main()
# #sleep a lot

# {
#   "kind": "youtube#videoListResponse",
#   "etag": "4W_br4Cz3QO5She8YK6p5Du3JVI",
#   "items": [
#     {
#       "kind": "youtube#video",
#       "etag": "hw8ECB0_eoA7w98vdaLoHZ_E6K0",
#       "id": "JzY8fLoK2S0",
#       "snippet": {
#         "publishedAt": "2020-07-16T18:26:39Z",
#         "channelId": "UCzu5jv-qAZJ3ZaavGJ5RCtw",
#         "title": "[ENG SUB] Young Jump July 2020 Featurette - Suwa Nanaka",
#         "description": "Small video featuring Suwa Nanaka to promote Aqours in Young Jump 2020 33/34.\n\nOriginal video: https://www.youtube.com/watch?v=5Eln-gya1h0\nBuy physical here (JP CC/Address required): https://7net.omni7.jp/search/?keyword=lovelivess_unitfile\nBuy digital here: https://books.rakuten.co.jp/rk/6d853e5b2ca13957bb84d3fc0aa61a8c/?l-id=search-c-item-text-01",
#         "thumbnails": {
#           "default": {
#             "url": "https://i.ytimg.com/vi/JzY8fLoK2S0/default.jpg",
#             "width": 120,
#             "height": 90
#           },
#           "medium": {
#             "url": "https://i.ytimg.com/vi/JzY8fLoK2S0/mqdefault.jpg",
#             "width": 320,
#             "height": 180
#           },
#           "high": {
#             "url": "https://i.ytimg.com/vi/JzY8fLoK2S0/hqdefault.jpg",
#             "width": 480,
#             "height": 360
#           },
#           "standard": {
#             "url": "https://i.ytimg.com/vi/JzY8fLoK2S0/sddefault.jpg",
#             "width": 640,
#             "height": 480
#           },
#           "maxres": {
#             "url": "https://i.ytimg.com/vi/JzY8fLoK2S0/maxresdefault.jpg",
#             "width": 1280,
#             "height": 720
#           }
#         },
#         "channelTitle": "Dyrea",
#         "categoryId": "1",
#         "liveBroadcastContent": "none",
#         "localized": {
#           "title": "[ENG SUB] Young Jump July 2020 Featurette - Suwa Nanaka",
#           "description": "Small video featuring Suwa Nanaka to promote Aqours in Young Jump 2020 33/34.\n\nOriginal video: https://www.youtube.com/watch?v=5Eln-gya1h0\nBuy physical here (JP CC/Address required): https://7net.omni7.jp/search/?keyword=lovelivess_unitfile\nBuy digital here: https://books.rakuten.co.jp/rk/6d853e5b2ca13957bb84d3fc0aa61a8c/?l-id=search-c-item-text-01"
#         }
#       },
#       "contentDetails": {
#         "duration": "PT2M10S",
#         "dimension": "2d",
#         "definition": "hd",
#         "caption": "false",
#         "licensedContent": false,
#         "contentRating": {},
#         "projection": "rectangular"
#       }
#     }
#   ],
#   "pageInfo": {
#     "totalResults": 1,
#     "resultsPerPage": 1
#   }
# }