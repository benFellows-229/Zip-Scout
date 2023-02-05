from flask import Flask
from flask import request
import json
import http.client
import praw
import random
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def handle_request():
    text = str(request.args.get('input'))

    if text == "New York City":
        text = "NYC"

    if text == "Richmond":
        text = "rva"

    if text == "Madison":
        text = "MadisonWI"




    headers = {
        'X-RapidAPI-Key': "e375110e3cmshaf77ee007d8b4f6p1b083fjsn1e170d0c3e46",
        'X-RapidAPI-Host': "zillow56.p.rapidapi.com"
        }
    conn = http.client.HTTPSConnection("zillow56.p.rapidapi.com")
    conn.request("GET", "/search?location=houston%2C%20tx", headers=headers)
    j = 0
    res = conn.getresponse()
    data = res.read()
    foo = json.loads(data)
    bar = foo.get("results")
    price = bar[0].get("price")
    for i in range (len(bar)):
        price = price + bar[i].get("price")
        j += 1
    average = price/j
    city_name = text.replace(" ","")



    reddit = praw.Reddit(client_id="fPz5Y9NZMPnwLabdY2cwBQ", client_secret="DtkkyKGailJgGVnHkPMIOwYb7YAfSg", user_agent="my_user_agent")

    subreddit_names = [city_name]  # List of subreddit names to process

    for subreddit_name in subreddit_names:
        subreddit = reddit.subreddit(subreddit_name)  # Get the subreddit

        post_count = 100

        top_posts = subreddit.hot(limit=post_count)  # Get the top 100 posts in the subreddit
        score = 0
        counter = 0

        for post in top_posts:
            counter = counter + 1

            # Get the text of the post
            text = post.title + " " + post.selftext
            sentiment = sia.polarity_scores(text)["compound"]
            random_num = random.randrange(0,100)
            if counter == random_num:
                rtext = text
            score = score + sentiment

    score = score/post_count

    score = ((score / 2) + .5) * 100

    data_set = {"response": {"input": city_name, "score": score, "reddit_text": rtext}}
    json_dump = json.dumps(data_set)
    return json_dump
