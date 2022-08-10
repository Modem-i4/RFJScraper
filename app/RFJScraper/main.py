

import locale

import optparse

import time

from datetime import datetime, timedelta

from datetime import time as dt_time

import os

import dotenv



import facebook

import schedule

import tweepy

import pyfacebook

from selenium.webdriver import Chrome

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait



from Repository import Repository

from scrapers.PostScrapers.ApiScrapers.FacebookApiScraper import api_check as facebook_api_checker

from scrapers.PostScrapers.ApiScrapers.InstagramApiScraper import api_check as instagram_api_checker

from scrapers.PostScrapers.ApiScrapers.TwitterApiScraper import api_check as twitter_api_checker

from scrapers.PostScrapers.BrowserScrapers.FabebookBrowserScraper import browser_check as facebook_browser_checker

from scrapers.PostScrapers.BrowserScrapers.InstagramBrowserScraper import browser_check as instagram_browser_checker

from scrapers.StoriesScrapers.FacebookStoriesScraper import check as facebook_stories_checker

from scrapers.StoriesScrapers.InstagramStoriesScraper import check as instagram_stories_checker



dotenv.load_dotenv()



FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")



USER_DATA_DIR = os.getenv("USER_DATA_DIR")

INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")

INSTAGRAM_BUSINESS_ID = os.getenv("INSTAGRAM_BUSINESS_ID")

INSTAGRAM_APP_ID = os.getenv("INSTAGRAM_APP_ID")

INSTAGRAM_APP_SECRET = os.getenv("INSTAGRAM_APP_SECRET")

TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")

TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")

TWITTER_ACCESS_KEY = os.getenv("TWITTER_ACCESS_KEY")

TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")



DB_NAME = os.getenv("DB_DATABASE")

DB_USER = os.getenv("DB_USERNAME")

DB_PASS = os.getenv("DB_PASSWORD")



locale.setlocale(locale.LC_TIME, "de_DE.utf8")


repo = Repository(DB_NAME, DB_USER, DB_PASS)



options = Options()

#options.add_argument("--user-data-dir=/root/.config/google-chrome-1")
options.add_argument("--user-data-dir=C:\\Users\\vasea\\AppData\\Local\\Google\\Chrome\\User Data")
#options.add_argument(f"--user-data-dir={USER_DATA_DIR}")

options.add_argument("window-size=900,1100") # no start menu cover

options.add_argument("window-position=0,0") #left side

options.add_argument("log-level=3")

options.add_argument("--no-sandbox")

#browser = Chrome('//chromedriver', options=options)
browser = Chrome('chromedriver.exe', options=options)

api = {}



def main() :

    api['facebook'] = facebook.GraphAPI(access_token=FACEBOOK_ACCESS_TOKEN)

    api['instagram'] = pyfacebook.IgProApi(long_term_token=INSTAGRAM_ACCESS_TOKEN, instagram_business_id=INSTAGRAM_BUSINESS_ID, app_secret=INSTAGRAM_APP_SECRET)

    twitter_auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)

    twitter_auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)

    api['twitter'] = tweepy.API(twitter_auth)

    

    check_access_token_refresh_required()

    update_settings()



    facebook_api_checker(api['facebook'], browser, repo)

    instagram_api_checker(api['instagram'], browser, repo)

    twitter_api_checker(api['twitter'], browser, repo)

    

    facebook_browser_checker(browser, repo)

    instagram_browser_checker(browser, repo)

    facebook_stories_checker(browser, repo)

    instagram_stories_checker(browser, repo)

    

    while True: 
        
        try:

            schedule.run_pending()

        except:

            print(f"Pending error - {datetime.now()}")

            raise

        time.sleep(1)



settings = {

        "facebook_api_check_period" : 0,

        "instagram_api_check_period" : 0,

        "twitter_api_check_period" : 0,

        "facebook_browser_check_period" : 0,

        "instagram_browser_check_period" : 0,

        "sleep_over_night" : 0,

        "sleep_from" : 0,

        "sleep_to" : 0,

        "facebook_stories_check_period" : 0,

        "instagram_stories_check_period" : 0,

        }



def update_settings() :

    if check_settings() :

        print(f"Settings have been updated - {datetime.now()}")

        schedule.clear()



        schedule.every(settings["facebook_api_check_period"]).minutes.do(facebook_api_checker, api['facebook'], browser, repo)

        schedule.every(settings["instagram_api_check_period"]).minutes.do(instagram_api_checker, api['instagram'], browser, repo)

        schedule.every(settings["twitter_api_check_period"]).minutes.do(twitter_api_checker, api['twitter'], browser, repo)



        schedule.every(settings["facebook_browser_check_period"]).minutes.do(facebook_browser_checker, browser, repo)

        schedule.every(settings["instagram_browser_check_period"]).minutes.do(instagram_browser_checker, browser, repo)



        schedule.every(settings["facebook_stories_check_period"]).minutes.do(facebook_stories_checker, browser, repo)

        schedule.every(settings["instagram_stories_check_period"]).minutes.do(instagram_stories_checker, browser, repo)



        schedule.every(1).minutes.do(update_settings)

        schedule.every(1).minutes.do(check_sleep_required)

        schedule.every(1).day.do(check_access_token_refresh_required)



def check_sleep_required() :

    if settings["sleep_over_night"] == 1 :

        if is_sleep_required(settings["sleep_from"], settings["sleep_to"]) :

            print(f"Scraper is going to sleep till {settings['sleep_to']}")

            browser.get("file:///" + os.path.abspath("sleeping/index.html").replace('\\','/'))

            while is_sleep_required(settings["sleep_from"], settings["sleep_to"]) :

                time.sleep(60)

                check_settings()

            print("Wake up!")



def is_sleep_required(start, end):

    from_ = dt_time(start)

    to = dt_time(end-1 if end != 0 else 23)

    now = dt_time(datetime.now().hour)

    if from_ <= to:

        return from_ <= now <= to

    else:

        return from_ <= now or now <= to



def check_settings() :

    is_changed = False

    for key in settings.keys() :

        new_setting = repo.get_setting(key)

        if new_setting != settings[key] :

            settings[key] = new_setting

            is_changed = True



    return is_changed



def check_access_token_refresh_required() :

	try:

		expires_at = api['instagram'].get_token_info().expires_at

		expires_at = datetime.fromtimestamp(expires_at)

	except:

		expires_at = datetime.now()

	if (expires_at-datetime.now()).days < 2 :

		browser.get(f'https://www.facebook.com/v9.0/dialog/oauth?response_type=token&display=0&client_id={INSTAGRAM_APP_ID}&redirect_uri=https%3A%2F%2Fdevelopers.facebook.com%2Ftools%2Fexplorer%2Fcallback&auth_type=rerequest&scope=instagram_basic%2Cinstagram_manage_insights%2Cpublic_profile')

		generate_token_btn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[style='width: 50%; margin-left: 4px;']")))

		generate_token_btn.click()

		time.sleep(5)

		token = browser.find_element_by_css_selector('.paneContent input').get_attribute('value')

		api['instagram'] = pyfacebook.IgProApi(short_token=token, instagram_business_id=INSTAGRAM_BUSINESS_ID, app_id=INSTAGRAM_APP_ID, app_secret=INSTAGRAM_APP_SECRET)

        

		dotenv.set_key(dotenv.find_dotenv(), "INSTAGRAM_ACCESS_TOKEN", api['instagram']._access_token)





if __name__ == '__main__':

    main()

