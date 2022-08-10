import pymysql
from dotenv import load_dotenv
import os

class ProfileRepository:
    def __init__(self) :
        load_dotenv()
        self.db_user = os.getenv("DB_USERNAME")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_DATABASE")

    def _getConn(self) :
        return pymysql.connect(host='localhost', user=self.db_user, password=self.db_password, db=self.db_name)
        #return pymysql.connect(host='localhost', user='root', password='root', db='scraper')

    def check_if_in_db(self, url) :
        conn = self._getConn()
        sql = conn.cursor()
        sql.execute(f"SELECT COUNT(id) FROM profiles WHERE url='{url}' AND removed=0")
        entries = sql.fetchone()[0]
        sql.close()
        conn.close()
        return entries>0

    def add(self, uid, name, url, is_group = False) :
        conn = self._getConn()
        sql = conn.cursor()
        sql.execute(f"INSERT INTO profiles (uid, name, url, is_group) VALUES ('{uid}', '{name}', '{url}', '{is_group}')")
        id = sql.lastrowid
        conn.commit()
        sql.close()
        conn.close()
        return id
