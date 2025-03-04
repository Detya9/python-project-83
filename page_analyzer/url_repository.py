from datetime import date, datetime

import psycopg2
from psycopg2.extras import RealDictCursor


class UrlRepository:
    def __init__(self, db_url):
        try:
            self.conn = psycopg2.connect(db_url)
        except:  # noqa: E722
            print('Can`t establish connection to database')

    def get_content(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM urls ORDER BY id DESC")
            return [dict(row) for row in cur]
    
    def find(self, id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def get_by_url(self, url):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE name = %s", (url,))
            row = cur.fetchone()
            return dict(row) if row else None

    def save(self, url):
        now = datetime.now()
        today = date(now.year, now.month, now.day)
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO urls (url, created_at) VALUES (%s, %s) RETURNING id",  # noqa: E501
                (url['url'], today)
            )
            id = cur.fetchone()[0]
            url['id'] = id
        self.conn.commit()
    
    def save_check(self, url):
        now = datetime.now()
        today = date(now.year, now.month, now.day)
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO url_checks (url_id, created_at) VALUES (%s, %s) RETURNING id",  # noqa: E501
                (url['id'], today)
            )
        self.conn.commit()        

    def get_all_checks(self, id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""SELECT * FROM url_checks
                         WHERE url_id=%s
                         ORDER BY created_at DESC""", (id,))
            return [dict(row) for row in cur]       



