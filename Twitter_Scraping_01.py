# Import required modules
import pandas as pd
import pymongo
import streamlit as st
import snscrape.modules.twitter as sntwitter
from PIL import Image

# Load image
image = Image.open(r"C:\Users\cprat\OneDrive\Pictures\Saved Pictures\how-to-scrape-twitter-step-by-step-guide.jpg")

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
Search = hashtag + f" since:{start_date}"+f" until:{end_date}"


# Create text input for the limit of tweets to be scraped
limit = st.number_input("Enter the limit of tweets to be scraped>>>", min_value=1, max_value=1000, value=100)


# Scrape tweets containing the hashtag
tweets = []
if hashtag:
    for tweet in sntwitter.TwitterSearchScraper(Search).get_items():
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
      collection = db[str(limit)+'_'+hashtag+"_"+str(start_date)+"_"+str(end_date)]


      # Converts the dataframe  into a dictionary format
      # "records" specifying that each row of the dataframe to be a dictionary
      data_dict = data.to_dict("records")

      # Inserts the dataframe in selected collection.
      collection.insert_many(data_dict)

      #Finally
      st.success('Data uploaded to the database')


# Add a button to download the data in CSV format
if st.button('Download as CSV'):
    data.to_csv(f"{str(limit)+'_'+hashtag+'_'+str(start_date)+'_'+str(end_date)}_tweets.csv", index=False)
    st.success('Data downloaded as CSV')

# Add a button to download the data in JSON format
if st.button('Download as JSON'):
    data.to_json(f"{str(limit)+'_'+hashtag+'_'+str(start_date)+'_'+str(end_date)}_tweets.json",orient='records', force_ascii=False, indent=4, default_handler=str)
    st.success('Data downloaded as JSON')
