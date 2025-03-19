from datetime import date

from psycopg2.extras import RealDictCursor


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn
  
    def get_content(self):
        with self.conn as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id, name FROM urls ORDER BY id DESC")
                all_urls = [dict(row) for row in cur]
                cur.execute("""
                    SELECT DISTINCT ON (url_id)
                        url_id,
                        created_at AS last_check,
                        status_code
                    FROM url_checks
                    ORDER BY url_id, created_at DESC;
                """)            
                last_checks = [dict(row) for row in cur]
                url_checks = {check['url_id']: check for check in last_checks}
                for url in all_urls:
                    check = url_checks.get(url['id'])
                    url['last_check'] = check.get('last_check') if check else ''
                    url['status_code'] = check.get('status_code') if check else ''  # noqa: E501
                return all_urls                

    def find(self, id):
        with self.conn as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
                row = cur.fetchone()
                return dict(row) if row else None

    def get_by_name(self, url):
        with self.conn as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE name = %s", (url,))
                row = cur.fetchone()
                return dict(row) if row else None

    def save(self, url):
        today = date.today()
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO urls (name, created_at)
                    VALUES (%s, %s) RETURNING id""", (url, today)
                )
                id = cur.fetchone()[0]
            conn.commit()
        return id
        
    def save_check(self, url):
        today = date.today()
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO url_checks (url_id, status_code, h1,
                    title, description, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
                (url['id'], url['status_code'], url['h1'],
                url['title'], url['description'], today)
                )
            conn.commit()        

    def get_all_checks(self, id):
        with self.conn as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""SELECT * FROM url_checks
                            WHERE url_id=%s
                            ORDER BY created_at DESC""", (id,))
                return cur.fetchall()      



