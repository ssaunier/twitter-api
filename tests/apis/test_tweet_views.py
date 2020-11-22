from flask_testing import TestCase
from app import create_app, db
from app.models import Tweet, User

class TestTweetViews(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f"{app.config['SQLALCHEMY_DATABASE_URI']}_test"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_read_many_tweets(self):
        user = User(username='ssaunier')
        first_tweet = Tweet(text='First tweet', user=user)
        second_tweet = Tweet(text='Second tweet', user=user)
        db.session.add(first_tweet)
        db.session.add(second_tweet)
        db.session.commit()

        response = self.client.get('/tweets')
        response_tweets = response.json
        print(response_tweets)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response_tweets), list)
        self.assertEqual(len(response_tweets), 2)

        response_first_tweet = response_tweets[0]
        self.assertEqual(response_first_tweet['id'], 1)
        self.assertEqual(response_first_tweet['text'], 'First tweet')
        self.assertIsNotNone(response_first_tweet['created_at'])
        self.assertEqual(response_first_tweet['user']['username'], "ssaunier")

        response_second_tweet = response_tweets[1]
        self.assertEqual(response_second_tweet['id'], 2)
        self.assertEqual(response_second_tweet['text'], 'Second tweet')
        self.assertIsNotNone(response_second_tweet['created_at'])
        self.assertEqual(response_second_tweet['user']['username'], "ssaunier")

    def test_read_one_tweet(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        db.session.commit()
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
        tweet_to_update = Tweet(text='Tweet to update')
        db.session.add(tweet_to_update)
        db.session.commit()

        response = self.client.patch('/tweets/1', json={'text': 'New text'})

        self.assertEqual(response.status_code, 204)

        # We use direct access to database to validate our operation
        # Database return Tweet instance, not json converted to a dict
        updated_tweet = db.session.query(Tweet).get(1)
        self.assertEqual(updated_tweet.id, 1)
        self.assertEqual(updated_tweet.text, 'New text')
        self.assertIsNotNone(updated_tweet.created_at)

    def test_delete_one_tweet(self):
        tweet_to_delete = Tweet(text='A tweet')
        db.session.add(tweet_to_delete)
        db.session.commit()

        response = self.client.delete('/tweets/1')

        self.assertEqual(response.status_code, 204)

        # We use direct access to database to validate our operation
        deleted_tweet = db.session.query(Tweet).get(1)
        self.assertIsNone(deleted_tweet)
