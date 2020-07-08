import twint
import heapq
import matplotlib.pyplot as plt


def get_top_mentions_hashtags_geo(lat_long, radius, limit):
    twint.output.tweets_list = []
    c = twint.Config()
    c.Hide_output = True  # hides command line verbose output
    c.Limit = limit  # maximum number of tweets to pull
    c.Geo = f"{lat_long},{radius}"
    c.Store_object = True
    c.Store_csv = True
    c.Output = f"{lat_long}-tweets.csv"
    twint.run.Search(c)
    tweets = twint.output.tweets_list
    mentions_dict = {}
    hashtags_dict = {}
    for tweet in tweets:
        for mention in tweet.mentions:
            if mention in mentions_dict:
                mentions_dict[mention] += 1
            else:
                mentions_dict[mention] = 1
        for hashtag in tweet.hashtags:
            if hashtag in hashtags_dict:
                hashtags_dict[hashtag] += 1
            else:
                hashtags_dict[hashtag] = 1
    top_mentions = heapq.nlargest(10, mentions_dict, key=mentions_dict.get)  # gets highest mentions
    top_hashtags = heapq.nlargest(10, hashtags_dict, key=hashtags_dict.get)  # gets highest hashtags

    # makes dictionary of just highest ones
    mentions_ranked = {}
    hashtags_ranked = {}
    for mention in top_mentions:
        mentions_ranked[mention] = mentions_dict[mention]
    for hashtag in top_hashtags:
        hashtags_ranked[hashtag] = hashtags_dict[hashtag]
    plt.barh(range(len(mentions_ranked)), list(mentions_ranked.values()), align='center', color='maroon')
    plt.yticks(range(len(mentions_ranked)), list(mentions_ranked.keys()))
    plt.gca().invert_yaxis()  # just to have the highest bar at the top
    plt.title("Top Mentions of the Geo-location: " + lat_long)
    plt.savefig(lat_long + '-mentions.png', bbox_inches='tight')  # saves the visualization as png
    # plt.savefig(seed_hashtag + '.pdf', bbox_inches='tight')
    plt.show()
    plt.close()
    plt.barh(range(len(hashtags_ranked)), list(hashtags_ranked.values()), align='center', color='maroon')
    plt.yticks(range(len(hashtags_ranked)), list(hashtags_ranked.keys()))
    plt.gca().invert_yaxis()  # just to have the highest bar at the top
    plt.title("Top Hashtags of the Geo-location:" + lat_long)
    plt.savefig(lat_long + '-hashtags.png', bbox_inches='tight')  # saves the visualization as png
    # plt.savefig(seed_hashtag + '.pdf', bbox_inches='tight')
    plt.show()
    plt.close()

    print("List of Top 10 mentions " + lat_long + " :")
    print(top_mentions)  # displays the top 10 hashtags as a list.
    print("List of Top 10 hashtags " + lat_long + " :")
    print(top_hashtags)  # displays the top 15 hashtags as a list.


def main():
    seed_coordinates = ["28.617245604288797, 77.20818042755127"]
    radius = "1km"
    limit = 1000  # limits the number of tweets to pull
    for coordinate in seed_coordinates:
        get_top_mentions_hashtags_geo(coordinate, radius, limit)

if __name__ == "__main__":
	main()