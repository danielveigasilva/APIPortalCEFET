from apicefet.helpers import URLS, normalizacao, Autenticado
from itsdangerous import TimedJSONWebSignatureSerializer
from flask import jsonify, request, send_file, abort
from bs4 import BeautifulSoup as bs
from requests import Session
import io


def reports_list():
    session = Session()

    if 'X-Token' not in request.headers:
        abort(400, description='Insira um token')

    jwt = TimedJSONWebSignatureSerializer('%key%', expires_in=10 * 60)
    try:
        token_data = jwt.loads(request.headers['X-Token'])
    except:
        abort(400, description='Insira um token valido')
        return

    cookie = token_data('cookie')
    matricula = token_data('matricula')

    if not Autenticado(cookie):
        abort(403, description='Nao autorizado')

    session.cookies.set("JSESSIONID", cookie)
    reports_dirty = session.get(URLS['relatorio_action_matricula'] + matricula)
    reports_bs = bs(reports_dirty.content, "html.parser")

    reports_clean = reports_bs.find_all('a', {'title': 'Relatório em formato PDF'})

    reports = []
    for item in reports_clean:
        reports.append({
            'id': reports_clean.index(item),
            'nome': normalizacao(item.previousSibling),
            'link': item['href'].replace("/aluno/aluno/relatorio/", '')
        })

    return jsonify({
        "codigo": 200,
        "data": reports
    })


def reports_generate(url):
    session = Session()

    if 'X-Token' not in request.headers:
        abort(400, description='Insira um token')

    jwt = TimedJSONWebSignatureSerializer('%key%', expires_in=10 * 60)
    try:
        token_data = jwt.loads(request.headers['X-Token'])
    except:
        abort(400, description='Insira um token valido')
        return

    cookie = token_data('cookie')

    if not Autenticado(cookie):
        abort(403, description='Nao autorizado')

    session.cookies.set("JSESSIONID", cookie)

    pdf_data = session.get(URLS['aluno_relatorio'] + url).content
    pdf = io.BytesIO()
    pdf.write(pdf_data)
    pdf.seek(0)

    return send_file(
        pdf,
        as_attachment=True,
        attachment_filename='relatorio.pdf',
        mimetype='application/pdf'
    )
