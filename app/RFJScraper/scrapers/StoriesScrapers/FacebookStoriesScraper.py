from scrapers.Verifier import check_for_delete, check_for_edit
from Repository import Repository
import json
import time
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup, element
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome

def check(browser, repo:Repository) :
    posts = []
    profiles = repo.get_profiles('facebook.com/', get_url_with_uid=True)
    for profile in profiles :
        try:
            browser.get(profile['url'])
            #wait for load
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[role]>div>svg>g>[preserveAspectRatio='xMidYMid slice']")))
            posts += scrape(browser, repo, profile)
        except :
            print(f'Facebook Public Pages Stories exception - {datetime.now()}')
            raise
    repo.add_many_posts(reversed(posts))
    browser.get("https://www.google.com/")
    if len(posts) > 0 :
        print(f'{len(posts)} Facebook stories were scraped with Browser - {datetime.now()}')
    
        
    
def scrape(browser:Chrome, repo:Repository, profile) :
    posts = []
    open_stories_btn = browser.find_elements_by_css_selector("circle[r='82'], circle[r='64']")
    if not open_stories_btn or open_stories_btn[0].get_attribute('class') == "m74jz5tg gjkn0k4t":
        return []
    click(browser, open_stories_btn[0])
    open_stories_btn = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[role=menuitem]")))
    browser.set_window_size(900, 900)    
    time.sleep(2)
    click(browser, open_stories_btn)
    
    #WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[tabindex="-1"] [role=button]>div>div[aria-label], [data-pagelet=page] div[role=button]')))
    #next = browser.find_elements_by_css_selector("[role=banner] + span +div [role=button]")
    #if len(next) == 1 :
    #    click(browser, next[0])
    try:
        revealStory = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR,'[role=banner] + span +div [role=button]')))
        revealStory.click()
    except:
        pass
    while True:
        post = {}
        post['url'] = browser.current_url
        try:
            #published_at = WebDriverWait(browser, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR,'[data-pagelet=Stories] div>span>span')))
            #next = browser.find_elements_by_css_selector('div[tabindex="-1"] [role=button]>div>div[aria-label]')[1]
            published_at = WebDriverWait(browser, 4).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.g0qnabr5.ojkyduve')))
            next = browser.find_elements_by_css_selector('[aria-label="„Nächste Karte“-Button"]')[0]
            root = browser.find_element_by_css_selector("[tabindex='-1']>div>div>div>div>div+div")
            text = root.find_elements_by_css_selector('[data-pagelet=Stories]>div>[data-id]>div+div')
            img = root.find_elements_by_css_selector('img')
            if len(img) == 2:
                post['text'] = f"Text Story:\n{text}"
                img = img[0]
            else:
                post['text'] = "Story"
                img = img[1]
        except:
            break
        post['poster_id'] = profile['id']
        post['images'] = [img.get_attribute('src')]
        post['status'] = 'story'
        
        uid = re.findall(r"\d+_\d+_\d+", post['images'][0])
        if uid and repo.try_to_get_post_by_uid(uid[0]) == None and uid[0] not in [p['uid'] for p in posts]:
            post['uid'] = uid[0]
        else:
            break

        published_at = published_at.text.split()

        if published_at[1] == 'Min.':
            td = timedelta(minutes=int(published_at[0]))
        elif published_at[1] == 'Std.':
            td = timedelta(hours=int(published_at[0]))
        else:
            td = timedelta(hours=24)
        post['published_at'] = datetime.now() - td

        #get screen
        img_path = f"..//..//public//images//screenshots//{post['uid']}.png"
        root.screenshot(img_path)
        
        if post not in posts :
            posts.append(post)
        else:
            break
        try:
            click(browser, next)
        except:
            break
        time.sleep(3)
    browser.set_window_size(900, 1100) 
    return posts
    

def click(browser, element) :
   browser.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", element)