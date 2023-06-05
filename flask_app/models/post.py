
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user, comment
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# The above is used when we do login registration, be sure to install flask-bcrypt: pipenv install flask-bcrypt


class Post:
    db = "dojo_wall_db" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # What changes need to be made above for this project?
        #What needs to be added her for class association?
        self.creator = None
        self.comments = []



    # Create Post Models
    @classmethod
    def create_post(cls, data):
        if not cls.validate_post(data['content']):
            flash('You must write something in order to post!')
            return False
        query = """
        INSERT INTO posts (user_id, content)
        VALUES (%(user_id)s, %(content)s)
        ;"""
        post_id = connectToMySQL(cls.db).query_db(query,data)
        return post_id


    # Read Post Models
    @classmethod
    def get_all_posts_with_users(cls):
        query = """
        SELECT * FROM posts
        JOIN users 
        ON posts.user_id = users.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_posts = []
        for db_row in results:
            one_post = cls(db_row)
            # Adding creator of the post user
            one_post_user_info = {
                'id': db_row['users.id'],
                'first_name': db_row['first_name'],
                'last_name': db_row['last_name'],
                "email": db_row['email'],
                "password": db_row['password'],
                'created_at': db_row['users.created_at'],
                'updated_at': db_row['users.updated_at']
            }
            one_post.creator = user.User(one_post_user_info)
            #Get the comments info and creator
            one_post.comments = comment.Comment.get_post_comments_with_user(db_row['id'])
            all_posts.append(one_post)
        all_posts = all_posts[::-1]
        return all_posts
    
    @classmethod
    def get_all_posts_with_comments(cls):
        query = """
        SELECT * FROM posts
        JOIN comments
        ON posts.id =
        ;"""
    
    # Update Post Models



    # Delete Post Models
    @classmethod
    def delete_post(cls, post_id):
        data = {'id': post_id}
        query = """
        DELETE FROM posts
        WHERE id = %(id)s
        ;"""

        return connectToMySQL(cls.db).query_db(query, data)
    
    # Validate Post
    @staticmethod
    def validate_post(content):
        if len(content) < 1:
            return False
        return True