import tweepy
api_consumer_key = "cdP8braWCtTeTkY5ggxOQ3yiX"
api_secret_key = "wGbfVXjFCtJ9HaHfnPMuaor6lx7jgyHixqslS5a56RBvmPhX4f"
access_token = "4482741045-mrZQQ08ynIwKS87IKpnA0KWvquv0J6yA1qK48Dx"
access_token_secret = "o3cOEXxANnPFFP41khx80VlgYg06xlPSXHBROclRjjmDK"


bearer_token = "AAAAAAAAAAAAAAAAAAAAAPbpbgEAAAAAUxATSNES1V54FhAqlRYChfI5kow%3DYcUKdppR3f0lbWEkKKBxgI8e61EBM3j5gt9SOWQOtrH2TxyjWO"

client = tweepy.Client(bearer_token=bearer_token, consumer_key=api_consumer_key, consumer_secret=api_secret_key,
                       access_token=access_token, access_token_secret=access_token_secret)

# response = client.create_tweet(
#     text="Twitter is updating Live", user_auth=True, quote_tweet_id=None)
# print(response)

query = '#marthakarua'
tweets = client.search_recent_tweets(
    query=query,  max_results=10)
for tweet in tweets.data:
    print(tweet.text)
    print(tweet.id)


#retweet = client.retweet(tweet_id, user_auth=True)
print("Code run successfully")
