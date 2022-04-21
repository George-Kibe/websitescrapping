import tweepy
api_consumer_key = "A0TX77r0mYgTNn2w1f3i3FVRo"
api_secret_key = "0RrMobtq1713CY5eYpz6xJA1AjYrjwjEW6x9dKQcukgyx6jOcq"
access_token = "4482741045-WINev6NZ1YLuMDKuj0Ba1N8aJ96JDk8LwMQPGzn"
access_token_secret = "YhESagWC4uc3KI9CWhNpfx0iaLOOzB5HLoPNxiI5I9IJp"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_consumer_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
