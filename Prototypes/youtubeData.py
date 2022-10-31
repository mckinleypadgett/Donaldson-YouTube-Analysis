# Credit: This iteration includes idea presented by Thoufiq Mohammed in this video https://www.youtube.com/watch?v=SwSbnmqk3zY
from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns

api_key = 'AIzaSyBwxyfaOh3wkFlOgG4TY6R2L-7wKYF-W78' # YouTube Data API v3

# This single string and list of channel ids is for testing purposes at the moment. Need to gather additional channel ids for rest of requested companies
channel_id = 'UCZNvqiGznGApSxsVHxw9hrA' # Arctic Cat
channel_ids = ['UCfe2d71EQLZXhOLY9N7aqfg', # Donaldson
               'UC1D6AaYUTdR86tngI_HsVig', # AGCO Power
               'UCgWfMSM_i80aJ_Yu5XVfb1A', # Agrale S.A. 
               'UCZNvqiGznGApSxsVHxw9hrA', # Arctic Cat
               'UCcsfE910TN0QI6ae4dWXI6w'  # Ashok Leyland
              ]

# create a build service to pull data from 
youtube = build('youtube', 'v3', developerKey=api_key)

## Function to get channel statistics
def get_channel_statistics(youtube, channel_ids):
    all_channel_data = []
    request = youtube.channels().list(
                part='snippet,contentDetails,statistics',
                id= ','.join(channel_ids))
    response = request.execute()

    for i in range(len(response['items'])):
        channel_data = dict(Channel_name = response['items'][i]['snippet']['title'],
                    Subscribers = response['items'][i]['statistics']['subscriberCount'],
                    Views = response['items'][i]['statistics']['viewCount'],
                    Total_videos = response['items'][i]['statistics']['videoCount'],
                    playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_channel_data.append(channel_data)

    return all_channel_data

channel_statistics = get_channel_statistics(youtube, channel_ids)

channel_stats_df = pd.DataFrame(channel_statistics)
channel_stats_df.to_csv('./channel_stats.csv')


playlist_id = channel_stats_df.loc[channel_stats_df['Channel_name']=='Arctic Cat', 'playlist_id'].iloc[0]


## Function to get all video IDs from a channel
def get_video_ids(youtube, playlist_id):

    request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId = playlist_id, 
                maxResults = 50)
    response = request.execute()

    video_ids = []

    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token = response['nextPageToken']
    more_pages = True

    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId = playlist_id, 
                maxResults = 50,
                pageToken = next_page_token)
            response = request.execute()

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')

    return video_ids

all_video_ids = get_video_ids(youtube, playlist_id)
videos_df = pd.DataFrame(all_video_ids)
videos_df.to_csv('./all_videos.csv')
print(videos_df)

def get_comments(youtube, channel_id):

    comments = []

    request = youtube.commentThreads().list(
                part='snippet, replies',
                allThreadsRelatedToChannelId = channel_id,
                maxResults = 50)
    response = request.execute()

    for i in range(len(response['items'])):
        comments.append(response['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])

    return comments

comments = (get_comments(youtube, channel_id))

all_comments_df = pd.DataFrame(comments)
all_comments_df.to_csv('./all_comments.csv')

print(all_comments_df)
#channel_statistics = get_channel_statistics(youtube, channel_ids)

#channel_stats = pd.DataFrame(channel_statistics)

print(channel_stats_df)

