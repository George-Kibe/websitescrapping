import tweepy
api_consumer_key = "A0TX77r0mYgTNn2w1f3i3FVRo"
api_secret_key = "0RrMobtq1713CY5eYpz6xJA1AjYrjwjEW6x9dKQcukgyx6jOcq"
access_token = "4482741045-WINev6NZ1YLuMDKuj0Ba1N8aJ96JDk8LwMQPGzn"
access_token_secret = "YhESagWC4uc3KI9CWhNpfx0iaLOOzB5HLoPNxiI5I9IJp"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAPbpbgEAAAAAUxATSNES1V54FhAqlRYChfI5kow%3DYcUKdppR3f0lbWEkKKBxgI8e61EBM3j5gt9SOWQOtrH2TxyjWO"

client = tweepy.Client(bearer_token=bearer_token, consumer_key=api_consumer_key, consumer_secret=api_secret_key,
                       access_token=access_token, access_token_secret=access_token_secret)
query = '#marthakarua'
tweets = client.search_recent_tweets(
    query=query,  max_results=10)
for tweet in tweets.data:
    print(tweet.text)


query1 = '#marthakarua -is:retweet'
start_time = '2022-04-20T00:00:00Z'
end_time = '2022-04-21T00:00:00Z'
all_tweets = client.search_all_tweets(query=query1, tweet_fields=[
                                      'context_annotations', 'created_at'], start_time=start_time, end_time=end_time, max_results=10,  user_auth=True, )
for tweet in all_tweets.data:
    print(tweet.text)
    print(tweet.created_at)

client.mentions_timeline()

print("Code completed successfully")
