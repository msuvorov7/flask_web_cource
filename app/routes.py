from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def hello_world():
    user = {'username': 'msuvorov7'}

    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]

    return render_template('index.html', user=user, posts=posts)
