#from youtube_data import *
import youtube_data
import csv
import pandas as pd
from decouple import config
import os

api_key = config('API_KEY') # YouTube Data API v3
youtube = youtube_data.build('youtube', 'v3', developerKey=api_key)

def main():

    f = open('C:/Users/McKinley/Source/Repos/Donaldson-YouTube-Analysis/src/data_collection/companies1.csv')
    reader = csv.reader(f)

    channel_ids = []

    for row in reader:
	    channel_ids.append(row[1])

    #channel_statistics = get_channel_statistics(youtube, channel_ids[:50])
    #channel_stats_df = pd.DataFrame(channel_statistics)
    #print(channel_stats_df.columns)
    #print(channel_stats_df.dtypes)
    #print(channel_stats_df)

    choice = -1

    while (choice != 0):
        playlistID = []
        MainMenu()
        
        choice = input("What would you like to do? ")

        if choice == "1":
           print("You have chosen to collect Channel Statistics")
           #print(len(channel_ids))
           channel_ids = openChannelFile()
           channel_statistics = pd.DataFrame(youtube_data.get_channel_statistics(youtube, channel_ids))
           channel_statistics.to_csv('C:/Users/McKinley/Source/Repos/Donaldson-YouTube-Analysis/src/data/channel_statistics.csv', header=channel_statistics.columns, index=False, encoding='utf-8')
           cont = input("Are there any other files of companies you want to gather data for? Y/N ")

           while cont != "N":
                cont = input("Are there any other files of companies you want to gather data for? Y/N ")
 
                if cont.upper() == "Y" or cont == "YES":
                    channel_ids = openChannelFile()
                    channel_statistics_more = pd.DataFrame(youtube_data.get_channel_statistics(youtube, channel_ids))
                    channel_statistics_more.to_csv('C:/Users/McKinley/Source/Repos/Donaldson-YouTube-Analysis/src/data/channel_statistics.csv', mode='a', index=False, header=False)
           
           print(len(channel_statistics))
           #channel_statistics.to_csv('C:/Users/McKinley/Source/Repos/Donaldson-YouTube-Analysis/src/data/channel_statistics.csv', header=channel_statistics.columns, index=False, encoding='utf-8')

          
           print(playlistID) 
           print(len(channel_statistics))

        elif choice == "2":
           #playlist_ids = []
           print("You have chosen to collect Video Statistics")
           channels = pd.read_csv('channel_statistics.csv')

           channel = input("What channel do you want to gather videos from? ")
            
           playlist_id = channels.loc[channels['Channel_name']==channel, 'playlist_id'].iloc[0]

           #for i in range(len(channels)):
           #    playlist_ids.append(channels.loc[i, "playlist_id"])
            
           #print(playlist_ids)
           #print(len(playlist_ids))

           video_statistics = pd.DataFrame(youtube_data.get_video_ids(youtube, playlist_id))
           fileName = channel.replace(" ", "") + "_video_statistics.csv"
           filePath = "C:/Users/McKinley/Source/Repos/Donaldson-YouTube-Analysis/src/data/" + fileName
           video_statistics.to_csv(filePath, header=video_statistics.columns, index=False, encoding='utf-8')
           cont = input("Are there any other files of companies you want to gather data for? Y/N ")

           while cont != "N":
                cont = input("Are there any other files of companies you want to gather data for? Y/N ")
 
                if cont.upper() == "Y" or cont == "YES":
                    playlist_ids = openChannelFile()
                    video_statistics_more = pd.DataFrame(youtube_data.get_channel_statistics(youtube, channel_ids))
                    video_statistics_more.to_csv('C:/Users/McKinley/Source/Repos/Donaldson-YouTube-Analysis/src/data/video_statistics.csv', mode='a', index=False, header=False)
           
           
           
        elif choice == "3":
           video_ids = []
           print("You have chosen to collect video comments")

           channel = input("What channel do you want to gather comments for? ")

           inputFileName = channel.replace(" ", "") + "_video_statistics.csv"
           inputFilePath = "C:/Users/McKinley/Source/Repos/Donaldson-YouTube-Analysis/src/data/" + inputFileName

           videos = pd.read_csv(inputFilePath)
           
           #video_ids.append(videos.loc[:, 'video_id'])
           video_ids = videos['video_id'].tolist()
           print(video_ids)

           video_comments = pd.DataFrame(youtube_data.get_video_comments(youtube, video_ids[0]))
           outputFileName = channel.replace(" ", "") + "_comments.csv"
           outputFilePath = "C:/Users/McKinley/Source/Repos/Donaldson-YouTube-Analysis/src/data/" + outputFileName
           video_comments.to_csv(outputFilePath, header=video_comments.columns, index=False, encoding='utf-8')
           
           for i in range(1, len(video_ids)-1):
               video_comments = pd.DataFrame(youtube_data.get_video_comments(youtube, video_ids[i]))
               #outputFileName = channel.replace(" ", "") + "_comments.csv"
               #outputFilePath = "C:/Users/McKinley/Source/Repos/Donaldson-YouTube-Analysis/src/data/" + outputFileName
               video_comments.to_csv(outputFilePath, mode='a', header=False, index=False, encoding='utf-8')
           cont = input("Are there any other files of companies you want to gather data for? Y/N ")

           while cont != "N":
                cont = input("Are there any other files of companies you want to gather data for? Y/N ")
 
                if cont.upper() == "Y" or cont == "YES":
                    playlist_ids = openChannelFile()
                    video_comments_more = pd.DataFrame(youtube_data.get_video_comments(youtube, video_ids))
                    video_comments_more.to_csv('C:/Users/McKinley/Source/Repos/Donaldson-YouTube-Analysis/src/data/video_statistics.csv', mode='a', index=False, header=False)
        elif choice == "4":
           print("You have chosen to view results")
        elif choice == "0":
            break

    
    return

def MainMenu():
    print("Main Menu:")
    print("1. Collect Channel Statistics")
    print("2. Collect Video Statistics")
    print("3. Collect Video Comments")
    print("4. Collect All Data")
    print("0. Exit")

    return

def openChannelFile():
    working_directory = os.getcwd()
    file_name = input("What is the file you want to use as input? ")
    file_path = "../data/" + file_name
    #print(file_path)

    #f = open('C:/Users/McKinley/Source/Repos/Donaldson-YouTube-Analysis/src/data_collection/companies2.csv')
    f = open(file_name)
    reader = csv.reader(f)

    channel_ids = []

    for row in reader:
        channel_ids.append(row[1])
    
    return channel_ids



if __name__ == '__main__':
    main()