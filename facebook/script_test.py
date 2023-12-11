from facebook_scraper import *
import os

# enable_logging()
print("Hola")
for post in get_posts(account="nintendo", start_url="https://mbasic.facebook.com/nintendo?v=timeline",
              cookies=os.getcwd() + "/cookies.json"):
    print("x")
    print(post['text'][:50])
