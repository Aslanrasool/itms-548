import praw
import datetime
from key_contents import query_keywords

client_id = '68n97pmuxvLUfkVHxU7w-w'
client_secret = 'bX25ZyAiK9Dg0-h423W5jQkRlDhArw'
user_agent = 'python:islfo:v1.0.0 (by /u/itm448)'
username = 'itm448'
password = 'Chicago12345!'

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)

def search_posts(subreddit_name, query, limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    return subreddit.search(query, limit=limit)

def utc_to_local(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

subreddit_name = 'AskReddit'
limit = 10

# Use the query_keywords variable imported from key_content.py
posts = search_posts(subreddit_name, query_keywords, limit)

for post in posts:
    print(f"Author: {post.author}")
    print(f"Date posted: {utc_to_local(post.created_utc)}")
    print(f"Title (short description): {post.title}")
    print(f"Content link: {post.url}\n")