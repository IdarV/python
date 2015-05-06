import praw
import time


r = praw.Reddit(user_agent='redditnewestpost')
for y in range(1, 100):
    time.sleep(1)
    submissions = r.get_new(limit=5)
    for x in submissions:
        print(str(x))