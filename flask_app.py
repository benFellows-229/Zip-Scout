from flask import Flask
from flask import request
import json
import requests
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

    city_name = text.replace(" ","")

    url = "https://zillow56.p.rapidapi.com/search"

    city = text

    popcity = text

    if popcity == "None":
        popcity = "irvine"

    if text == "New York City":
        popcity = "New York"

    popcity = popcity.replace(" ", "%20")

    popUrl = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-cities-demographics&q=" + popcity + "&facet=city"

    popResponse = requests.request("GET", popUrl)

    w = popResponse.json()
    foo2 = w.get("records")
    population = foo2[0].get("fields").get("total_population")

    querystring = {"location": city}

    headers = {
        "X-RapidAPI-Key": "8626d3be38msh6928ad1d7e29352p118b3djsn1cf85f4e531f",
        "X-RapidAPI-Host": "zillow56.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    j = 0
    foo = response.json()
    price = 0
    bar = foo.get("results")
    picUrl = bar[0].get("imgSrc")
    lat = bar[0].get("latitude")
    lon = bar[0].get("longitude")
    for i in range (len(bar)):
        price = price + bar[i].get("price")
        j += 1
    average = price/j
    url = "https://walk-score.p.rapidapi.com/score"

    querystring = {"lat":lat,"address":"walk-score.p.rapidapi.com","wsapikey":"1de1f30d2a73116864cb49de63357b16","lon":lon,"format":"json","bike":"1","transit":"1"}

    headers = {
        "X-RapidAPI-Key": "e375110e3cmshaf77ee007d8b4f6p1b083fjsn1e170d0c3e46",
        "X-RapidAPI-Host": "walk-score.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    walkData = response.json()
    walkScore = walkData.get("walkscore")




    reddit = praw.Reddit(client_id="fPz5Y9NZMPnwLabdY2cwBQ", client_secret="DtkkyKGailJgGVnHkPMIOwYb7YAfSg", user_agent="my_user_agent")

    subreddit_names = [city_name]  # List of subreddit names to process

    for subreddit_name in subreddit_names:
        subreddit = reddit.subreddit(subreddit_name)  # Get the subreddit

        post_count = 100

        top_posts = subreddit.hot(limit=post_count)  # Get the top 100 posts in the subreddit
        score = 0
        counter = 0
        random_num = random.randrange(0,96)

        for post in top_posts:


            # Get the text of the post
            text = post.title + " " + post.selftext
            sentiment = sia.polarity_scores(text)["compound"]

            if counter == random_num:
                rtext = text
            elif counter == (random_num + 1):
                rtext2 = text
            elif counter == (random_num + 2):
                rtext3 = text

            counter = counter + 1
            score = score + sentiment

    score = score/post_count

    score = ((score / 2) + .5) * 100

    data_set = {"response": {"input": city_name, "score": score, "reddit_text": rtext, "reddit_text2": rtext2,  "reddit_text3": rtext3, "avg": average, "pic_url": picUrl, "population": population, "walk_score": walkScore}}
    json_dump = json.dumps(data_set)
    return json_dump
