"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self):
        """The Playlist class is initialized."""
        self._playlist = {}

    def get_playlist(self):
        return self._playlist

    def check_playlist_exist(self, playlist_name):
        if playlist_name in self._playlist.keys():
            return True
        else:
            return False

    def create_playlist(self, playlist_name):
        lowercase_playlist_name = playlist_name.lower()
        self._playlist[lowercase_playlist_name] = {
            "name": playlist_name,
            "videos":{}
        }

    def check_video_exists_in_playlist(self, playlist_name, video_id):
        if playlist_name in self._playlist.keys():
            if video_id in self._playlist[playlist_name]['videos'].keys():
                return True
            else:
                return False
        return False

    def add_video_in_playlist(self, playlist_name, video_id):
        self._playlist[playlist_name]["videos"][video_id] = {}

    def remove_from_playlist(self, playlist_name, video_id):
        self._playlist[playlist_name]["videos"].pop(video_id, None)

    def clear_playlist(self, playlist_name):
        self._playlist[playlist_name]["videos"] = {}

    def delete_playlist(self, playlist_name):
        self._playlist.pop(playlist_name, None)
