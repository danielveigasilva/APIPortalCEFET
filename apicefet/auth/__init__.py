from itsdangerous import TimedJSONWebSignatureSerializer
from bs4 import BeautifulSoup as bs
from apicefet.helpers import URLS
from requests import Session
from flask import jsonify


def auth(user, passwd):
    session = Session()
    session.headers.update({'referer': URLS['matricula']})
    session.get(URLS['aluno_login_action_error'])

    auth_info = {"j_username": user, "j_password": passwd}

    site_post = session.post(URLS['security_check'], data=auth_info)
    site_post_bs = bs(site_post.content, "html.parser")

    matricula = site_post_bs.find("input", id="matricula")["value"]
    cookie = session.cookies.get_dict()

    jwt = TimedJSONWebSignatureSerializer('%key%', expires_in=10 * 60)
    token = jwt.dumps({
        "matricula": matricula,
        "cookie": cookie['JSESSIONID']
    }).decode("utf-8")

    return jsonify({
        "code": 200,
        "data": {
            "token": token
        }
    })
