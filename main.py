import requests
import os
#import feedparser
from time import sleep
from datetime import datetime


YOUTUBE_PLAYLIST_ID = ''
YOUTUBE_API_TOKEN = ''

def main():
    global YOUTUBE_API_TOKEN, YOUTUBE_PLAYLIST_ID   
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
            # continua a cercare nella playlist
            NEXTPAGE = '&pageToken=' + listaVideo['nextPageToken']
        else:
            # sono arrivato alla fine della playlist.
            loop = False
                
    # VIDEOID;VIDEO TITLE;CHANNEL TITLE;DATE PUBLISHED
    savedVideosFile = open('savedVideos.txt', 'r+')
    listaVideoSalvati = savedVideosFile.read().splitlines()
    listaIDSalvati = [LVS.split(';')[0] for LVS in listaVideoSalvati]

    logFile = open('logFile.txt', 'a+')
    for videoID in listaVideoID:
        if videoID not in listaIDSalvati:
            videoRequest = (f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails&id={videoID}&key={YOUTUBE_API_TOKEN}')
            rispostaVideo = requests.get(videoRequest)
            videoJSON = rispostaVideo.json()
            # se ho più di 0 risultati, ho un match. Ne dovrei avere solo 1 in teoria, but who knows...
            if videoJSON['pageInfo']['totalResults'] > 0:
                # filtro per bene ciò che mi interessa e lo salvo nei file
                videoJSON = videoJSON['items'][0]
                newVideo = videoJSON['id'] + ';' + videoJSON['snippet']['title'].replace(';', ',') + ';' + videoJSON['snippet']['channelTitle'] + ';' + videoJSON['snippet']['publishedAt'] + "\n"
                savedVideosFile.write(newVideo)
                logWrite = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ " Aggiunto " + videoJSON['snippet']['title'] + " - ID: " + videoJSON['id'] + "\n"
                logFile.write(logWrite)
                print('Aggiunto ' + videoJSON['id'])
            else:
                # se non posso accedere alle informazioni del video...
                print('Il video con ID ' + videoID + ' è privato o in fase di rimozione.')
                logWrite = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ " Il video con ID " + videoID + " è privato o in fase di rimozione.\n"
                listaVideoID.remove(videoID)
                # Elimino il video privato dalla lista degli id in modo da rimuoverlo dai file accessibili
                logFile.write(logWrite)
    savedVideosFile.close()
    # se il video non è nella lista appena ricevuta, è privato o eliminato e quindi devo rimuoverlo
    for videoID in listaIDSalvati:
        if videoID not in listaVideoID:
            index = listaIDSalvati.index(videoID)
            titoloDaRimuovere = listaVideoSalvati.pop(index).split(';')[1]
            # ricreo il file della lista senza il video eliminato
            with open('nuovaLista.txt','w') as f:
                for ogg in listaVideoSalvati:
                    f.write('%s\n' % ogg)
            os.replace('nuovaLista.txt', 'savedVideos.txt')
            # scrivo il log con il titolo per chiarezza
            logWrite = datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ " Rimosso " + titoloDaRimuovere + " - ID: " + videoID + "\n"
            logFile.write(logWrite)
            print('Rimosso ' + videoID)
    logfile.close()

if __name__ == "__main__":
    while(True):
        main()
        print('sleeping for 6 hours')
        sleep(6 * 60 * 60)