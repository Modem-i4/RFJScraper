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
import scrapers.StoriesScrapers.FacebookStoriesScraper as facebook_stories_scraper

def browser_check(browser, repo) :
    posts = []
    profiles = repo.get_profiles('facebook.com/', with_uid=False)
    for profile in profiles :
        try:
            posts += scrape(browser, repo, profile)
        except:
            print(f'Facebook Browser Exception - {datetime.now()}')
            #raise
        posts += facebook_stories_scraper.scrape(browser, repo, profile)
    repo.add_many_posts(reversed(posts))
    browser.get("https://www.google.com/")
    if len(posts) > 0 :
        print(f'{len(posts)} Facebook posts were scraped with Browser - {datetime.now()}')
        

def scrape(browser:Chrome, repo:Repository, profile) :
    posts = []
    present_posts = []
    url = profile['url'] if '/groups/' not in profile['url'] else profile['url']+"?sorting_setting=CHRONOLOGICAL"
    browser.get(url)
    #wait for load
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span>span>span>a[role=link]")))
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(5)
    #hide not needed headers
    browser.execute_script("arguments[0].setAttribute('style','display:none')", 
                        browser.find_element_by_css_selector('[role=banner]'))
    browser.execute_script("arguments[0].setAttribute('style','display:none')", 
                        browser.find_element_by_css_selector('div[role=main]>div+div+div'))
    

    post_els = find(browser, 'div[role=article][aria-describedby]')
    for post_el in post_els :
        #print(f"start - {datetime.now()}")
        post = {}
        expand_els = post_el.find_elements_by_xpath("//*[contains(text(), 'Mehr ansehen')]")
        if len(expand_els) > 0 :
            try:

                click(browser, expand_els[0])
            except:
                #raise
                pass
        browser.execute_script("arguments[0].scrollIntoView(true)", post_el)
        #get date
        post['published_at'] = get_date(browser, post_el)
        if post['published_at'] is None :
            break
        #get url
        post_url = find_one(post_el, 'span>span>span>a[role=link]')
        post_url = post_url.get_attribute('href')
        post['url'] = re.findall(r'.+(?=__cft__)', post_url)[0].rstrip('?')
        #set uid
        uid = re.findall(r"(?<=story_fbid=)\d+|(?<=&id=)\d*|(?<=\/permalink\/)\d*|(?<=posts\/)\d*", post['url'])
        if uid:
            post['uid'] = uid[0]
        else:
            post['uid'] = re.findall(r"(?<=facebook\.com\/).*", post['url'])[0]
        present_posts.append( {'id': post['uid']} )
        #set poster_id
        post['poster_id'] = profile['id']
        #get text
        text_item = find_one(post_el, 'div>div>div[dir=auto]')
        if text_item is not None :
            post['text'] = text_item.text
        else :
            post['text'] = ''
        #highlight links in text
        if text_item is not None:
            links = find(text_item, 'a')
            for i in range(len(links)) :
                link = links[i]
                link_text = link.text
                href = link.get_attribute('href')
                if '__cft__' in href:
                    href = re.findall(r'.+(?=\__cft__)', href)[0]
                post['text'] = post['text'].replace(link_text,f'<a href="{href}" target="_blank">{link_text}</a>')

        #get images
        images = find(post_el, 'a div img') 
        post['images'] = []
        for image in images :
            if int(image.get_attribute('height')) > 50 :
                post['images'].append(image.get_attribute('src'))
        #print(f"end - {datetime.now()}")
        if not check_for_edit(repo, post, browser, is_browser_based=True, check_images=True):
            #checks if post should be appended
            continue
        #get screen
        img_path = f"..//..//public//images//screenshots//{post['uid']}.png"
        post_el.screenshot(img_path)
        posts.append(post)
    check_for_delete(repo, profile, present_posts, new_posts_amount=len(posts), deep_check=True, browser=browser)
    return posts

def find(find_in, css) :
    return find_in.find_elements_by_css_selector(css)

def find_one(find_in, css) :
    elements = find(find_in, css)
    if len(elements) > 0:
        return elements[0]
    else:
        return None
def click(browser, element) :
   browser.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", element)

def get_date(browser:Chrome, post_el) :

    published_at_el = []
    hover_to_generate_url = find_one(post_el, "span>span>span>a[role=link]")

    while not published_at_el or published_at_el[0].text == '':

        try:
            #browser.execute_script("arguments[0].dispatchEvent(new MouseEvent('mouseover', {bubbles: true}))", hover_to_generate_url)
            hover = ActionChains(browser).move_to_element(hover_to_generate_url)
            hover.perform()
        except:
            #raise
            pass
        published_at_el = browser.find_elements_by_css_selector("span[role=tooltip] span")

        #time.sleep(3)
        #browser.execute_script("arguments[0].dispatchEvent(new MouseEvent('mouseout', {bubbles: true}))", hover_to_generate_url)

    published_at_text = published_at_el[0].text

    published_at = datetime.strptime(published_at_text, '%A, %d. %B %Y um %H:%M') # < de | en > %A, %B %d, %Y at %I:%M %p
    hover = ActionChains(browser).move_by_offset(500,0)    
    hover.perform()
    time.sleep(2)
    #Samstag, 6. Februar 2021 um 11:17

    return published_at
