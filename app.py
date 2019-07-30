import os
from flask import Flask, render_template, request
from RssCollector import RssCollector
from sql import sql
import webbrowser

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/collect')
def collect():
    RssCollector()
    return render_template('index.html')


@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'GET':
        return render_template('query.html')
    elif request.method == 'POST':
        position = request.form.get('position')
        type = request.form.get('type')
        date = request.form.get('date')
        keyword = request.form.get('keyword')
        result = sql(position, type, date, keyword)
        return render_template('query.html', result=result)


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000/', 0, False)
    app.run()
