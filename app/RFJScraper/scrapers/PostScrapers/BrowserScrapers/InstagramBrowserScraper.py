from scrapers.Verifier import check_for_delete, check_for_edit
from Repository import Repository
import json
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup, element
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome

def browser_check(browser, repo) :
    try:
        posts = []
        profiles = repo.get_profiles('instagram.com/', with_uid=False)
        for profile in profiles :
            posts += scrape(browser, repo, profile)
        repo.add_many_posts(reversed(posts))
        browser.get("https://www.google.com/")
        if len(posts) > 0 :
            print(f'{len(posts)} Instagram posts were scraped with Browser - {datetime.now()}')
    except :
        print(f'Instagram Browser Exception - {datetime.now()}')
        #raise
    
def scrape(browser:Chrome, repo:Repository, profile) :
    posts = []
    browser.get(f"{profile['url']}/?__a=1")
    try:
        raw_posts = json.loads(browser.find_element_by_tag_name('pre').text)['graphql']['user']['edge_owner_to_timeline_media']['edges']
    except:
        return []
    for raw_post in raw_posts :
        post = {}
        raw_post = raw_post['node']
        post['poster_id'] = profile['id']
        post['uid'] = raw_post['id']
        text_el = raw_post['edge_media_to_caption']['edges']

        if text_el :

            post['text'] = text_el[0]['node']['text']

            hashtags = re.findall(r'(#[^\s]+)', post['text'])

            for hashtag in hashtags :

                post['text'] = post['text'].replace(hashtag, f'<a href="https://www.instagram.com/explore/tags/{hashtag[1:]}" target="_blank">{hashtag}</a>')

            mentions = re.findall(r'(@[^\s]+)', post['text'])

            for mention in mentions :

                post['text'] = post['text'].replace(mention, f'<a href="https://instagram.com/{mention[1:]}" target="_blank">{mention}</a>')

        else : 

            post['text'] = ''
        if 'edge_sidecar_to_children' in raw_post :
            post['images'] = [raw_img['node']['video_url'] if raw_img['node']['is_video'] else raw_img['node']['display_url']
                for raw_img in raw_post['edge_sidecar_to_children']['edges']]
        else :
            post['images'] = [ raw_post['display_url'] ]
        post['published_at'] = datetime.fromtimestamp(raw_post['taken_at_timestamp'])
        post['url'] = f"https://www.instagram.com/p/{raw_post['shortcode']}"
        
        if not check_for_edit(repo, post, browser, is_browser_based=True):
            #checks if post should be appended
            continue
        posts.append(post)
    for post in posts :
        #get screen
        browser.get(post['url'])
        post_el = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article')))
        for screen_id in range(len(post['images'])) :
            img_path = f"..//..//public//images//screenshots//{post['uid']}_{screen_id}.png"
            post_el.screenshot(img_path)
            try:
                next = WebDriverWait(browser, 0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.coreSpriteRightChevron')))
                next.click()
                time.sleep(0.5)
            except:
                break
    check_for_delete(repo, profile, [post['node'] for post in raw_posts], new_posts_amount=len(posts))
    return posts