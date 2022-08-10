import facebook
from Repository import Repository
from datetime import datetime
import re
from scrapers.Verifier import check_for_edit, check_for_delete
    
def api_check(graph:facebook, browser, repo:Repository) :
    try:
        posts = []
        profiles = repo.get_profiles('facebook.com/', with_uid=True)
        for profile in profiles :
            new_posts_amount = 0
            raw_posts = graph.get_object(id=profile['uid'], fields="feed.limit(5){message,permalink_url,created_time,attachments{subattachments{media}}}")
            raw_posts = raw_posts['feed']['data']
            
            for raw_post in raw_posts :
                post = {}
                post['url'] = raw_post['permalink_url']
                post['uid'] = raw_post['id']
                post['poster_id'] = profile['id']

                if 'message' in raw_post :

                    post['text'] = raw_post['message']

                    urls = re.findall(r'(https?:\/\/[^\s]+)', post['text'])

                    for url in urls :

                        post['text'] = post['text'].replace(url, f'<a href="{url}" target="_blank">{url}</a>')

                    hashtags = re.findall(r'(#[^\s]+)', post['text'])

                    for hashtag in hashtags :

                        post['text'] = post['text'].replace(hashtag, f'<a href="https://www.facebook.com/hashtag/{hashtag[1:]}" target="_blank">{hashtag}</a>')



                else:
                    post['text'] = ''            
                if 'attachments' in raw_post :
                    post['images'] = [image['media']['image']['src'] for image in raw_post['attachments']['data'][0]['subattachments']['data']]
                else :
                    post['images'] = []
                post['published_at'] = datetime.strptime(raw_post['created_time'], "%Y-%m-%dT%H:%M:%S+0000") #2021-01-31T13:27:02+0000

                if not check_for_edit(repo, post, browser, main_el_selector="[role=main] [aria-describedby], .h7zd8jcd, #watch_feed .asz1e59d", check_images=True):
                    #checks if post should be appended
                    continue

                new_posts_amount += 1
                posts.append(post)
            if len(posts) > 0 :
                print(f'{len(posts)} Facebook posts were scraped with API - {datetime.now()}')
            check_for_delete(repo, profile, raw_posts, new_posts_amount, deep_check=True, browser=browser)
        repo.add_many_posts(reversed(posts))
        browser.get("https://www.google.com/")
    except :
        print(f'Facebook API Exception - {datetime.now()}')
        raise