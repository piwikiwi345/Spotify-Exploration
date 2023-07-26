'''
This python file is a module that contains functions to retrieve data from the Spotify API
Created by Prithvi Venkataswamy on July 18, 2023
'''

import requests
import base64
from requests import post
from requests import get
import json
import pprint
import pandas as pd


def get_token(client_ID, client_SECRET):
    '''
    Get a bearer token from the Spotify API.

    This functions both prints all the info relevant to the bearer token
    and returns the bearer token ID itself.
    '''

    # Spotify API credentials
    client_id = client_ID
    client_secret = client_SECRET

    # Base64 encoded client_id:client_secret
    client_creds = base64.b64encode(
        f"{client_id}:{client_secret}".encode()).decode()

    # Request headers
    headers = {
        "Authorization": f"Basic {client_creds}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Request body
    data = {
        "grant_type": "client_credentials",
    }

    # Send POST request to obtain access token
    response = requests.post(
        "https://accounts.spotify.com/api/token", headers=headers, data=data)

    print(json.dumps(response.json()))

    # Check if the request was successful
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        return (access_token)
    else:
        print("Error:", response.text)


def get_auth_header(token):
    '''
    This function creates the authorization header for the bearer token.
    '''

    return {"Authorization": "Bearer " + token}


def search_for_artist(token, artist_name):
    '''
    Search for an artist by name and return the 10 most popular results.
    '''

    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=10"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return (json_result)


def get_playlist(token, playlist_id):
    '''
    Get the metadata for all the tracks in a playlist.
    
    Note: The metadata retrieved for each track does not contain all the fields present in the 'Get Track'
    
    Returns a list of dictionaries (for each song).
    '''

    url = "https://api.spotify.com/v1/playlists"
    headers = get_auth_header(token)
    playlist = f"/{playlist_id}"

    playlist_url = url + playlist
    result = get(playlist_url, headers=headers)
    json_result = json.loads(result.content)
    return (json_result)


def get_audio_feature(token, track_id):
    '''
    Get audio features for a single track.
    '''
    # build request
    url = "https://api.spotify.com/v1/audio-features/"
    headers = get_auth_header(token)

    audio_feature_url = url + str(track_id)
    result = get(audio_feature_url, headers=headers)
    json_result = json.loads(result.content)
    return (json_result)


def get_audio_feature_for_list(token, track_ids):
    '''
    Get audio features for each track in a playlist given a list of playlist ids.
    '''
    data = []

    for song in track_ids:
        audio_data = get_audio_feature(token, song)
        data.append(audio_data)

    return (data)


def audio_feature_data_into_df(data):
    '''
    Grab data from dictionary and put it into a dataframe

    Clean the data of unwanted columns and move the 'id' column to be first.
    '''
    df = pd.DataFrame(data)

    columns_to_drop = ['uri', 'track_href', 'analysis_url', 'type']
    df = df.drop(columns_to_drop, axis=1)

    new_order = ['id', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
                 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']
    df = df[new_order]

    return (df)


def get_audio_features_for_playlist(token, playlist_id):
    '''
    This function takes a Spotify playlist id and returns a pandas dataframe containing audio features of every track in the           playlist while dropping the following columns: uri, track_href, analysis_url, and type. 

    It also moves the id column into a better position
    
    token: bearer token id 
    playlist_id: playlist ID formatted as a string
    '''

    # get track metadata from playlists
    playlist = get_playlist(token, playlist_id)
    tracks = playlist["tracks"]["items"]

    # extract track_ids from dictionary and store in list
    playlist_track_ids = []

    for song in tracks:
        playlist_track_ids.append(song["track"]["id"])

    # get audio features for each track in playlist
    playlist_tracks_audio_features = get_audio_feature_for_list(token, playlist_track_ids)

    # transfer to pandas dataframe and clean dataframe
    df = audio_feature_data_into_df(playlist_tracks_audio_features)

    return (df)


def compile_playlists(token, playlist_ids):
    '''
    This function takes a list of playlist ids and returns a list of dictionaries with the key containing the playlist name 
    and the value containing a dataframe object with the audio features for each track in the playlist.
    '''
    playlists_w_audio_data = {}
    
    for playlist_id in playlist_ids:
        # get name of playlist
        name = get_playlist(token, playlist_id)['name']
        
        # get audio feature data for playlist
        data = get_audio_features_for_playlist(token, playlist_id)
        
        # add name and data to dictionary
        playlists_w_audio_data[name] = data
        
    return(playlists_w_audio_data)


def get_artist_details_from_track(token, track_id):
    '''
    This function (given a track_id) grabs the track ID, track name, artist ID, and artist name as a dictionary.
    
    token: bearer token id 
    track_id: track ID formatted as a string
    '''
    
    # build request to get track information
    url = "https://api.spotify.com/v1/tracks/"
    headers = get_auth_header(token)

    track_metadata_url = url + track_id
    result = get(track_metadata_url, headers=headers)
    json_result = json.loads(result.content)
    
    # grab the following columns and delete other columns from track information
    artist_info = json_result['album']['artists'][0]
    del artist_info['external_urls']
    del artist_info['href']
    del artist_info['type']
    del artist_info['uri']
    artist_info['artist_id'] = artist_info['id']
    del artist_info['id']
    artist_info['track_id'] = track_id
    artist_info['track_name'] = json_result['name']
    artist_info['popularity'] = json_result['popularity']
    return(artist_info)


def get_artist_genre(token, artist_id):
    '''
    This function (given an artist_id) grabs the artist_id, name, and their related genres 
    and returns them in a dictionary.
    
    token: bearer token ID
    artist_id: artist ID formatted as a string
    '''
    
    # build request to get track information
    url = "https://api.spotify.com/v1/artists/"
    headers = get_auth_header(token)

    artist_metadata_url = url + artist_id
    result = get(artist_metadata_url, headers=headers)
    json_result = json.loads(result.content)
    
    # grab information from json to put in dictionary
    genres = json_result['genres']
    name = json_result['name']
    data = {'artist_id': artist_id, 'name': name}
    if len(genres) == 1:
        data['Genre 1'] = genres[0]
    if len(genres) > 1:
        for genre in genres:
            data[f'Genre {genres.index(genre) + 1}'] = genre
    return(data)


def df_export_csv(df, filename):
    '''
    This function exports a dataframe as a .csv file with the name of the dataframe as the filename.
    
    df: a pandas dataframe
    '''
    
    # export dataframe to csv
    df.to_csv(f'{filename}.csv', sep = ',', index=False, encoding='utf-8')
    

def get_genres_for_playlist(token, playlist_id):
    '''
    This function gets the artist name, ID, and genre information for all the tracks in a playlist returned as a pandas dataframe.
    
    token: bearer token ID
    playlist_id: playlist ID formatted as a string
    '''
    # get track metadata from playlists
    playlist = get_playlist(token, playlist_id)
    tracks = playlist["tracks"]["items"]

    # extract track IDs from dictionary and store in list
    tracks_ids = []

    for song in tracks:
        tracks_ids.append(song["track"]["id"])
        
    # get artist IDs for each track in playlist
    artists_ids = []
    
    for track_id in tracks_ids:
        artists_ids.append(get_artist_details_from_track(token, track_id)['artist_id'])
        
    print(artists_ids)
        
    # get genres for each artist
    tracks_genre = []
    
    for artist_id in artists_ids:
        tracks_genre.append(get_artist_genre(token, artist_id))

    df = pd.DataFrame(tracks_genre)
    
    return(df)


def get_track_and_artist_info_for_playlist(token, playlist_id):
    '''
    This function returns a pandas dataframe containing the track_id, track name, and  artist_id, and artist name
    for all tracks in the given playlist.
    
    token: bearer token ID
    playlist_id: playlist ID formatted as a string
    '''
    
    # get track metadata from playlists
    playlist = get_playlist(token, playlist_id)
    tracks = playlist["tracks"]["items"]

    # extract track IDs from dictionary and store in list
    tracks_ids = []

    for song in tracks:
        tracks_ids.append(song["track"]["id"])
    
    # get artist and track details from track ID
    information = []
    
    for track_id in tracks_ids:
        information.append(get_artist_details_from_track(token, track_id))
        
    df = pd.DataFrame(information)
    
    return(df)