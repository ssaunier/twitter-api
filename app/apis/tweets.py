from flask_restplus import Namespace, Resource, fields
from app.db import tweet_repository

api = Namespace('tweets')

tweet = api.model('Tweet', {
    'id': fields.Integer,
    'text': fields.String,
    'created_at': fields.DateTime
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
