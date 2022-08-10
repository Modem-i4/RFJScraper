import re
import sys
import os
import json
import dotenv
import time

import requests
import tweepy
from bs4 import BeautifulSoup
from ProfileRepository import ProfileRepository
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


dotenv.load_dotenv()

TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_KEY = os.getenv("TWITTER_ACCESS_KEY")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_BUSINESS_ID = os.getenv("INSTAGRAM_BUSINESS_ID")

options = Options()
options.add_argument("log-level=3")
#options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--user-data-dir=/root/.config/google-chrome/")

url = sys.argv[1]
if 'https://' not in url:
    url = 'https://' + url
if url[-1] == '/' :
    url = url[:-1]
url = url.replace('https://m.','https://')

repo = ProfileRepository()
if not repo.check_if_in_db(url) :
    name = ''
    picture = ''
    uid = ''
    is_group = False
    if 'facebook.com/' in url :
        url = url.replace('facebook.com/friends', 'facebook.com')
        url_end = re.findall(r'(?<=facebook.com\/).*$', url)[0]
        temp_url = "https://m.facebook.com/" + url_end + ("&" if "?" in url else "?") + "brand_redir=DISABLE&locale=de_DE"
        soup = ''
        try:
            html = requests.get(temp_url)
            soup = BeautifulSoup(html.text, features="lxml")
            name = soup.select_one('meta[property="og:title"]').get('content','')
            if 'Bei Facebook anmelden' in name :
                raise
            if soup.select_one('#pages_follow_action_id') != None :
                uid = url_end #page name
            else:
                uid = ''
            picture = soup.select_one('meta[property="og:image"]').get('content', '')
            if 'lookaside' in picture:
                is_group = True
        except:
            #browser = Chrome('/chromedriver', options=options)
            browser = Chrome("C:\Projects\RFJScraper\app\RFJScraper\chromedriver.exe", options=options)
            browser.get(url)
            raw_name = browser.title
            name = raw_name.replace(" | Facebook", "").replace(" Öffentliche Gruppe","")
            name = re.sub(r'^\([0-9]*\) ', '', name)
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'image')))
            time.sleep(0.3)
            raw_picture = browser.find_elements_by_css_selector('image[style="height: 132px; width: 132px;"], image[style="height: 116px; width: 116px;"]')
            #print(raw_picture[0].get_attribute('xlink:href'))
            if not raw_picture :
                raw_picture = browser.find_elements_by_css_selector('image[style="height: 168px; width: 168px;"], image[style="height: 152px; width: 152px;"]')
            else:
                uid = re.findall(r'(?<=facebook\.com\/).+', url)[0]
                if '-' in uid :
                    uid = re.findall(r'(?<=-)\d+', uid)[0]

            if raw_picture :
                picture = raw_picture[0].get_attribute('xlink:href')
            else:
                picture = 'images/group.jpg'
                
            browser.quit()
    elif 'instagram.com/' in url :
        username = re.findall(r'(?<=com\/).+(?=\/|$)', url)[0]
        try:
            html = requests.get(f'https://www.instagram.com/{username}/?__a=1')
            soup = BeautifulSoup(html.text, 'lxml')
            root = soup.select_one('p')
            data = json.loads(root.text)['graphql']['user']
            name = f"{data['full_name']} (@{data['username']})"
            picture = data['profile_pic_url_hd']
            if data['is_business_account'] == True :
                uid = data['fbid']
            else:
                uid = ''
        except:
            #browser = Chrome('/chromedriver', options=options)
            browser = Chrome("C:/Projects/RFJScraper/app/RFJScraper/chromedriver.exe", options=options)
            browser.get(f'https://www.instagram.com/{username}/?__a=1')
            user = json.loads(browser.find_element_by_tag_name('pre').text)['graphql']['user']
            browser.quit()
            if user['business_category_name'] is not None :
                uid = username
            else :
                uid = ''
            name = f'{user["full_name"]} (@{username})'
            picture = user['profile_pic_url_hd']
    elif 'twitter.com/' in url :
        twitter_auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        twitter_auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)
        username = re.findall(r'(?<=\.com\/).*$', url)[0]
        api = tweepy.API(twitter_auth)
        user = api.get_user(username)
        uid = username
        name = f'{user.name} (@{username})'
        picture = user.profile_image_url.replace('_normal.', '.')
    else :
        print('url error')
        quit()

    id = repo.add(uid, name, url, is_group)
    response = requests.get(picture)
    file = open(f'C:\Projects\RFJScraper\public\images\profiles\{id}.jpg', "wb")
    file.write(response.content)
    file.close()
    
    print("Success")
    quit()
else:
    print("Already in db")
