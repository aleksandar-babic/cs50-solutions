from flask import Flask, redirect, render_template, request, url_for

import helpers
import sys
import os
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)
    
    # render index template if get_user_timeline returned None
    if tweets == None:
        return redirect(url_for("index"))
        
    #Absolute paths to lists
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")
    
    #Init variables to keep track of tweets
    positive, negative, neutral = 0.0, 0.0, 0.0
    
    #Instantiate Analyzer for single tweet(from Analayzer.py)
    singleTweetAnalyzer = Analyzer(positives,negatives)
    
    #Loop through every tweet
    for tweet in tweets:
        #Analyze tweet
        score = singleTweetAnalyzer.analyze(tweet)
        if score > 0.0:
            positive+=1
        elif score < 0.0:
            negative+=1
        else:
            neutral+=1
    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
