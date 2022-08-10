from Repository import Repository
from Notifications.Email import send_email
import json
from datetime import datetime
import dotenv
import os

dotenv.load_dotenv()
APP_URL = os.getenv("APP_URL")
def notify_by_email(repo : Repository, type, post_id, change_to=None) :
    original_post = repo.get_post_by_id(post_id)
    receivers = repo.get_notifications_receivers(original_post['poster_id'])

    profile = repo.get_poster_by_id(original_post['poster_id'])
    site = 'facebook' if 'facebook.com/' in profile['url'] else 'instagram' if 'instagram.com/' in profile['url'] else 'twitter' if 'twitter.com/' in profile['url'] else ''

    now = datetime.now().strftime('%d %b %H:%M')
    scraper_link=f"{APP_URL}/posts/{site}/{post_id}"

    original_img_block = ''
    new_img_block = ''

    print(f"Found a {type} post on {site}!")

    if site == 'facebook' :
        original_img_block = get_images(json.loads(original_post['images']))
        if change_to is not None :
            new_img_block = get_images(change_to['images'])


    if type == 'deleted' :
        subj = f"{site}: {profile['name']} deleted a post"
        html = f"""<a href="{site}.com">{site}</a>: <a href="{profile['url']}">{profile['name']}</a> deleted a <a href="{original_post['url']}">post</a> - {now}<br>
        <br>
        Post text: <br>
        "<br>
        {original_post['text']}<br>
        "<br>
        {original_img_block}
        You can try to restore it: <a href="{scraper_link}">{scraper_link}</a>
        """
    else : #if type == 'edited' :
        subj = f"{site}: {profile['name']} edited a post"
        html = f"""<a href="{site}.com">{site}</a>: <a href="{profile['url']}">{profile['name']}</a> edited a <a href="{original_post['url']}">post</a> - {now}<br>
        <br>
        From: <br>
        "<br>
        {original_post['text']}<br>
        "<br>
        {original_img_block}<br>
        To:<br>
        "<br>
        {change_to['text']}<br>
        "<br>
        {new_img_block}<br>
        You can try to restore it: <a href="{scraper_link}">{scraper_link}</a>
        """
    send_email(receivers, subj, html)

def get_images(images) :
    if len(images) == 0 :
        return []
    html = 'Images : <br>'
    for image in images :
        html += f'<a href={image}><img src="{image}" style="width:30%; margin-left: 2%"></a>'
    return html
