import os

import googleapiclient.discovery

def getUploadsNumber(channelName):

    api_service_name = "youtube"
    api_version = "v3"

    DEVELOPER_KEY = open('dev.key', 'r').read().strip()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

# get channel id
    request = youtube.search().list(
        part="snippet",
        q=channelName,
        type="channel"
    )
    response = request.execute()
    
    channelid = response["items"][0]["id"]["channelId"]

# get uploads playlist id
    request = youtube.channels().list(
        part="contentDetails",
        id=channelid
    )
    response = request.execute()

    uploadPlaylist = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

# get total number of vids
    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=1,
        playlistId=uploadPlaylist
    )
    response = request.execute()

    return response["pageInfo"]["totalResults"]
