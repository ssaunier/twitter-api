from unittest import TestCase
from app.models import Tweet  # We will code our `Tweet` class in `app/models.py`

class TestTweet(TestCase):
    def test_instance_variables(self):
        # Create an instance of the `Tweet` class with one argument
        tweet = Tweet("my first tweet")
        # Check that `text` holds the content of the tweet
        self.assertEqual(tweet.text, "my first tweet")
        # Check that when creating a new `Tweet` instance, its `created_at` date gets set
        self.assertIsNotNone(tweet.created_at)
        # Check that the tweet's id is not yet assigned when creating a Tweet in memory
        self.assertIsNone(tweet.id)
