from googleapiclient.discovery import build
import csv

def gather_data():
	api_key = config('API_KEY') # YouTube Data API v3
	youtube = build('youtube', 'v3', developerKey=api_key)

	f = open('C:/Users/McKinley/Source/Repos/Donaldson-YouTube-Analysis/src/data_collection/companies1.csv')
	reader = csv.reader(f)

	channel_ids = []

	for row in reader:
		channel_ids.append(row[1])


def get_channel_statistics(youtube, channel_ids):
	all_channel_data = []
	request = youtube.channels().list(
				part='snippet,contentDetails,statistics',
				id= ','.join(channel_ids),
				maxResults = 50)
	response = request.execute()

	for i in range(len(response['items'])):
		channel_data = dict(Channel_name = response['items'][i]['snippet']['title'],
					Channel_id = response['items'][i]['id'],
					Subscribers = response['items'][i]['statistics']['subscriberCount'],
					Views = response['items'][i]['statistics']['viewCount'],
					Total_videos = response['items'][i]['statistics']['videoCount'],
					playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
		all_channel_data.append(channel_data)

	return all_channel_data

# Gather statistics about all videos uploaded to a YouTube channel
def get_video_ids(youtube, playlist_ids):
	all_video_data = []
	request = youtube.playlistItems().list(
				part='snippet,contentDetails',
				playlistId = playlist_ids, 
				maxResults = 50)
	response = request.execute()

	for i in range(len(response['items'])):
		video_data = dict(channel_id = response['items'][i]['snippet']['channelId'],
					#channel_name = response['items'][i]['channelTitle'],
					video_title = response['items'][i]['snippet']['title'],
					video_id = response['items'][i]['contentDetails']['videoId'],
					publish_date = response['items'][i]['snippet']['publishedAt'])
		all_video_data.append(video_data)

	next_page_token = response['nextPageToken']
	more_pages = True

	while more_pages:
		if next_page_token is None:
			more_pages = False
		else:
			request = youtube.playlistItems().list(
				part="snippet,contentDetails",
				playlistId = playlist_ids,
				maxResults = 50,
				pageToken = next_page_token)
			response = request.execute()

			for i in range(len(response['items'])):
				video_data = dict(channel_id = response['items'][i]['snippet']['channelId'],
					  #channel_name = response['items'][i]['channelTitle'],
					  video_title = response['items'][i]['snippet']['title'],
					  video_id = response['items'][i]['contentDetails']['videoId'],
					  publish_date = response['items'][i]['snippet']['publishedAt'])
				all_video_data.append(video_data)

				next_page_token = response.get('nextpagetoken')
	return all_video_data

# Gather comments from a YouTube video
def get_video_comments(youtube, videos):
	all_comment_data = []

	request = youtube.commentThreads().list(
		part="snippet,replies",
		videoId=videos,
		maxResults = 50)
	response = request.execute()

	for i in range(len(response['items'])):
		comment_data = dict(video_id = response['items'][i]['snippet']['videoId'],
					  comment = response['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'],
					  like_count = response['items'][i]['snippet']['topLevelComment']['snippet']['likeCount'])
		all_comment_data.append(comment_data)

	next_page_token = response.get('nextPageToken')
	more_pages = True
	
	while more_pages:
		if next_page_token is None:
			more_pages = False
		else:
			request = youtube.commentThreads().list(
				part="snippet,replies",
				videoId=videos,
				maxResults = 50)
			response = request.execute()

			for i in range(len(response['items'])):
				comment_data = dict(video_id = response['items'][i]['snippet']['videoId'],
						comment = response['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'],
						like_count = response['items'][i]['snippet']['topLevelComment']['snippet']['likeCount'])
				all_comment_data.append(comment_data)

			next_page_token = response.get('nextPageToken')

	return all_comment_data

