import snscrape.modules.twitter as sntwitter
from urllib.parse import urlparse

def fetch_tweet_text(url: str) -> str:
    try:
        parts = urlparse(url)
        path = parts.path.strip("/").split("/")
        if len(path) >=3:
            tweet_id = path[-1]
        else:
            tweet_id = None
        if not tweet_id:
            return ""
        tweet = sntwitter.TwitterTweetScraper(tweet_id).get_item()
        return tweet.content
    except Exception:
        return ""
