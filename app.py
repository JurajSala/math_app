from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Simulovaná databáze (seznam příspěvků)
posts = []

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['POST'])
def add_post():
    title = request.form.get('title')
    content = request.form.get('content')
    if title and content:
        posts.append({'title': title, 'content': content})
    return redirect(url_for('index'))

@app.route('/external')
def external_data():
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    data = response.json()
    return render_template('external.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)