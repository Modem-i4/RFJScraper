import time
from datetime import datetime, timedelta
from io import BytesIO
import os
import re
from pprint import pprint as pp

import tweepy
from PIL import Image
from Repository import Repository
from scrapers.Verifier import check_for_delete
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def api_check(api:tweepy.API, browser:Chrome, repo:Repository) :
    try:
        posts = []
        profiles = repo.get_profiles('twitter.com/', with_uid=True)

        for profile in profiles :
            new_posts_amount = 0
            try:
            	raw_posts = api.user_timeline(profile['uid'], tweet_mode='extended')
            except:
                continue
            for raw_post in raw_posts :
                post = {}
                post['url'] = f"https://twitter.com/{raw_post.author.screen_name}/status/{raw_post.id}"
                post['uid'] = raw_post.id_str
                post['poster_id'] = profile['id']
                post['text'] = raw_post.full_text    
                if post['text'] != '' :

                    urls = re.findall(r'(https?:\/\/[^\s]+)', post['text'])

                    for url in urls :

                        post['text'] = post['text'].replace(url, f'<a href="{url}" target="_blank">{url}</a>')

                    hashtags = re.findall(r'(#[^\s]+)', post['text'])

                    for hashtag in hashtags :

                        post['text'] = post['text'].replace(hashtag, f'<a href="https://twitter.com/hashtag/{hashtag[1:]}" target="_blank">{hashtag}</a>')

                    mentions = re.findall(r'(@[^\s]+)', post['text'])

                    for mention in mentions :

                        post['text'] = post['text'].replace(mention, f'<a href="https://twitter.com/{mention[1:]}" target="_blank">{mention}</a>')


                if hasattr(raw_post, 'extended_entities') :
                    post['images'] = [media['media_url_https'] for media in raw_post.extended_entities['media']]
                else :
                    post['images'] = []
                post['published_at'] = raw_post.created_at
                post['status'] = 'usual'

                if repo.try_to_get_post_by_uid(post['uid'], extra_info=False) is None : #if post is new - make a screenshot
                    browser.get(post['url'])
                    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article')))
                    img_path = f"..//..//public//images//screenshots//{post['uid']}.png"
                    time.sleep(1)
                    articles = browser.find_elements_by_css_selector('article')
                    if raw_post.in_reply_to_status_id == None: #with no replies
                        articles[0].screenshot(img_path)
                    else : #with replies
                        #hide headers
                        header = browser.find_element_by_css_selector('div[data-testid=primaryColumn]>div>div')
                        browser.execute_script('arguments[0].remove()', header)
                        output = Image.new("RGBA", (0, 0))
                        for i, article in enumerate(articles) :
                            if i>4:
                                break
                            try:
                                browser.execute_script("arguments[0].scrollIntoView(true)", article)
                                article.screenshot("temp.png")
                            except:
                                break
                            img = Image.open("temp.png")
                            height = output.height + img.height
                            width = max(output.width, img.width)
                            new_img = Image.new("RGBA", (width, height))
                            new_img.paste(output)
                            new_img.paste(img, (0, output.height))
                            output = new_img
                        output.save(img_path)
                        os.remove("temp.png")
                    new_posts_amount += 1
                    posts.append(post)
            check_for_delete(repo, profile, [{'id': raw_post.id_str} for raw_post in raw_posts], new_posts_amount)
        if len(posts) > 0 :
            print(f'{len(posts)} new Twitter posts were scraped with API - {datetime.now()}')
        repo.add_many_posts(reversed(posts))
        browser.get("https://www.google.com/")
    except :
        print(f'Twitter API Exception - {datetime.now()}')
        #raise
