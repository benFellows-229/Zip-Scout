from flask import Flask
from flask import request
import json
import praw
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

app = Flask(name)

@app.route('/', methods = ['GET', 'POST'])
def handle_request():
    text = str(request.args.get('input'))

    if text == "New York City":
        text = "NYC"

    if text == "Richmond":
        text = "rva"

    if text == "Madison":
        text = "MadisonWI"

    city_name = text.replace(" ","")



    reddit = praw.Reddit(client_id="fPz5Y9NZMPnwLabdY2cwBQ", client_secret="DtkkyKGailJgGVnHkPMIOwYb7YAfSg", user_agent="my_user_agent")

    subreddit_names = [city_name]  # List of subreddit names to process

    for subreddit_name in subreddit_names:
        subreddit = reddit.subreddit(subreddit_name)  # Get the subreddit

        post_count = 100

        top_posts = subreddit.hot(limit=post_count)  # Get the top 100 posts in the subreddit
        score = 0


        for post in top_posts:
            # Get the text of the post
            text = post.title + " " + post.selftext
            sentiment = sia.polarity_scores(text)["compound"]
            score = score + sentiment

    score = score/post_count

    score = ((score / 2) + .5) * 100

    data_set = {"response": {"input": city_name, "score": score}}
    json_dump = json.dumps(data_set)
    return json_dump