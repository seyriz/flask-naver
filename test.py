__author__ = 'seyriz'
from json import loads, dumps

from flask import *

from naver_login import flask_naver

app = Flask(__name__)
app.config['CLIENT_ID'] = ""
app.config['CLIENT_SECRET'] = ""
app.config['CALLBACK'] = "callback"


@app.route('/index')
def index():
    if(session.get('isLogged')):
        ent = {'userInfo': loads(session.get('userInfo')), 'hashed': loads(session.get('hashed')),
               'state': session.get('state'), 'auth_token': session.get('auth_token'),
               'refresh_token': session.get('refresh_token'), 'token_type': session.get('token_type')}
        return render_template('userInfo.html', entity = ent)
    else:
        flask_naver.login()


@app.config('/callback')
def callback():
    if(request.args is not None):
        auth = flask_naver.getAuth(request.args)
        if(type(auth) == dict):
            session['auth_token'] = auth.get('access_token')
            session['refresh_token'] = auth.get('refresh_token')
            session['token_type'] = auth.get('token_type')
            session['userInfo'] = flask_naver.getUserInfo(session.get('token_type'), session.get('auth_token'))
            session['hashed'] = flask_naver.getUserUnique(session.get('token_type'), session.get('auth_token'))
            return redirect(url_for('index'))
        else:
            return auth
    else:
        raise ValueError

if(__name__ == '__main__'):
    app.run(host='0.0.0.0', port=5000, debug=True)