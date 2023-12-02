from flask import Flask, render_template

app = Flask(__name__)

@app.route('/about')
def about_page():
    return '<h1>About Page</h1>'

#kişiye özel sayfa http uzantısıyla görüntülemke için
@app.route('/about/<username>')
def about_person_page(username):
    return f'<h1>This is the about the page of {username}</h1>'

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')