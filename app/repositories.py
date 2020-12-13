class TweetRepository:
    def __init__(self):
        self.clear()

    def add(self, tweet):
        self.tweets.append(tweet)
        tweet.id = self.next_id
        self.next_id += 1

    def get(self, id):
        for tweet in self.tweets:
            if tweet.id == id:
                return tweet
        return None

    def get_all(self):
        return self.tweets

    def remove(self, id):
        self.tweets = [tweet for tweet in self.tweets if tweet.id != id]

    def clear(self):
        self.tweets = []
        self.next_id = 1
