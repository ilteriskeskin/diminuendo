import time

from flask import Flask, render_template, session, request, redirect
from heybooster.helpers.database.mongodb import MongoDBHelper
from configs import URI, NAME, SECRET_KEY
from utils.generator_and_saver import generate_short_url, save_url
from utils.json_encoder import JsonEncoder

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.json_encoder = JsonEncoder


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        long_url = request.form['long_url']
        unix_timestamp = time.time()

        with MongoDBHelper(uri=URI, database=NAME) as db:
            if session.get('logged_in'):
                # user process
                _id = db.insert_one('url', data={'email': session['email'],
                                                 'long_url': long_url,
                                                 'click_counter': 0,
                                                 'referrer_url': [],
                                                 'ts': unix_timestamp}).inserted_id

                short_url = generate_short_url(int(unix_timestamp))
                save_url(long_url=long_url, short_url=short_url, _id=_id, db=db)

                return render_template('home.html', short_url=short_url)
            else:
                # anonymous process
                _id = db.insert_one('url', data={'long_url': long_url, 'ts': unix_timestamp}).inserted_id

                short_url = generate_short_url(int(unix_timestamp))
                save_url(long_url=long_url, short_url=short_url, _id=_id, db=db)

                return render_template('home.html', short_url=short_url)

    return render_template('home.html')


@app.route('/about')
def about():
    return 'about'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        with MongoDBHelper(uri=URI, database=NAME) as db:
            user = db.find_one('user', query={'email': email, 'password': password})

        if user:
            session['email'] = email
            session['logged_in'] = True

            return redirect('/')

    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        data = {
            'email': email,
            'password': password
        }

        with MongoDBHelper(uri=URI, database=NAME) as db:
            db.insert_one('user', data=data)

        return redirect('login')

    return render_template('auth/register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('login')


@app.route('/<short_url>/', methods=['GET'])
def short_url(short_url):
    with MongoDBHelper(uri=URI, database=NAME) as db:
        long_url = db.find_one('url', query={'short_url': short_url})
        click_counter = long_url.get('click_counter')

        if long_url.get('email'):
            referrers = long_url.get('referrer_url')
            referrer = request.headers.get("Referer")
            referrers.append(referrer)
            click_counter += 1
            db.find_and_modify('url', query={'_id': long_url['_id']},
                               click_counter=click_counter,
                               referrer_url=referrers)

    # return redirect(long_url['long_url'])
    return render_template('home.html', long_url=long_url)


if __name__ == '__main__':
    app.run(debug=True)