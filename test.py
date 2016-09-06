__author__ = 'seyriz'
from json import loads, dumps

from flask import *

from naver_login import flask_naver

app = Flask(__name__)
app.config['CLIENT_ID'] = "t4zhYRQ2RoZwVXAXzL5V"
app.config['CLIENT_SECRET'] = "iqANBHZRnq"
app.config['CALLBACK'] = '/callback'
app.config['SECRET_KEY'] = 'THIS_IS_NOT_SECRET_KEY'
naver = flask_naver(app)


@app.route('/')
def index():
    if(session.get('isLogged')):
        ent = {'userInfo': loads(session.get('userInfo')), 'hashed': loads(session.get('hashed')),
               'state': session.get('state'), 'auth_token': session.get('auth_token'),
               'refresh_token': session.get('refresh_token'), 'token_type': session.get('token_type')}
        return render_template('userInfo.html', entity = ent)
    else:
        return naver.login()


@app.route('/callback')
def callback():
    if(request.args is not None):
        auth = naver.getAuth(request.args)
        if(type(auth) == dict):
            session['auth_token'] = auth.get('access_token')
            session['refresh_token'] = auth.get('refresh_token')
            session['token_type'] = auth.get('token_type')
            session['userInfo'] = dumps(naver.getUserInfo(session.get('token_type'), session.get('auth_token')))
            session['hashed'] = dumps(naver.getUserUnique(session.get('token_type'), session.get('auth_token')))
            session['isLogged'] = True
            return redirect(url_for('index'))
        else:
            return auth
    else:
        raise ValueError

if(__name__ == '__main__'):
    app.run(host='0.0.0.0', port=5000, debug=True)