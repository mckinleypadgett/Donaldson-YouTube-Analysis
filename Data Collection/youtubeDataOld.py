# Credit: This iteration includes idea presented by Thoufiq Mohammed in this video https://www.youtube.com/watch?v=SwSbnmqk3zY
from subprocess import ABOVE_NORMAL_PRIORITY_CLASS
from googleapiclient.discovery import build
import pandas as pd
import os
import numpy as np
import csv

api_key = 'AIzaSyBUhj3Q0oNLijpRmti05xOVMpOVjL06wIg' # YouTube Data API v3

# This single string and list of channel ids is for testing purposes at the moment. Need to gather additional channel ids for rest of requested companies
"""
channel_id = 'UCZNvqiGznGApSxsVHxw9hrA' # Arctic Cat
channel_ids = ['UCfe2d71EQLZXhOLY9N7aqfg', # Donaldson
               'UC1D6AaYUTdR86tngI_HsVig', # AGCO Power
               'UCgWfMSM_i80aJ_Yu5XVfb1A', # Agrale S.A. 
               'UCZNvqiGznGApSxsVHxw9hrA', # Arctic Cat
               'UCcsfE910TN0QI6ae4dWXI6w'  # Ashok Leyland
              ]
"""
#channelId = pd.read_csv('C:/Users/12532/Donaldson-Youtube-Analysis/companies1.csv',
#                        usecols = ["UCvUbaC8BjzIGIIzI3gGq5BA"])
channelId = pd.read_csv('./companies1.csv', usecols = ["UCvUbaC8BjzIGIIzI3gGq5BA"])
channelID_2 = pd.read_csv('./companies2.csv', usecols = ["UCcmHACp_jOo5-Mb3VVeDacw"])
#channelID_2 = pd.read_csv('C:/Users/12532/Donaldson-Youtube-Analysis/companies2.csv',
#                        usecols = ["UCcmHACp_jOo5-Mb3VVeDacw"])
# create a build service to pull data from 
youtube = build('youtube', 'v3', developerKey=api_key)

comments = []

for i in channelId:
    request = youtube.commentThreads().list(
                part='snippet, replies',
                allThreadsRelatedToChannelId = i,
                maxResults = 100)
    response = request.execute()

    for com in range(len(response['items'])):
        video_request = youtube.videos().list(
                        part='snippet',
                        id = response['items'][com]['snippet']['videoId'])
        video_response = video_request.execute()

        comment_data = dict(channel_name = video_response['items'][0]['snippet']['channelTitle'],
                            video_name = video_response['items'][0]['snippet']['title'],
                            comment = response['items'][com]['snippet']['topLevelComment']['snippet']['textOriginal'])
        comments.append(comment_data)
        #comments.append(response['items'][com]['snippet']['topLevelComment']['snippet']['textOriginal'])
    
    next_page_token = response.get('nextPageToken')
    more_pages = True
	
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.commentThreads().list(
                part='snippet, replies',
                allThreadsRelatedToChannelId = i,
                maxResults = 100,
                pageToken = next_page_token)
            response = request.execute()

            for com in range(len(response['items'])):
                video_request = youtube.videos().list(
                        part='snippet',
                        id = response['items'][com]['snippet']['videoId'])
                video_response = video_request.execute()

                comment_data = dict(channel_name = video_response['items'][0]['snippet']['channelTitle'],
                            video_name = video_response['items'][0]['snippet']['title'],
                            comment = response['items'][com]['snippet']['topLevelComment']['snippet']['textOriginal'])
                comments.append(comment_data)
                #comments.append(response['items'][com]['snippet']['topLevelComment']['snippet']['textOriginal'])

            next_page_token = response.get('nextPageToken')

for j in channelID_2:
    request = youtube.commentThreads().list(
                part='snippet, replies',
                allThreadsRelatedToChannelId = j,
                maxResults = 100)
    response = request.execute()

    for com in range(len(response['items'])):
        video_request = youtube.videos().list(
                        part='snippet',
                        id = response['items'][com]['snippet']['videoId'])
        video_response = video_request.execute()

        comment_data = dict(channel_name = video_response['items'][0]['snippet']['channelTitle'],
                            video_name = video_response['items'][0]['snippet']['title'],
                            comment = response['items'][com]['snippet']['topLevelComment']['snippet']['textOriginal'])
        comments.append(comment_data)
        #comments.append(response['items'][com]['snippet']['topLevelComment']['snippet']['textOriginal'])
    
    next_page_token = response.get('nextPageToken')
    more_pages = True
	
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.commentThreads().list(
                part='snippet, replies',
                allThreadsRelatedToChannelId = j,
                maxResults = 100,
                pageToken = next_page_token)
            response = request.execute()

            for com in range(len(response['items'])):
                video_request = youtube.videos().list(
                        part='snippet',
                        id = response['items'][com]['snippet']['videoId'])
                video_response = video_request.execute()

                comment_data = dict(channel_name = video_response['items'][0]['snippet']['channelTitle'],
                            video_name = video_response['items'][0]['snippet']['title'],
                            comment = response['items'][com]['snippet']['topLevelComment']['snippet']['textOriginal'])
                comments.append(comment_data)
                #comments.append(response['items'][com]['snippet']['topLevelComment']['snippet']['textOriginal'])

            next_page_token = response.get('nextPageToken')

comments_df = pd.DataFrame(comments)
comments_df.to_csv('./all_comments.csv', index=False, encoding='utf-8')



    
"""
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
channel_stats_df.to_csv('./channel_stats.csv', header=channel_stats_df.columns, index=False, encoding='utf-8')

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

def get_comments(youtube, channel_ids):

    comments = []

    request = youtube.commentThreads().list(
                part='snippet, replies',
                allThreadsRelatedToChannelId = channel_ids,
                maxResults = 50)
    response = request.execute()

    for i in range(len(response['items'])):
        comments.append(response['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])

    return comments

comments = (get_comments(youtube, channel_ids))

all_comments_df = pd.DataFrame(comments)
all_comments_df.to_csv('./all_comments.csv')

print(all_comments_df)
#channel_statistics = get_channel_statistics(youtube, channel_ids)

#channel_stats = pd.DataFrame(channel_statistics)

print(channel_stats_df)
"""
