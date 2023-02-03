#TWITTER_SCRAPING

# Import required modules
import pandas as pd
import pymongo
import streamlit as st
import snscrape.modules.twitter as sntwitter
import datetime
from PIL import Image

# Load Image or Gif under Title
image =("https://ucarecdn.com/51e11998-6315-46ef-b39e-40476425efda/")

# Create a GUI using streamlit
st.title("Twitter Scraping")
st.image(image, use_column_width=True)

# Create text input for the hashtag
hashtag = st.text_input("Enter the Username or Hashtag (e.g. #example)>>>")


# Connect to the database
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')

# Mention the required database
database = "Twitter"


# Create date range input
start_date = st.date_input("Enter start date>>>")
end_date = st.date_input("Enter end date>>>")

# Also time_interval
time_interval = end_date - start_date

# Create a limit selector for the number of tweets
limit = st.slider("Select the number of tweets>>>", min_value=1, max_value=1000, value=100)


# Scrape tweets containing the hashtag
tweets = []
if hashtag:
    for tweet in sntwitter.TwitterSearchScraper('{}'.format(hashtag)).get_items():
        if len(tweets)== limit:
            break
        else:
             tweets.append({'date': tweet.date, 'id': tweet.id, 'url': tweet.url,'tweet_content': tweet.content,'user': tweet.user.username, 'replyCount': tweet.replyCount, 'retweet_count': tweet.retweetCount,'language': tweet.lang, 'source': tweet.source, 'like_count': tweet.likeCount})
else:
    st.warning("Please enter a valid hashtag or username")

# Convert the collection to a dataframe
data = pd.DataFrame(tweets)

# Display the dataframe
st.dataframe(data)


# Add a button to upload the data to the database
if st.button('Upload to database'):

      #Required_Database
      db = client[database]

      # Creates a new collection name in database.
      collection = db[hashtag + str(time_interval)]


      # Converts the dataframe  into a dictionary format.
      # With the argument "records" specifying that each row of the dataframe should be a dictionary
      data_dict = data.to_dict("records")

      # Inserts the dataframe in selected collection.
      collection.insert_many(data_dict)

      #Finally
      st.success('Data uploaded to the database')


# Add a button to download the data in CSV format
if st.button('Download as CSV'):
    data.to_csv(f"{hashtag}_tweets.csv", index=False)
    st.success('Data downloaded as CSV')

# Add a button to download the data in JSON format
if st.button('Download as JSON'):
    data.to_json(f"{hashtag}_tweets.json",orient='records', force_ascii=False, indent=4, default_handler=str)
    st.success('Data downloaded as JSON')


