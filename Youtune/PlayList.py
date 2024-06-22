class PlayList:
    def __init__(self, id_playList, nombrep):
        self.id_playList = id_playList
        self.nombrep = nombrep
        
    def crear_playlist(self, id_playList, nombrep):
        playlist = PlayList(id_playList, nombrep)
        self.playlists.append(playlist)
        return playlist