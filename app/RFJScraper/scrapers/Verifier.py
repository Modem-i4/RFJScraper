
from datetime import datetime
from Notifications.Notifications import notify_by_email
from Repository import Repository
import json
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome


def check_for_edit(repo:Repository, post, browser : Chrome, main_el_selector = None, is_browser_based = False, check_images=False) :
    original_post = repo.try_to_get_post_by_uid(post['uid'])
    if original_post is not None :
        if (remove_tags(original_post['text']) == remove_tags(post['text'])):
             if(not check_images or get_img_root(original_post['images']) == get_img_root(post['images']) ) :
                return False
    img_path = f"..//..//public//images//screenshots//{post['uid']}.png"
    if not is_browser_based :
        try:
            browser.get(post['url'])
            time.sleep(1)
            main_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, main_el_selector)))
            main_element.screenshot(img_path)
        except: 
            try:
                main_element = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-pagelet=page]')))
                main_element.screenshot(img_path)
            except:
                try:
                    browser.save_screenshot(img_path)
                    print(f"Suspicious for page freezing")
                    #test if frozen
                except:
                    print(f"Post HTML was not saved!")
                    raise
                    return False

    if original_post is None :
        #add a new post
        post['status'] = 'usual'
    else :
        #post was edited
        post['status'] = 'edited_to'
        post['published_at'] = datetime.now()
        repo.set_post_status(id=original_post['id'], status='edited')
        notify_by_email(repo, 'edited', original_post['id'], post)
    return True

def get_img_root(arr) :
    if isinstance(arr, str) :
        arr = json.loads(arr)
    try:
        return [re.findall(r'\d+_\d+_\d+', img)[0] for img in arr]
    except:
        return []

def remove_tags(text) :
    return re.sub('<[^>]*>', '', text)

def check_for_delete(repo: Repository, profile, posts, new_posts_amount, deep_check=False, browser:Chrome = None) :
    last_post_uids = [post['id'] for post in posts]
    amount = len(last_post_uids) - new_posts_amount
    if amount <= 0 :
        return
    amount = min(amount, 10)
    last_db_posts = repo.get_last_posts(profile['id'], max(amount,0))
    for last_db_post in last_db_posts :
        if not last_db_post['uid'] in last_post_uids :
            if deep_check :
                browser.get(f"https://facebook.com/{last_db_post['uid']}")
                try:
                    WebDriverWait(browser, 7).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[role=main]>div>div>div>img")))
                except:
                    continue
            new_status = 'deleted_after_edit' if last_db_post['status'] == 'edited_to' else 'deleted'
            repo.set_post_status(last_db_post['id'], new_status)
            print(f"pizdas {last_db_post['uid']}")
            notify_by_email(repo, 'deleted', last_db_post['id'])