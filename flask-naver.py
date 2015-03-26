# -*- coding : utf-8 -*-
from json import *
from uuid import uuid4
# for compatibility to python3
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from flask import session, redirect
from httplib2 import Http
from encoder import XML2Dict

class flask_naver(object):
    def __init__(self, app=None):
        if(app is not None):
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        self.CLIENT_ID = app.config.get('CLIENT_ID')
        self.CLIENT_SECRET = app.config.get('CLIENT_SECRET')
        self.CALLBACK = app.config.get('CALLBACK')
        if(self.CLIENT_ID == None or self.CLIENT_SECRET == None or self.CALLBACK == None):
            raise KeyError

    def login(self):
        """
        Start login sequence.
        MUST redirect to returned URL
        :return: Naver auth URL with query
        """
        session['state'] = state = uuid4().hex
        param = {'state': state, 'redirect_uri': self.CALLBACK, 'response_type': 'code', 'client_id': self.CLIENT_ID}
        urlen = urlencode(param)
        print(urlen)
        uri = "https://nid.naver.com/oauth2.0/authorize?"
        return uri + urlen


    def getAuth(self, args):
        """
        Get access_toke and check CSRF.
        :param args: 'request.args()' only
        :return: Authorization information in Dict.
        """
        state = args.get('state')
        auth = args.get('code')
        error = args.get('error')
        error_description = args.get('error_description')
        if(state == session.get('state') and error == '00'):
            uri = "https://nid.naver.com/oauth2.0/token?"
            params = {'client_id': self.CLIENT_ID, 'client_secret': self.CLIENT_SECRET, 'grant_type': 'authorization_code',
                      'state': state, 'code': auth}
            urlen = urlencode(params)
            http = Http()
            resp, content = http.request(uri + urlen)
            print(resp)
            print(content)
            return loads(content)
        else:
            return error_description is not None if error_description else 'CSRF error'


    def refreshAuth(self, refresh_token = ""):
        """
        Refresh access_token
        :param refresh_token: refresh_token given by getAuth.
        :return: New authorization information in Dict.
        """
        print(session)
        uri = "https://nid.naver.com/oauth2.0/token?"
        params = {'grant_type': 'refresh_token', 'client_id': self.CLIENT_ID, 'client_secret': self.CLIENT_SECRET,
                  'refresh_token': refresh_token}
        http = Http()
        urlen = urlencode(params)
        print(urlen)
        resp, content = http.request(uri + urlen)
        print(resp)
        print(content)
        return loads(content)


    def gerUserInfo(self, token_type="", access_token=''):
        """
        Get user personal information(email, user_unique_key, nickname, etc...)
        :param token_type: token_type given by getAuth or refreshAuth.
        :param access_token: access_token given by getAuth or refreshAuth.
        :return: User's personal information
        """
        http = Http()
        uri = "https://apis.naver.com/nidlogin/nid/getUserProfile.xml"
        header = {'Authorization': token_type + " " + access_token}
        resp, content = http.request(uri=uri, method="POST", headers=header)
        print(resp)
        print(content)
        parser = XML2Dict()
        cont = parser.parse(content)
        print(cont)
        return dumps(cont)


    def getUserUnique(self, token_type="", access_token=''):
        """
        Get user_unique_key only(maybe can get user nickname too?)
        :param token_type: token_type given by getAuth or refreshAuth.
        :param access_token: access_token given by getAuth or refreshAuth.
        :return: user_unique_key and result code in Dict
        """
        http = Http()
        uri = "https://apis.naver.com/nidlogin/nid/getHashId_v2.xml?mode=userinfo"
        header = {'Authorization': token_type + " " + access_token}
        resp, content = http.request(uri=uri, headers=header)
        print(resp)
        print(content)
        parser = XML2Dict()
        cont = parser.parse(content)
        print(cont)
        return dumps(cont)
