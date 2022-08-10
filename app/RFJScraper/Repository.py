from re import T
import pymysql
from datetime import datetime, timedelta
from pprint import pprint as pp
import json

class Repository:
    def __init__(self, db_name, user, password) :
        self._db_name = db_name
        self._user = user
        self._password = password

    def _getConn(self) :
        return pymysql.connect(host='localhost', user=self._user, password=self._password, db=self._db_name)

    def add_many_posts(self, new_posts) :
        conn = self._getConn()
        sql = conn.cursor()
        new_posts_formatted = [(post['poster_id'], post['text'], json.dumps(post['images']), post['published_at'], post['url'], post['uid'], post['status'])
         for post in new_posts]
        #add entries
        query = "INSERT INTO posts (poster_id, text, images, published_at, url, uid, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        sql.executemany(query, new_posts_formatted)
        conn.commit()
        sql.close()
        conn.close()

    def fetchall(self, query):
        conn = self._getConn()
        sql = conn.cursor()
        sql.execute(query)
        result = sql.fetchall()
        sql.close()
        conn.close()
        return result

    def get_profiles(self, site, with_uid = False, any = False, get_url_with_uid = False) :
        if with_uid :
            raw_profiles = self.fetchall(f"SELECT id, uid FROM profiles WHERE watched=1 AND url LIKE '%{site}%' AND uid != ''")
            profiles = [{'id': raw_profile[0], 'uid': raw_profile[1]} for raw_profile in raw_profiles]
        else :
            if any :
                raw_profiles = self.fetchall(f"SELECT id, url FROM profiles WHERE watched=1 AND url LIKE '%{site}%'")
            elif get_url_with_uid :
                raw_profiles = self.fetchall(f"SELECT id, url FROM profiles WHERE watched=1 AND url LIKE '%{site}%' AND uid!=''")
            else :
                raw_profiles = self.fetchall(f"SELECT id, url FROM profiles WHERE watched=1 AND url LIKE '%{site}%' AND uid = ''")
            profiles = [{'id': raw_profile[0], 'url': raw_profile[1]} for raw_profile in raw_profiles]
        return profiles

    def try_to_get_post_by_uid(self, uid, extra_info=True):
        conn = self._getConn()
        sql = conn.cursor()
        sql.execute(f"SELECT id{', text, images' if extra_info else ''} FROM posts WHERE uid='{uid}' ORDER BY id DESC LIMIT 1")
        result = sql.fetchone()
        sql.close()
        conn.close()
        if result == None :
            return None
        if extra_info :
            return {'id': result[0], 'text': result[1], 'images': result[2]}
        else :
            return {'id': result[0]}

    def check_if_link_in_db(self, link) :
        conn = self._getConn()
        sql = conn.cursor()
        sql.execute(f"SELECT COUNT(1) FROM posts WHERE url='{link}'")
        entries = sql.fetchone()[0]
        sql.close()
        conn.close()
        return entries>0

    def get_post_by_id(self, id) :
        conn = self._getConn()
        sql = conn.cursor()
        sql.execute(f"SELECT poster_id, text, images, url FROM posts WHERE id = {id}")
        result = sql.fetchone()
        sql.close()
        conn.close()
        return {'poster_id': result[0], 'text': result[1], 'images': result[2], 'url': result[3]}

    def set_post_status(self, id, status) :
        conn = self._getConn()
        sql = conn.cursor()
        sql.execute(f"UPDATE posts SET status = '{status}' WHERE id = {id}")
        conn.commit()
        sql.close()
        conn.close()



    def get_last_posts(self, poster_id, amount = 5) :
        posts = self.fetchall(f"SELECT id, uid, status FROM posts WHERE poster_id = {poster_id} AND (status = 'edited_to' OR status='usual') ORDER BY published_at DESC LIMIT {amount}")
        return [{'id': post[0], 'uid': post[1], 'status': post[2]} for post in posts]

    def update_posts_status(self, changes) :
        conn = self._getConn()
        sql = conn.cursor()
        query = "UPDATE posts SET status = '%s' WHERE id = %s"
        for change in changes:
            sql.execute(query % (change[1], change[0]))
        conn.commit()
        sql.close()
        conn.close()

    def get_poster_by_id(self, id) :
        conn = self._getConn()
        sql = conn.cursor()
        sql.execute(f"SELECT name, url FROM profiles WHERE id='{id}'")
        result = sql.fetchone()
        sql.close()
        conn.close()
        return {'name': result[0], 'url': result[1]}


    def get_warns_receivers(self) :
        answer = self.fetchall("SELECT email FROM users WHERE warns_receiver = 1")
        result = [a[0] for a in answer] #values from the only column of tuple
        return result

    def get_notifications_receivers(self, poster_id) :
        answer = self.fetchall(f"SELECT email FROM users LEFT JOIN notifications ON users.id = notifications.user_id WHERE notifications.profile_id = {poster_id}")
        result = [a[0] for a in answer] #values from the only column of tuple
        return result

    def get_setting(self, name) :
        conn = self._getConn()
        sql = conn.cursor()
        sql.execute(f"SELECT value FROM settings WHERE alias = '{name}'")
        setting = sql.fetchone()[0]
        sql.close()
        conn.close()
        return setting