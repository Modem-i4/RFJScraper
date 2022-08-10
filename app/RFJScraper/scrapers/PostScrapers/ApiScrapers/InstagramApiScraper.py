from Repository import Repository
from pprint import pprint as pp
from datetime import datetime, timedelta
from pyfacebook import IgBasicApi
import re
from selenium.webdriver import Chrome
from scrapers.Verifier import check_for_edit, check_for_delete

def api_check(api:IgBasicApi, browser:Chrome, repo:Repository) :
    try:
        posts = []
        profiles = repo.get_profiles('instagram.com/', with_uid=True)
        for profile in profiles :
            new_posts_amount = 0
            raw_posts = api.discovery_user_medias(profile['uid'], fields='id, caption, permalink, media_url, timestamp')
            
            for raw_post in raw_posts :
                post = {}
                post['url'] = raw_post.permalink
                post['uid'] = raw_post.id
                post['poster_id'] = profile['id']

                if raw_post.caption is not None :

                    post['text'] = raw_post.caption 

                    hashtags = re.findall(r'(#[^\s]+)', post['text'])

                    for hashtag in hashtags :

                        post['text'] = post['text'].replace(hashtag, f'<a href="https://www.instagram.com/explore/tags/{hashtag[1:]}" target="_blank">{hashtag}</a>')

                    mentions = re.findall(r'(@[^\s]+)', post['text'])

                    for mention in mentions :

                        post['text'] = post['text'].replace(mention, f'<a href="https://instagram.com/{mention[1:]}" target="_blank">{mention}</a>')

                else:

                    post['text'] = ''
                post['images'] = raw_post.media_url if isinstance(raw_post.media_url, list) else [raw_post.media_url]
                post['published_at'] = datetime.strptime(raw_post.timestamp, "%Y-%m-%dT%H:%M:%S+0000")
                post['status'] = 'usual'

                if not check_for_edit(repo, post, browser, main_el_selector="article"):
                    #checks if post should be appended
                    continue
                new_posts_amount += 1
                posts.append(post)
            
            check_for_delete(repo, profile, [{'id': post.id} for post in raw_posts], new_posts_amount)
        if len(posts) > 0 :
            print(f'{len(posts)} new Instagram posts were scraped with API - {datetime.now()}')
        repo.add_many_posts(reversed(posts))
        browser.get("https://www.google.com/")
        
    except :
        print(f'Instagram API Exception - {datetime.now()}')
        #raise
