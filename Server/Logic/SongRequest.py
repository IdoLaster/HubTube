"""
    Author: Ido Laster
    Description: a basic song request class to keep things organized.
    Date: 21/4/2017
"""
import json
import re


class SongRequest():

    def __init__(self, song_url, sender):
        """
        A basic constructor to the class.
        @param song_url: The song url.
        @param sender: The name of the sender.
        """
        self.__song_url = song_url
        self.__sender = sender

    # Just some getters in case we need them.
    def get_sender(self):
        """
        Returning the name of the sender.
        @return: The name of the sender.
        """
        return self.__sender

    def get_song_url(self):
        """
        Returning the raw song url.
        @return: The raw song url.
        """
        return self.__song_url

    # Returning only the video ID of the url, still need to test it with
    # Different kind of URLs.
    def get_video_id(self):
        """
        Extracting and returning the video id from the url.
        @return: Only the video ID from the url.
        """
        return self.__song_url.split('/')[3].split('=')[1]

    # Returning the song request class as json, so we could send it.
    def to_json(self):
        """
        Converting the object to json so we could send him.
        @return: The object as json.
        """
        fields = {"name": self.get_sender(), "video-id": self.get_video_id()}
        return json.dumps(fields)

    def valid_url(self):
        """
        Validating the video url.
        @return: True if valid, False if invalid.
        """
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        youtube_regex_match = re.match(youtube_regex, self.__song_url)

        if youtube_regex_match:
            return youtube_regex_match.group(6)

        return youtube_regex_match
