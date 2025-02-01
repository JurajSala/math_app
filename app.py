from flask import Flask, render_template, request, redirect, url_for
import requests

from data_handler import load_posts, add_post

app = Flask(__name__)


@app.route('/')
def index():
    posts = load_posts()
    posts.reverse()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['POST'])
def addPost():
    title = request.form.get('title')
    content = request.form.get('content')
    if title and content:
        add_post(title, content)
    return redirect(url_for('index'))

@app.route('/external')
def external_data():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    data = response.json()
    return render_template('external.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)