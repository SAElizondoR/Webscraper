from facebook_scraper import *

options = {"posts_per_page": 5, "allow_extra_requests": True}
enable_logging()
# set_user_agent(
#     "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
# for post in get_posts(
#     post_urls=["https://mbasic.facebook.com/nintendo?v=timeline"],
#     credentials=(config['CS']['uno'], config['CS']['dos']), options=options):
#     print(post)

# for post in get_posts("nintendo",
#     credentials=(config['CS']['uno'], config['CS']['dos']),
#     start_url="https://mbasic.facebook.com/nintendo?v=timeline"):
#     print(post)

for post in get_posts(post_urls=["https://mbasic.facebook.com/nintendo?v=timeline"],
# start_url="https://mbasic.facebook.com/nintendo?v=timeline",
credentials=(config['CS']['uno'], config['CS']['dos'])):
    print(post)


