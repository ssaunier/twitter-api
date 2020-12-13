from flask_restx import Namespace, Resource, fields
from app.db import tweet_repository
from app.models import Tweet

api = Namespace('tweets')  # Base route

json_tweet = api.model('Tweet', {
    'id': fields.Integer(required=True),
    'text': fields.String(required=True, min_length=1),
    'created_at': fields.DateTime(required=True),
})

json_new_tweet = api.model('New tweet', {
    'text': fields.String(required=True, min_length=1),  # Don't allow empty string
})

@api.route('/<int:tweet_id>')  # route extension (ie: /tweets/<int:id>)
@api.response(404, 'Tweet not found')
@api.param('tweet_id', 'The tweet unique identifier')
class TweetResource(Resource):
    @api.marshal_with(json_tweet)  # Used to control JSON response format
    def get(self, tweet_id):  # GET method
        tweet = tweet_repository.get(tweet_id)
        if tweet is None:
            api.abort(404)  # abort will throw an exception and break execution flow (equivalent to 'return' keyword for an error)
        return tweet, 200

    @api.marshal_with(json_tweet, code=200)
    @api.expect(json_new_tweet, validate=True)  # Used to control JSON body format (and validate)
    def patch(self, tweet_id):  # PATCH method
        tweet = tweet_repository.get(tweet_id)
        if tweet is None:
            api.abort(404)

        # body is also called payload
        # No need to verify if 'text' is present in body, or if it is a valid string since we use validate=True
        # body has already been validated using json_new_tweet schema
        tweet.text = api.payload['text']
        return None, 204

    def delete(self, tweet_id):  # DELETE method
        tweet = tweet_repository.get(tweet_id)
        if tweet is None:
            api.abort(404)
        tweet_repository.remove(tweet_id)
        return None, 204

@api.route('')  # empty route extension (ie: /tweets)
@api.response(422, 'Invalid tweet')
class TweetsResource(Resource):
    @api.marshal_with(json_tweet, code=201)
    @api.expect(json_new_tweet, validate=True)
    def post(self):  # POST method
        # No need to verify if 'text' is present in body, or if it is a valid string since we use validate=True
        # body has already been validated using json_new_tweet schema
        text = api.payload['text']
        tweet = Tweet(text)
        tweet_repository.add(tweet)
        return tweet, 201

    # Here we use marshal_list_with (instead of marshal_with) to return a list of tweets
    @api.marshal_list_with(json_tweet)
    def get(self):  # GET method
        tweets = tweet_repository.get_all()
        return tweets, 200
