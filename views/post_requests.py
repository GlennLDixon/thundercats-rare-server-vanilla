from datetime import datetime
import sqlite3
import json
from models import Post
        
def get_all_posts():
  
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM Posts p
        """)

        posts = []
        dataset = db_cursor.fetchall()

        for row in dataset:

            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                        row['publication_date'], row['image_url'], row['content'],
                        row['approved'])

            posts.append(post.__dict__)

    return json.dumps(posts)

def get_single_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM Posts p
        """, ( id, ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'],
                    data['publication_date'], data['title'], data['image_url'],
                    data['content'], data['approved'])

        return json.dumps(post.__dict__)
    
def create_post(new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, category_id, publication_date, title, image_url, content, approved  )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ? );
        """, (new_post['user_id'], new_post['category_id'], datetime.now(),
              new_post['title'], new_post['image_url'], new_post['content'],
              new_post['approved']))

        id = db_cursor.lastrowid

        new_post['id'] = id

    return json.dumps(new_post)

def delete_post(id):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id, ))
        
def update_post(id, new_post):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Posts
            SET
                user_id = ?,
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?
        WHERE id = ?
        """, (new_post['user_id'], new_post['category_id'],
              new_post['title'], datetime.now(),
              new_post['image_url'], new_post['content'], id ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True