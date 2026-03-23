import os
import json
from datetime import datetime
from dotenv import load_dotenv
import praw
from src.utils.logger import get_logger

logger = get_logger("RedditProducer")

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv(
    "REDDIT_USER_AGENT", "python:po_spectrum_dw:1.0 (public opinion analysis)"
)
REDDIT_SUBREDDIT = os.getenv("REDDIT_SUBREDDIT", "all")
REDDIT_LIMIT = int(os.getenv("REDDIT_LIMIT", "100"))
REDDIT_TIME_FILTER = os.getenv("REDDIT_TIME_FILTER", "week")


def get_reddit_client():
    """Build authenticated PRAW client."""
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        raise ValueError(
            "REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET must be set in .env. "
            "Create a script app at https://www.reddit.com/prefs/apps"
        )
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )


def fetch_posts_by_keyword(keyword: str, limit: int = None, time_filter: str = None):
    """
    Search Reddit for posts containing the given keyword.
    Returns a list of post dicts suitable for JSON serialization.
    """
    limit = limit or REDDIT_LIMIT
    time_filter = time_filter or REDDIT_TIME_FILTER

    logger.info(f"Searching r/{REDDIT_SUBREDDIT} for '{keyword}' (limit={limit}, time={time_filter})")

    reddit = get_reddit_client()
    subreddit = reddit.subreddit(REDDIT_SUBREDDIT)
    posts = []

    try:
        for submission in subreddit.search(keyword, limit=limit, time_filter=time_filter):
            posts.append({
                "id": submission.id,
                "title": submission.title,
                "selftext": submission.selftext[:5000] if submission.selftext else "",
                "score": submission.score,
                "num_comments": submission.num_comments,
                "created_utc": submission.created_utc,
                "subreddit": str(submission.subreddit),
                "author": str(submission.author) if submission.author else "[deleted]",
                "url": submission.url,
                "permalink": f"https://reddit.com{submission.permalink}",
                "is_self": submission.is_self,
                "over_18": submission.over_18,
                "keyword": keyword,
            })
    except Exception as e:
        logger.error(f"Reddit search failed: {e}")
        raise

    logger.info(f"Retrieved {len(posts)} posts for keyword '{keyword}'")
    return posts


def save_to_bronze(posts: list, keyword: str):
    """Write posts to the bronze raw layer."""
    os.makedirs("data/raw", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/raw/reddit_posts_{keyword}_{timestamp}.json"

    try:
        with open(filename, "w") as f:
            json.dump(posts, f, indent=2)
        logger.info(f"Bronze layer updated: {filename}")
    except IOError as e:
        logger.critical(f"Disk write failed: {e}")
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch Reddit posts by keyword")
    parser.add_argument("keyword", help="Search term (e.g. inflation, healthcare)")
    parser.add_argument("-l", "--limit", type=int, default=None, help="Max posts to fetch")
    parser.add_argument(
        "-t", "--time",
        choices=["hour", "day", "week", "month", "year", "all"],
        default=None,
        help="Time window for results",
    )
    args = parser.parse_args()

    logger.info("Starting Reddit ingestion pipeline...")
    posts = fetch_posts_by_keyword(args.keyword, limit=args.limit, time_filter=args.time)

    if posts:
        save_to_bronze(posts, args.keyword.replace(" ", "_"))
    else:
        logger.warning("Pipeline finished with no posts ingested.")
