import soundcloud

CLIENT = soundcloud.Client(client_id='get-your-own-key')
PAGE_SIZE = 200

def getStreamableURL(track_id):
    track = CLIENT.get('/tracks/' + track_id)
    stream_url = CLIENT.get(track.stream_url, allow_redirects=False)
    return stream_url.location

def search(queryString):
    tracks = CLIENT.get('/tracks', q=queryString, streamable='true', limit=PAGE_SIZE)

    #for track in tracks:
    #    print track
    #    print track.stream_url
    #    print track.artwork_url

    return tracks