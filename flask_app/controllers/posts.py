from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, post # import entire file, rather than class, to avoid circular imports

# Create Users Controller
@app.route('/post/new_post', methods=['POST'])
def create_post():
    data = {
        "content": request.form['content'],
        "user_id": session['user_id']
    }
    post.Post.create_post(data)
    return redirect('/user/wall')

# Read Users Controller


# Update Users Controller



# Delete Users Controller
@app.route('/post/delete/<int:post_id>')
def delete_post(post_id):
    post.Post.delete_post(post_id)
    return redirect('/user/wall')

# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions 
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')
# def index(id):
#     user_info = user.User.get_user_by_id(id)
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.