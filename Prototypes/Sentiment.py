# Donaldson Query Sentiment

# Dogma: sentiment_query_score = sum(channel_score)
#        channel_score = sum(video_score)
#        video_score = (video_views/average_views) * sum(compound_sentiment * likes)

# this script will demonstrate how information is gathered from a clean .csv file and video_score is calculated

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

obj = SentimentIntensityAnalyzer()

# input string (youtube comment)
sentence = "Kyle runs funny as hell👹"


sentiment_dict = obj.polarity_scores(sentence)

print("Sentiment of sentence: ", end='')
print(sentiment_dict)

# Output: "Sentiment of sentence: {'neg': 0.4, 'neu': 0.348, 'pos': 0.252, 'compound': -0.4019}"

# Default Vader Features of interest:
    # 1) can interpret emojis
    # 2) No special consideration for non-english sentences
            # every non-english sentence returns a compound score of 0


with open("/Users/andrewdifranco/Desktop/all_comments.txt", "r") as f:

    newList = []    # stores comments
    likeList = []   # stores No. of likes per comment
    compound_sentiment = [] # stores the compound value per comment
    weightedScore = []  # stores the compound value * the No. of likes
    vv = f.readline()   # video_views read in
    end = vv.find('\n')
    int_vv = int(vv[12:end])
    av = f.readline()   # average_views read in
    end = av.find('\n')
    int_av = int(av[16:end])

    print("video_views:", end =' '), print(int_vv)
    print("average_views:", end =' '), print(int_av)

    # populates likeList and newList array
    for line in f:
        if line[-1] == '\n':
            i = line.find(',') + 1
            likeList.append(line[:i-1]) # saves the likes
            newList.append(line[i:-1])  # saves the comment

    # populates compound_sentiment array
    count1 = 0
    for i in newList:
        print(i)
        sentiment_dict = obj.polarity_scores(i)
        compound_sentiment.append(sentiment_dict['compound'])
        print(sentiment_dict)
        print(compound_sentiment[count1])
        count1 += 1

    # populates weightedScore array
    count2 = 0
    for i in likeList:
        i = float(i)
        weightedScore.append(i * compound_sentiment[count2])
        count2 += 1


    print(weightedScore)
    sum = 0
    for i in range(0, len(weightedScore)):
        sum = sum + weightedScore[i]

    # sum = 74.4217

    video_score = (sum * (int_vv/int_av))
    print(video_score)

    # video_score = 90.3693

f.close()

