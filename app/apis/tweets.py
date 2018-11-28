from flask_restplus import Namespace, Resource, fields
from flask import abort
from app.db import tweet_repository
from app.models import Tweet as TweetModel

api = Namespace('tweets')

tweet = api.model('Tweet', {
    'id': fields.Integer,
    'text': fields.String,
    'created_at': fields.DateTime
})

new_tweet = api.model('New tweet', {
    'text': fields.String(required=True)
})

@api.route('/<int:id>')
@api.response(404, 'Tweet not found')
@api.param('id', 'The tweet unique identifier')
class Tweet(Resource):
    @api.marshal_with(tweet)
    def get(self, id):
        tweet = tweet_repository.get(id)
        if tweet is None:
            api.abort(404,  "Tweet {} doesn't exist".format(id))
        else:
            return tweet

@api.route('')
@api.response(422, 'Invalid tweet')
class CreateTweet(Resource):
    @api.marshal_with(tweet, code=201)
    @api.expect(new_tweet, validate=True)
    def post(self):
        text = api.payload["text"]
        if len(text) > 0:
            tweet = TweetModel(text)
            tweet_repository.add(tweet)
            return tweet, 201
        else:
            return abort(422, "Tweet text can't be empty")
