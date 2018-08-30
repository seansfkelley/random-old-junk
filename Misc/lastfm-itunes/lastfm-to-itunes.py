API_KEY = 'b32227d902a74acc4a021dda622ee696'
USER = 'toastandoj'
ITUNES_MUSIC = '/Volumes/skelley/iTunes/iTunes Music/'

# Should return an iterable of Track objects.
def get_lastfm_tracks(lastfm_user):
    recent_plays = [] # lastfm_user.get_recent_tracks(limit = 200)[:2000]
    top_plays = lastfm_user.get_top_tracks(period = 'overall', limit = 200)[:1000]
    return set(itertools.chain(recent_plays, top_plays))

# ---------------------------------------------------------------------------------------

import lastfm
import os
import sys
import re
import difflib
import itertools
import appscript

# Canonicalize names (artists, albums, tracks) into a form better suited for fuzzy matching.
def canonicalize(name):
    name = name.lower()
    if name.startswith('the' ):
        name = name[4:]
    elif name.startswith('a '):
        name = name[2:]
    return name

# Uses canonicalization and near matches to retrieve something from a dictionary of
# strings to anything. Returns None if no satisfactory element can be found.
def fuzzy_get(key, dictionary, confidence=0.8):
    possible_keys = difflib.get_close_matches(canonicalize(key), dictionary.keys(), cutoff=confidence)
    if not possible_keys:
        return None
    else:
        return dictionary[possible_keys[0]]

# Represents an iTunes library, indexed by artist + song combinations.
class iTunesLibrary:
    def __init__(self, itunes_music_folder):
        self._build_itunes_dictionary(itunes_music_folder)

    # {artist_c -> {song_c -> [(album_c, path)]}}
    def _build_itunes_dictionary(self, itunes_music_folder):
        def listdir(path):
            if not os.path.isdir(path):
                return []
            return filter(lambda x: not x.startswith('.'), os.listdir(path))

        self._itunes_dict = {}
        for artist in listdir(itunes_music_folder):
            songs = {}
            for album in listdir(os.path.join(itunes_music_folder, artist)):
                for song_file in listdir(os.path.join(itunes_music_folder, artist, album)):
                    song_match = re.match(r'^\d{2}\s+(.*)\.[a-zA-Z0-9_]+$', song_file)
                    if song_match:
                        song = canonicalize(song_match.group(1))
                        versions = songs.setdefault(canonicalize(song), [])
                        versions.append((album, os.path.join(itunes_music_folder, artist, album, song_file)))
            self._itunes_dict[canonicalize(artist)] = songs

    # Get a list of (canonicalized album name, file path) tuples for the given artist + song combo.
    def get_versions(self, artist, song):
        artist = fuzzy_get(artist, self._itunes_dict)
        # print artist
        if artist:
            versions = fuzzy_get(song, artist)
            if not versions:
                versions = []
            return versions
        else:
            return []

if __name__ == '__main__':
    library = iTunesLibrary(ITUNES_MUSIC)
    lastfm_user = lastfm.Api(API_KEY).get_user(USER)
    lastfm_selection = get_lastfm_tracks(lastfm_user)
    files = []
    for t in lastfm_selection:
        versions = library.get_versions(t.artist.name, t.name)
        if versions:
            files.append(zip(*versions)[1])
    files = sorted(itertools.chain.from_iterable(files))
    print '\n'.join(files)

