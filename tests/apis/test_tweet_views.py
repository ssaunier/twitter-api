from flask_testing import TestCase
from app import create_app
from app.models import Tweet
from app.db import tweet_repository

class TestTweetViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app

    def setUp(self):
        tweet_repository.clear() # Upgrade the TweetRepository.__clear() method to public!

    def test_read_many_tweets(self):
        first_tweet = Tweet('First tweet')
        tweet_repository.add(first_tweet)
        second_tweet = Tweet('Second tweet')
        tweet_repository.add(second_tweet)

        response = self.client.get('/tweets')
        response_tweets = response.json
        print(response_tweets)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_tweets), 2)

        response_first_tweet = response_tweets[0]
        self.assertEqual(response_first_tweet['id'], 1)
        self.assertEqual(response_first_tweet['text'], 'First tweet')
        self.assertIsNotNone(response_first_tweet['created_at'])

        response_second_tweet = response_tweets[1]
        self.assertEqual(response_second_tweet['id'], 2)
        self.assertEqual(response_second_tweet['text'], 'Second tweet')
        self.assertIsNotNone(response_second_tweet['created_at'])

    def test_read_one_tweet(self):
        first_tweet = Tweet('First tweet')
        tweet_repository.add(first_tweet)
        response = self.client.get('/tweets/1')
        response_tweet = response.json
        print(response_tweet)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_tweet['id'], 1)
        self.assertEqual(response_tweet['text'], 'First tweet')
        self.assertIsNotNone(response_tweet['created_at'])

    def test_create_one_tweet(self):
        response = self.client.post('/tweets', json={'text': 'New tweet!'})
        created_tweet = response.json

        self.assertEqual(response.status_code, 201)
        self.assertEqual(created_tweet['id'], 1)
        self.assertEqual(created_tweet['text'], 'New tweet!')
        self.assertIsNotNone(created_tweet['created_at'])

    def test_update_one_tweet(self):
        tweet_to_update = Tweet('Tweet to update')
        tweet_repository.add(tweet_to_update)
        response = self.client.patch('/tweets/1', json={'text': 'New text'})

        self.assertEqual(response.status_code, 204)

        # We use direct access to database to validate our operation
        # Database return Tweet instance, not json converted to a dict
        updated_tweet = tweet_repository.get(1)
        self.assertEqual(updated_tweet.id, 1)
        self.assertEqual(updated_tweet.text, 'New text')
        self.assertIsNotNone(updated_tweet.created_at)

    def test_delete_one_tweet(self):
        tweet_to_delete = Tweet('A tweet')
        tweet_repository.add(tweet_to_delete)
        response = self.client.delete('/tweets/1')

        self.assertEqual(response.status_code, 204)

        # We use direct access to database to validate our operation
        self.assertIsNone(tweet_repository.get(1))
