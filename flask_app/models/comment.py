
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user, post
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# The above is used when we do login registration, be sure to install flask-bcrypt: pipenv install flask-bcrypt


class Comment:
    db = "dojo_wall_db" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.post_id = data['post_id']
        self.user_id = data['user_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # What changes need to be made above for this project?
        #What needs to be added her for class association?
        self.creator = None
        self.post_id = None



    # Create Post Models
    @classmethod
    def create_comment(cls, data):
        if not cls.validate_comment(data['content']):
            flash('You must write something in order to comment!')
            return False
        query = """
        INSERT INTO comments (post_id, user_id, content)
        VALUES (%(post_id)s, %(user_id)s, %(content)s)
        ;"""
        comment_id = connectToMySQL(cls.db).query_db(query,data)
        return comment_id


    # Read Post Models
    @classmethod
    def get_post_comments_with_user(cls, post_id):
        data = {'id': post_id}
        query = """
        SELECT * FROM comments
        JOIN users 
        ON comments.user_id = users.id
        WHERE post_id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        all_comments = []
        for db_row in results:
            this_comment = cls(db_row)
            user_info = {
                'id': db_row['users.id'],
                'first_name': db_row['first_name'],
                'last_name': db_row['last_name'],
                "email": db_row['email'],
                "password": db_row['password'],
                'created_at': db_row['users.created_at'],
                'updated_at': db_row['users.updated_at']
            }
            this_comment.creator = user.User(user_info)
            all_comments.append(this_comment)
        all_comments = all_comments[::-1]
        return all_comments
        
    
    # Update Post Models



    # Delete Post Models

    # Validate Post
    @staticmethod
    def validate_comment(content):
        if len(content) < 1:
            return False
        return True