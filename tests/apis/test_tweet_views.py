from flask_testing import TestCase
from app import create_app
from app.models import Tweet

class TestTweetViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app

    def setUp(self):
        tweet_repository.clear() # Upgrade the TweetRepository.__clear() method to public!

    def test_tweet_show(self):
        first_tweet = Tweet("First tweet")
        tweet_repository.add(first_tweet)
        response = self.client.get("/tweets/1")
        response_tweet = response.json
        print(response_tweet)
        self.assertEqual(response_tweet["id"], 1)
        self.assertEqual(response_tweet["text"], "First tweet")
        self.assertIsNotNone(response_tweet["created_at"])

    def test_tweet_create(self):
        response = self.client.post("/tweets", json={'text': 'New tweet!'})
        created_tweet = response.json
        self.assertEqual(response.status_code, 201)
        self.assertEqual(created_tweet["id"], 1)
        self.assertEqual(created_tweet["text"], "New tweet!")

    def test_tweet_update(self):
        first_tweet = Tweet("First tweet")
        tweet_repository.add(first_tweet)
        response = self.client.patch("/tweets/1", json={'text': 'New text'})
        updated_tweet = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_tweet["id"], 1)
        self.assertEqual(updated_tweet["text"], "New text")

    def test_tweet_delete(self):
        first_tweet = Tweet("First tweet")
        tweet_repository.add(first_tweet)
        self.client.delete("/tweets/1")
        self.assertIsNone(tweet_repository.get(1))
