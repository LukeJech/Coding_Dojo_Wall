from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, post, comment # import entire file, rather than class, to avoid circular imports

# Create Users Controller
@app.route('/user/register', methods=['POST', 'GET'])
def user_register():
    #get the register page
    if request.method == 'GET':
        return render_template('register.html', reg_form_input = session.get('user_registration_input', ''))
    #validate user registration
    if user.User.validate_user_registration(request.form):
        #if valid create user in our database
        user.User.create_user(request.form)
        #log in user to their posting page
        return redirect('/user/wall')
    #redirect if invalid with session info of their previous form except their password input
    session['user_registration_input'] = {
    'first_name': request.form['first_name'],
    'last_name': request.form['last_name'],
    'email': request.form['email'],
    }
    return redirect('/user/register')


# Read Users Controller
@app.route('/')
def direct_to_register():
    return redirect('/user/register')

@app.route('/user/wall')
def user_create_post():
    if 'user_id' in session:
        all_posts = post.Post.get_all_posts_with_users()
        return render_template('/wall.html', all_posts = all_posts)
    return redirect('/user/login')

@app.route('/user/login', methods=['POST', 'GET'])
def login_user():
    #GET login page
    if request.method == 'GET':
        return render_template('login.html')
    #check if login matches email and hashed password
    if user.User.validate_login(request.form):
        #if valid login redirect to wall page
        return redirect('/user/wall')
    #if invalid redirect to user login page again with their submitted email saved in session
    return redirect('/user/login')

@app.route('/user/logout')
def logout_user():
    session.clear()
    return redirect('/user/login')

# Update Users Controller



# Delete Users Controller


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