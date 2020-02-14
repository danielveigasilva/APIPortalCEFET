from apicefet.helpers import URLS, normalizacao, Autenticado
from itsdangerous import TimedJSONWebSignatureSerializer
from flask import jsonify, request, send_file
from bs4 import BeautifulSoup as bs
from requests import Session
import re
import io


def get_profile_property(conteudoHTML, propriedade):
    try:
        site_profile_bs = bs(conteudoHTML, "html.parser")
        bloco = site_profile_bs.find('span', text=re.compile(propriedade)).find_parent('td')

        objetoIgnorado = bloco.find('span')
        objetoIgnorado.extract()

        return normalizacao(bloco.get_text())

    except Exception as e:
        print('Exception:' + str(e))
        return None


def profile_data():  # @TODO: finalizar coleta de dados
    session = Session()

    if 'X-Token' not in request.headers:
        return jsonify({
            "code": 400,
            "error": "Insira um token"
        })

    jwt = TimedJSONWebSignatureSerializer('%key%', expires_in=10 * 60)
    try:
        token_data = jwt.loads(request.headers['X-Token'])
    except:
        return jsonify({
            "code": 400,
            "error": "Insira um token valido"
        })

    cookie = token_data('cookie')
    matricula = token_data('matricula')

    if not Autenticado(cookie):
        return jsonify({
            "code": 401,
            "error": "Nao autorizado"
        })

    session.cookies.set("JSESSIONID", cookie)
    siteHorarios = session.get(URLS['menu_action_matricula'] + matricula)
    sitePerfil = session.get(URLS['perfil_perfil_action'])

    return jsonify(
        {
            "codigo": 200,
            "data": {
                "Matricula": get_profile_property(siteHorarios.content, '.Matrícula:'),
                "Curso": get_profile_property(siteHorarios.content, '.Curso:'),
                "Periodo Atual": get_profile_property(siteHorarios.content, '.Período Atual:'),
                "Nome": get_profile_property(sitePerfil.content, '.Nome')
            }
        }
    )


def profile_data_all():  # TODO: finalizar coleta de dados
    session = Session()

    if 'X-Token' not in request.headers:
        return jsonify({
            "code": 400,
            "error": "Insira um token"
        })

    jwt = TimedJSONWebSignatureSerializer('%key%', expires_in=10 * 60)
    try:
        token_data = jwt.loads(request.headers['X-Token'])
    except:
        return jsonify({
            "code": 400,
            "error": "Insira um token valido"
        })

    cookie = token_data('cookie')
    matricula = token_data('matricula')

    if not Autenticado(cookie):
        return jsonify({
            "code": 401,
            "error": "Nao autorizado"
        })

    session.cookies.set("JSESSIONID", cookie)
    siteHorarios = session.get(URLS['menu_action_matricula'] + matricula)
    sitePerfil = session.get(URLS['perfil_perfil_action'])

    return jsonify({
        "codigo": 200,
        "data": {
            "academico": {
                "Matricula": get_profile_property(siteHorarios.content, '.Matrícula:'),
                "Curso": get_profile_property(siteHorarios.content, '.Curso:'),
                "Periodo Atual": get_profile_property(siteHorarios.content, '.Período Atual:')
            },
            "informacoes": {
                "Nome": get_profile_property(sitePerfil.content, '.Nome'),
                "Nome da Mae": get_profile_property(sitePerfil.content, '.Nome da Mãe'),
                "Nome do Pai": get_profile_property(sitePerfil.content, '.Nome da Pai'),
                "Nascimento": get_profile_property(sitePerfil.content, '.Nascimento'),
                "Sexo": get_profile_property(sitePerfil.content, '.Sexo'),
                "Etnia": get_profile_property(sitePerfil.content, '.Etnia'),
                "Deficiencia": get_profile_property(sitePerfil.content, '.Deficiência'),
                "Tipo Sanguineo": get_profile_property(sitePerfil.content, '.Tipo Sanguíneo'),
                "Fator RH": get_profile_property(sitePerfil.content, '.Fator RH'),
                "Estado Civil": get_profile_property(sitePerfil.content, '.Estado Civil'),
                "Pagina Pessoal": get_profile_property(sitePerfil.content, '.Página Pessoal'),
                "Nacionalidade": get_profile_property(sitePerfil.content, '.Nacionalidade'),
                "Estado": get_profile_property(sitePerfil.content, '.Estado'),
                # TODO: consertar bug, Estado obtem Estado Civil
                "Naturalidade": get_profile_property(sitePerfil.content, '.Naturalidade')
            },
            "endereco": {
                "Tipo de endereco": get_profile_property(sitePerfil.content, '.Tipo de endereço'),
                "Tipo de logradouro": get_profile_property(sitePerfil.content, '.Tipo de logradouro'),
                "Logradouro": get_profile_property(sitePerfil.content, '.Logradouro'),
                "Numero": get_profile_property(sitePerfil.content, '.Número'),
                # TODO: consertar bug, Numero não é encontrado
                "Complemento": get_profile_property(sitePerfil.content, '.Complemento'),
                "Bairro": get_profile_property(sitePerfil.content, '.Bairro'),
                "Pais": get_profile_property(sitePerfil.content, '.País'),
                "Estado": get_profile_property(sitePerfil.content, '.Estado'),
                # TODO: consertar bug, Estado obtem Estado Civil
                "Cidade": get_profile_property(sitePerfil.content, '.Cidade'),
                "Distrito": get_profile_property(sitePerfil.content, '.Distrito'),
                "CEP": get_profile_property(sitePerfil.content, '.CEP'),
                "Caixa Postal": get_profile_property(sitePerfil.content, '.Caixa Postal'),
                "E-mail": get_profile_property(sitePerfil.content, '.E-mail'),
                "Tel. Residencial": get_profile_property(sitePerfil.content, '.Tel. Residencial'),
                "Tel. Celular": get_profile_property(sitePerfil.content, '.Tel. Celular'),
                "Tel. Comercial": get_profile_property(sitePerfil.content, '.Tel. Comercial'),
                "Fax": get_profile_property(sitePerfil.content, '.Fax')
            }
        }
    })


def profile_photo():
    session = Session()

    if 'X-Token' not in request.headers:
        return jsonify({
            "code": 400,
            "error": "Insira um token"
        })

    jwt = TimedJSONWebSignatureSerializer('%key%', expires_in=10 * 60)
    try:
        token_data = jwt.loads(request.headers['X-Token'])
    except:
        return jsonify({
            "code": 400,
            "error": "Insira um token valido"
        })

    cookie = token_data('cookie')

    if not Autenticado(cookie):
        return jsonify({
            "code": 401,
            "error": "Nao autorizado"
        })

    session.cookies.set("JSESSIONID", cookie)

    img_data = session.get(URLS['foto_action']).content
    img = io.BytesIO()
    img.write(img_data)
    img.seek(0)

    return send_file(
        img,
        as_attachment=True,
        attachment_filename='imagemPerfil.jpeg',
        mimetype='image/jpeg'
    )
