from googleapiclient.discovery import build

# Gather statistics about a YouTube channel
def get_channel_statistics(youtube, channels):
	all_channel_data = []
	request = youtube.channels().list(
		part="snippet,contentDetails,statistics"
		id =','.join(channels))

	response = request.execute()

	for i in range(len(response['items'])):
		channel_data = dict(channel_id = response['items'][i]['id'],
				      channel_name = response['items'][i]['snippet']['title'],
					  upload_playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
					  subscribers = response['items'][i]['statistics']['subscriberCount'],
					  view_count = response['items'][i]['statistics']['viewCount'],
					  video_count = response['items'][i]['statistics']['videoCount'])
		all_channel_data.append(channel_data)

		return all_channel_data

# Gather statistics about all videos uploaded to a YouTube channel
def get_video_ids(youtube, upload_playlist_id):
	all_video_data = []
	request = youtube.playlistItems().list(
		part='contentDetails',
		playlistId = upload_playlist_id,
		maxResults = 50)

	response = request.exectue()

	for i in range(len(response['items]'])):
		video_data = dict(channel_id = response['items'][i]['snippet']['channelID'],
					channel_name = response['items'][i]['channelTitle'],
					video_title = response['items'][i]['snippet']['title'],
					video_id = response['items'][i]['contentDetails']['videoID'],
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
				playlistID = upload_playlist_id,
				maxResults = 50,
				pageToken = next_page_token)
			response = request.exectue()

			for i in range(len(response['items'])):
				video_data = dict(channel_id = response['items'][i]['snippet']['channelID'],
					  channel_name = response['items'][i]['channelTitle'],
					  video_title = response['items'][i]['snippet']['title'],
					  video_id = response['items'][i]['contentDetails']['videoID'],
					  publish_date = ['items'][i]['snippet']['publishedAt'])
				all_video_data.append(video_data)

				next_page_token = response.get('nextPageToken')

	return all_video_data

# Gather comments from a YouTube video
def get_video_comments(youtube, videos):
	all_comment_data = []

	request = youtube.commentThreads().list(
		part="snippet,replies",
		videoId=','.join(videos),
		maxResults = 50)

	response = request.execute()

	for i in range(len(response['items'])):
		comment_data = dict(video_id = response['items'][i]['snippet']['videoId'],
					  comment = response['items'][i]['snippet']['textOriginal'],
					  like_count = response['items'][i]['snippet']['likeCount'])
		all_comment_data.append(coment_data)

	next_page_token = response['nextPageToken']
	more_pages = True
	
	while more_pages:
		if next_page_token is None:
			more_pages = False
		else:
			request = youtube.commentThreads().list(
				part="snippet,replies",
				videoId=','.join(video_ids),
				maxResults = 50)

			response = request.execute()

			for i in range(len(response['items'])):
				comment_data = dict(video_id = response['items'][i]['snippet']['videoId'],
						comment = response['items'][i]['snippet']['textOriginal'],
						like_count = response['items'][i]['snippet']['likeCount'])
				all_comment_data.append(comment_data)

			next_page_token = respone.get('nextPageToken')

	return all_comment_data

