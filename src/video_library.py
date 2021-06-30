"""A video library class."""

from .video import Video
from pathlib import Path
import csv


# Helper Wrapper around CSV reader to strip whitespace from around
# each item.
def _csv_reader_with_strip(reader):
    yield from ((item.strip() for item in line) for line in reader)


class VideoLibrary:
    """A class used to represent a Video Library."""

    def __init__(self):
        """The VideoLibrary class is initialized."""
        self._videos = {}

        """ current video playing format -> video_id $$$ video_title $$$ status"""
        """status -> play/pause/continue"""
        self._current_video_playing = "" 
        

        with open(Path(__file__).parent / "videos.txt") as video_file:
            reader = _csv_reader_with_strip(
                csv.reader(video_file, delimiter="|"))
            for video_info in reader:
                title, url, tags = video_info
                self._videos[url] = Video(
                    title,
                    url,
                    [tag.strip() for tag in tags.split(",")] if tags else [],
                )
                
    def get_all_videos(self):
        """Returns all available video information from the video library."""
        return list(self._videos.values())

    def get_video(self, video_id):
        """Returns the video object (title, url, tags) from the video library.

        Args:
            video_id: The video url.

        Returns:
            The Video object for the requested video_id. None if the video
            does not exist.
        """
        return self._videos.get(video_id, None)

    def get_current_playing_video(self):
        return self._current_video_playing

    def play_video(self, video_id, video_title):
        self._current_video_playing = f"{video_id}$$${video_title}$$$play"

    def stop_video(self):
        self._current_video_playing = ""

    def pause_video(self):
        explode = self._current_video_playing.split("$$$")
        explode[2] = "pause"
        self._current_video_playing = "$$$".join(explode)

    def continue_video(self):
        explode = self._current_video_playing.split("$$$")
        explode[2] = "continue_video"
        self._current_video_playing = "$$$".join(explode)