from flask import Flask, render_template, jsonify, request
from random import randint
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.Debug = True

db = MongoClient('mongodb://yamil:medalla@troup.mongohq.com:10079/piloto-tweets')['piloto-tweets']
db.authenticate('yamil', 'medalla')
tweets = db.tweets

@app.route('/', methods = ['GET'])
def view_tweets():
	return render_template('index.html', tweets = list(tweets.find()))

@app.route('/tweets', methods = ['GET'])
def return_all_tweets():
	return jsonify({"tweets": list(tweets.find())})

@app.route('/tweets', methods = ['POST'])
def create_tweet():
	# tweets.append({"id": randint(0,256), "text": request.form['tweet']})
	return jsonify({'_id': str(tweets.insert({'text': request.form['tweet']}))})

@app.route('/tweets/<string:id>', methods = ['GET', 'DELETE'])
def handle_single_tweet(id): #bregar con un solo tweet para ver si lo borra o lo muestra 
	if request.method == 'DELETE':
		return jsonify({tweets.remove({'_id': ObjectId(id)})})
	else:
		return jsonify(tweets.find_one({'_id': ObjectId(id)}))
		# for tweet in tweets:
		# 	if tweet.id == id:
		# 		return jsonify(tweet)
		# return jsonify({})

@app.route('/tweets/emailbook', methods = ['POST'])
def  sendgrid_create():
	return jsonify(str(tweets.insert({'text': request.form['subject']})))

if __name__ == '__main__':
		app.run()