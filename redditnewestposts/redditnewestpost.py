import praw
import time

#as reddit handles spam pretty well, this is the best option though its slow
r = praw.Reddit(user_agent='redditnewestpost')
for y in range(1, 2):
    time.sleep(1)
    submissions = r.get_new(limit=5)
    for x in submissions:
        print(str(x))