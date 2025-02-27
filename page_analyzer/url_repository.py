from datetime import datetime

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
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO urls (url, created_at) VALUES (%s, %s) RETURNING id",  # noqa: E501
                (url['url'], now)
            )
            id = cur.fetchone()[0]
            url['id'] = id
        self.conn.commit()

