from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from json import dumps
from . import predict
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
import tweepy
from tweepy import OAuthHandler
import pandas as pd
import emoji
import regex
import string
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
from textblob import TextBlob
def home(request):
    data="hello"
    context={'data':data}
    return render(request,'searching.html',context)


def give_emoji_free_text(text):
    allchars = [str for str in text.decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.decode('utf-8').split() if not any(i in str for i in emoji_list)])
    return clean_text
def message_cleaning(message):
    message=give_emoji_free_text(message.encode('utf8'))
    Test_punc_removed = [char for char in message if char not in string.punctuation]
    Test_punc_removed_join = ''.join(Test_punc_removed)
    Test_punc_removed_join_clean = [word for word in Test_punc_removed_join.split() if word.lower() not in stopwords.words('english')]
    print(Test_punc_removed_join_clean)
    Test_punc_removed_join_clean=' '.join(Test_punc_removed_join_clean)
    return Test_punc_removed_join_clean
def getTweetsFromTwitter(query, count):
    # keys and tokens from the Twitter Dev Console 
	consumer_key = 'bWSGQAFtFckS9F67kByLUwpap'
	consumer_secret = 'XSZ1WzaRtZrvw4vjlXQrTKPo0aHQupaXBnG7pFqBZDv5QMkxWU'
	access_token = '1076360175752142848-DC5o22190Z8fhZdGTgqObDvS7t60sy'
	access_token_secret = 'zvMgOBLGl2vmApKAOlL5qGQw5XSHXzRPSXO7HBqOn4cqA'

		# attempt authentication 
	try: 
			# create OAuthHandler object 
		auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
		auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
		api = tweepy.API(auth) 
	except: 
		print("Error: Authentication Failed") 
      
      # empty list to store parsed tweets 
	tweets = [] 
		
			# call twitter api to fetch tweets 
	rawtweets = api.search(q = query, count = count, lang = 'en')
	print (type(rawtweets))
	print (len(rawtweets))
        
        #Capture tweet and its params into pandas df
	tid = [tweet.id for tweet  in rawtweets]
	tdf = pd.DataFrame(tid, columns = ["id"])
    
	tdf["tweet"] = [tweet.text for tweet in rawtweets]
		
	for rawtweet in rawtweets: 
        # take only text part and clean it
		cleantweet = message_cleaning(rawtweet.text)
		tweets.append(cleantweet) 

		# return cleaned tweets 
	print (tdf.head())
	return tweets 
def getTweetSentiment(all_tweets):
    for tweet in all_tweets:
	    tweet_sentiment = TextBlob(tweet).sentiment
	    yield tweet_sentiment
       
def plotSentiment(all_tweets):
    polarity = []
    subjectivity = []
    global no
    no=[]
    for sentiment in getTweetSentiment(all_tweets):
        polarity.append(sentiment.polarity)
        subjectivity.append(sentiment.subjectivity)
    positive_polarity = [p for p in polarity if p>0]
    negative_polarity = [n for n in polarity if n<0]
    neutral_polarity = [r for r in polarity if r==0]
    total_size = len(positive_polarity) + len(negative_polarity) + len(neutral_polarity)
    no.append(len(neutral_polarity))
    no.append(len(negative_polarity))
    no.append(len(positive_polarity))
    print(no)
    return no
def bargraph(request):
    data=dumps(plotSentiment(all_tweets))
    context={'data':data}
    return render(request,'bargraph.html',context)
    
def results(request):
    global all_tweets
    name=request.POST.get('aname','') 
    query=name
    context={'data':query}
    all_tweets=getTweetsFromTwitter(query,1000)
    tfidf=TfidfVectorizer(max_df=0.90, min_df=2,max_features=1000,stop_words='english')
    tfidf_matrix=tfidf.fit_transform(all_tweets)
    print(tfidf_matrix)
    print(all_tweets)
    data=dumps(plotSentiment(all_tweets))
    print(data)
    context ={'data':data}
    return render(request, 'piechart.html', context)


# Create your views here.
