import praw

# Fill in your Reddit API keys from https://www.reddit.com/prefs/apps
reddit = praw.Reddit(
    client_id="aVBYhAN7UOiQVNj9wafYcw",
    client_secret="VU1lO4w9P30sobTQSeu5i8Oek-WRmQ",
    user_agent="exercise_scraper 1.0 by JustARedDesign"
)

posts = []
scores = []

subreddit = reddit.subreddit("fitness")
for post in subreddit.search("Victory Sunday", limit=95):
    if (input("continue y/n: ") == 'n'):
        break
    print(f"Title: {post.title}")
    if (input('k?') =='k'):
        print(f"Text: {post.selftext}")
        s = input('score: ')
        if s != 'x':
            posts.append(post.selftext)
            scores.append(float(s))
        post.comments.replace_more(limit=0)
        for comment in post.comments:
            if (input("continue y/n: ") == 'n'):
                break
            print(f"Text: {comment.body}")
            s = input('score: ')
            if s != 'x':
                posts.append(comment.body)
                scores.append(float(s))

print(posts)
print(scores)