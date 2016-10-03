# Flask-Naver

네이버 아이디로 로그인을 위한 플라스크 확장기능입니다.

# Installation

    pip install flask-naver

# Usage

먼저 앱의 설정에 다음과 같은 값이 들어있어야 합니다.

    app.config['NAVER_CLIENT_ID'] = ""
    app.config['NAVER_CLIENT_SECRET'] = ""
    app.config['NAVER_CALLBACK'] = ''
    
CLIENT_ID와 CLIENT_SECRET은 [네이버 개발자센터](https://developers.naver.com/main)에서 발급받아서 입력합니다.

또한 앱의 url을 미리 네이버 개발자센터에 입력해야 합니다.

CALLBACK은 네아로를 이용했을 때 로그인 정보를 처리할 컨트롤러의 url을 입력합니다. 이때 프로토콜과 도메인을 제외한 url만 입력하면 됩니다. 


    from flask import Flask
    from naver_login import flask_naver
    
    app = Flask(__name__)
    naver = flask_naver(app)
    
    ... 
    
    @app.route('/login/naver')
    def login():
        ...
        if not logged_in:
            naver.login()
            
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
