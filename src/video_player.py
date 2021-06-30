"""A video player class."""
import random, collections
from .video_library import VideoLibrary
from .video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playlist_library = Playlist()

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        all_videos = sorted(self._video_library.get_all_videos(), key=lambda x: x._title)
        print("Here's a list of all available videos:")
        for video in all_videos:
            print(
                video._title, 
                "("+video._video_id+")",
                "["+" ".join(list(video._tags)) +"]",
                "- FLAGGED (reason: "+video._flagged_reason+")" if video._flagged==1 else ""
            )
        
    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot play video: Video does not exist")
        elif video._flagged == 1:
            print(f"Cannot play video: Video is currently flagged (reason: {video._flagged_reason})")
        else:
            video_to_be_played_id = video._video_id
            video_to_be_played_title = video._title
            
            current_video_playing = self._video_library.get_current_playing_video().split("$$$")

            #updating the new video
            self._video_library.play_video(video_to_be_played_id, video_to_be_played_title)

            if current_video_playing[0] == "":
                print(f"Playing video: {video_to_be_played_title}")
            else:
                print(f"Stopping video: {current_video_playing[1]}")
                print(f"Playing video: {video_to_be_played_title}")


    def stop_video(self):
        """Stops the current video."""
        current_video_playing = self._video_library.get_current_playing_video().split("$$$")
        
        if current_video_playing[0] != "":
            print(f"Stopping video: {current_video_playing[1]}")
            
            #updating the new video
            self._video_library.stop_video()
        else:
            print("Cannot stop video: No video is currently playing")
        

    def play_random_video(self):
        """Plays a random video from the video library."""

        #generating a random number from the length of total videos.
        all_videos = self._video_library.get_all_videos()
        new_all_video_list = []
        for i in range(len(all_videos)):
            if all_videos[i]._flagged == 0:
                new_all_video_list.append(all_videos[i])

        num_videos = len(new_all_video_list)
        if num_videos == 0:
            print("No videos available")
        else:
            video_index = random.randint(0,num_videos-1)
            video_id = new_all_video_list[video_index]._video_id
            self.play_video(video_id)
        

    def pause_video(self):
        """Pauses the current video."""
        current_video_playing = self._video_library.get_current_playing_video().split("$$$")
        
        if current_video_playing[0] != "":

            if current_video_playing[2] == "pause":
                print(f"Video already paused: {current_video_playing[1]}")
            elif current_video_playing[2] == "play":
                print(f"Pausing video: {current_video_playing[1]}")
                
                #updating the new video
                self._video_library.pause_video()
        else:
            print("Cannot pause video: No video is currently playing")
        

    def continue_video(self):
        """Resumes playing the current video."""
        current_video_playing = self._video_library.get_current_playing_video().split("$$$")
        
        if current_video_playing[0] != "":
            if current_video_playing[2] == "continue" or current_video_playing[2] == "play":
                print(f"Cannot continue video: Video is not paused")
            elif current_video_playing[2] == "pause":
                print(f"Continuing video: {current_video_playing[1]}")
                
                #updating the new video
                self._video_library.continue_video()
        else:
            print("Cannot continue video: No video is currently playing")


    def show_playing(self):
        """Displays video currently playing."""
        current_video_playing = self._video_library.get_current_playing_video().split("$$$")
        
        if current_video_playing[0] != "":
            video = self._video_library.get_video(current_video_playing[0])
            status = ""
            output = f"Currently playing: {video._title} ({video._video_id}) ["+" ".join(list(video._tags)) +"]"
            if current_video_playing[2] == "pause":
                output += " - PAUSED"

            print(output)
        else:
            print("No video is currently playing")


    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        lowercase_playlist_name = playlist_name.lower()
        check = self._playlist_library.check_playlist_exist(lowercase_playlist_name)
        if check:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self._playlist_library.create_playlist(playlist_name)
            print(f"Successfully created new playlist: {playlist_name}")
        
    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        lowercase_playlist_name = playlist_name.lower()
        check = self._playlist_library.check_playlist_exist(lowercase_playlist_name)
        video = self._video_library.get_video(video_id)
        
        if not check:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        elif video is None:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
        elif video._flagged == 1:
            print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {video._flagged_reason})")
        else:
            if self._playlist_library.check_video_exists_in_playlist(playlist_name.lower(), video_id):
                print(f"Cannot add video to {playlist_name}: Video already added")
            else:
                self._playlist_library.add_video_in_playlist(playlist_name.lower(), video_id)
                print(f"Added video to {playlist_name}: {video._title}")

    def show_all_playlists(self):
        """Display all playlists."""
        playlist = self._playlist_library.get_playlist()
        if len(playlist) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            playlists = sorted(playlist)
            for key in playlists:
                print(playlist[key]["name"])
        
    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        lowercase_playlist_name = playlist_name.lower()
        check = self._playlist_library.check_playlist_exist(lowercase_playlist_name)
        if not check:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
        else:
            print(f"Showing playlist: {playlist_name}")
            playlist = self._playlist_library.get_playlist()[lowercase_playlist_name]
            if len(playlist["videos"])==0:
                print("No videos here yet")
            else:
                for video_id in playlist["videos"]:
                    video = self._video_library.get_video(video_id)
                    output = f"Currently playing: {video._title} ({video._video_id}) ["+" ".join(list(video._tags)) +"]"
            
                    if video._flagged == 1:
                        output += " - FLAGGED (reason: "+video._flagged_reason+")"
                    
                    print(output)


    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        lowercase_playlist_name = playlist_name.lower()
        check = self._playlist_library.check_playlist_exist(lowercase_playlist_name)
        if not check:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        else:
            video = self._video_library.get_video(video_id)
            if video is None:
                print(f"Cannot remove video from {playlist_name}: Video does not exist")
            else:
                playlist = self._playlist_library.get_playlist()[lowercase_playlist_name]    
                if video_id in playlist["videos"].keys():
                    print(f"Removed video from {playlist_name}: {video._title}")
                    #code
                    self._playlist_library.remove_from_playlist(lowercase_playlist_name, video_id)

                else:
                    print(f"Cannot remove video from {playlist_name}: Video is not in playlist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        lowercase_playlist_name = playlist_name.lower()
        check = self._playlist_library.check_playlist_exist(lowercase_playlist_name)
        if not check:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            print(f"Successfully removed all videos from {playlist_name}")
            #code
            self._playlist_library.clear_playlist(lowercase_playlist_name)

        
    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        lowercase_playlist_name = playlist_name.lower()
        check = self._playlist_library.check_playlist_exist(lowercase_playlist_name)
        if not check:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            print(f"Deleted playlist: {playlist_name}")
            #code
            self._playlist_library.delete_playlist(lowercase_playlist_name)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        all_videos_list = {}
        for videos in all_videos:
            if videos._title.lower().find(search_term) != -1 and videos._flagged==0:
                all_videos_list[videos._video_id] = {} 
                all_videos_list[videos._video_id]["name"] = videos._title
        
        if len(all_videos_list)>0:
            all_videos_list = sorted(all_videos_list.items(), key=lambda x: x[1]['name'])
            all_videos_list = dict(all_videos_list)
            num = 1
            print(f"Here are the results for {search_term}:")
            output_dict = {}
            for key in all_videos_list.keys():
                video = self._video_library.get_video(key)
                print(f"{num}) {video._title} ({key}) ["+" ".join(list(video._tags)) +"]")
                output_dict[num] = {}
                output_dict[num]["id"] = key
                num+=1
            
            print("Would you like to play any of the above? If yes, "
                "specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            input_number = input()
            
            if input_number.isnumeric():
                if int(input_number) in output_dict.keys():
                    self.play_video(output_dict[int(input_number)]["id"])
        else:
            print(f"No search results for {search_term}")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        all_videos_list = {}
        for videos in all_videos:
            if video_tag in videos.tags and videos._flagged==0:
                all_videos_list[videos._video_id] = {} 
                all_videos_list[videos._video_id]["name"] = videos._title
        
        if len(all_videos_list)>0:
            all_videos_list = sorted(all_videos_list.items(), key=lambda x: x[1]['name'])
            all_videos_list = dict(all_videos_list)
            num = 1
            print(f"Here are the results for {video_tag}:")
            output_dict = {}
            for key in all_videos_list.keys():
                video = self._video_library.get_video(key)
                print(f"{num}) {video._title} ({key}) ["+" ".join(list(video._tags)) +"]")
                output_dict[num] = {}
                output_dict[num]["id"] = key
                num+=1
            
            print("Would you like to play any of the above? If yes, "
                "specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            input_number = input()
            
            if input_number.isnumeric():
                if int(input_number) in output_dict.keys():
                    self.play_video(output_dict[int(input_number)]["id"])
        else:
            print(f"No search results for {video_tag}")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot flag video: Video does not exist")
        else:
            if video._flagged == 0:

                current_video_playing = self._video_library.get_current_playing_video().split("$$$")
                if current_video_playing[0] == video_id:
                    self.stop_video()                    

                video._flagged = 1
                video._flagged_reason = "Not supplied" if flag_reason == "" else flag_reason
                print(f"Successfully flagged video: {video._title} (reason: {video._flagged_reason})")
            else:
                print("Cannot flag video: Video is already flagged")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot remove flag from video: Video does not exist")
        else:
            if video._flagged == 1:
                video._flagged = 0
                video._flagged_reason = ""
                print(f"Successfully removed flag from video: {video._title}")
            else:
                print("Cannot remove flag from video: Video is not flagged")
