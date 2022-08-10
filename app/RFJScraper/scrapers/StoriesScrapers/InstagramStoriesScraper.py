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

def check(browser, repo:Repository) :
    try:
        posts = []
        profiles = repo.get_profiles('instagram.com/', any=True)
        for profile in profiles :
            posts += scrape(browser, repo, profile)
        repo.add_many_posts(reversed(posts))
        browser.get("https://www.google.com/")
        if len(posts) > 0 :
            print(f'{len(posts)} Instagram stories were scraped with Browser - {datetime.now()}')
        
    except :
        print(f'Instagram Stories Expeption - {datetime.now()}')
        #raise
    
def scrape(browser:Chrome, repo:Repository, profile) :
    posts = []
    browser.get(profile['url'].replace('instagram.com/', 'instagram.com/stories/'))
    #wait for load
    try:
        start_stories_btn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div>div>button")))
    except:
        return []
    if '/stories/' not in browser.current_url:
        return []
    start_stories_btn.click()
    browser.set_window_size(900, 900) 
    
    while True:
        post = {}
        post['url'] = browser.current_url
        uid = re.findall(r"(?<=\/)\d+(?=\/$)", post['url'])

        if post['url'] == 'https://www.instagram.com/' :
            break

        next = browser.find_element_by_css_selector('.coreSpriteRightChevron')

        if uid and repo.try_to_get_post_by_uid(uid[0]) == None:
            post['uid'] = uid
        else:
            next.click()
            continue

        published_at = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'time'))).get_attribute('datetime')
        root = browser.find_element_by_css_selector('section')
        img = root.find_element_by_css_selector('img')

        post['poster_id'] = profile['id']
        post['text'] = 'Story'
        post['images'] = [img.get_attribute('src')]
        post['published_at'] = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%S.000Z")
        post['status'] = 'story'

        #get screen
        img_path = f"..//..//public//images//screenshots//{post['uid'][0]}.png"
        root = root.find_element_by_css_selector("section>div>div>section>div")
        root.screenshot(img_path)
        
        next.click()

        posts.append(post)
    browser.set_window_size(900, 1100) 
    return posts
    