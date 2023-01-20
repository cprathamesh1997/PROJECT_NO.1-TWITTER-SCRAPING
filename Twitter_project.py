#TWITTER_SCRAPING

#Import_required_modules
import pandas as pd
import pymongo
import streamlit as st
import snscrape.modules.twitter as sntwitter
import datetime

# Create a text input for the hashtag
hashtag =input('Enter the Username or Hashtag(#example):')


# Connect to the database
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client.twitter_scraped_data


# Scrape tweets containing the hashtag
tweets = []
limit=100
for tweet in sntwitter.TwitterSearchScraper('{}'.format(hashtag)).get_items():
    if len(tweets)== limit:
        break
    else:
         tweets.append({'date': tweet.date, 'id': tweet.id, 'url': tweet.url,'tweet_content': tweet.content,'user': tweet.user.username, 'replyCount': tweet.replyCount, 'retweet_count': tweet.retweetCount,'language': tweet.lang, 'source': tweet.source, 'like_count': tweet.likeCount})


# Store the data in a collection labeled with the hashtag
start_date = datetime.datetime(2023, 1, 1)
end_date = datetime.datetime(2023, 1, 20)
time_interval = end_date - start_date
collection=db[hashtag+str(time_interval)]


 #Add a button to upload the data to the database
if st.button('Upload to database'):
      client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
      db = client.twitter_scraped_data
      collection=db[hashtag+str(time_interval)]
      st.success('Data uploaded to the database')


# Convert the collection to a dataframe
data = pd.DataFrame(list(collection.find()))

#To view dataframe
print(data)

# Download the dataframe in CSV format
data.to_csv(f"{hashtag}_tweets.csv", index=False)

# Download the dataframe in JSON format
data.to_json(f"{hashtag}_tweets.json",orient='records')


