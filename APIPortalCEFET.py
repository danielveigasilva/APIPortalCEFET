from flask import Flask, jsonify, request, send_file
import unicodedata
import os
import io

from requests import Session
from bs4 import BeautifulSoup as bs
import re

app = Flask(__name__)


URLS = {
    'matricula': 'https://alunos.cefet-rj.br/matricula/',
    'index_action': 'https://alunos.cefet-rj.br/aluno/index.action',
    'foto_action': 'https://alunos.cefet-rj.br/aluno/aluno/foto.action',
    'menu_action_matricula': 'https://alunos.cefet-rj.br/aluno/aluno/quadrohorario/menu.action?matricula=',
    'perfil_perfil_action': 'https://alunos.cefet-rj.br/aluno/aluno/perfil/perfil.action',
    'aluno_relatorio': 'https://alunos.cefet-rj.br/aluno/aluno/relatorio/',
    'relatorio_action_matricula': 'https://alunos.cefet-rj.br/aluno/aluno/relatorio/relatorios.action?matricula=',
    'aluno_login_action_error': 'https://alunos.cefet-rj.br/aluno/login.action?error=',
    'security_check': 'https://alunos.cefet-rj.br/aluno/j_security_check'
}


def normalizacao(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').replace('  ','').replace('\n','').replace('\r','')


def pegaPropriedadePerfil(conteudoHTML, propriedade):
    
    try:
        sitePerfilBS = bs(conteudoHTML, "html.parser")
        bloco = sitePerfilBS.find('span', text = re.compile(propriedade)).find_parent('td')

        objetoIgnorado = bloco.find('span')
        objetoIgnorado.extract()

        return normalizacao(bloco.get_text())

    except Exception as e:
        print('Exception:' + e)
        return None

    
def Autenticado(cookie):
    
    sessao = Session()
    sessao.cookies.set("JSESSIONID", cookie)
    sessao.headers.update({'referer': URLS['matricula']})

    acesso = sessao.get(URLS['index_action'], allow_redirects=False)

    if (acesso.status_code == 302):
        return False
    else:
        return True


@app.route('/perfil', methods=['GET'])
def perfilDados():  # @TODO: finalizar coleta de dados

    sessao = Session()

    cookie = request.args.get('cookie')
    matricula = request.args.get('matricula')

    if not Autenticado(cookie):
        return jsonify({
            "code": 401,
            "error": "Nao autorizado"
        })

    sessao.cookies.set("JSESSIONID", cookie)
    siteHorarios = sessao.get(URLS['menu_action_matricula'] + matricula)
    sitePerfil = sessao.get(URLS['perfil_perfil_action'])

    return jsonify(
        {
            "codigo": 200,
            "data": {
                "Matricula": pegaPropriedadePerfil(siteHorarios.content, '.Matrícula:'),
                "Curso": pegaPropriedadePerfil(siteHorarios.content, '.Curso:'),
                "Periodo Atual": pegaPropriedadePerfil(siteHorarios.content, '.Período Atual:'),
                "Nome": pegaPropriedadePerfil(sitePerfil.content, '.Nome')
            }
        }
    )


@app.route('/perfil/geral', methods=['GET'])
def perfilDadosGerais():  # TODO: finalizar coleta de dados

    sessao = Session()

    cookie = request.args.get('cookie')
    matricula = request.args.get('matricula')
    sessao.cookies.set("JSESSIONID", cookie)

    if not Autenticado(cookie):
        return jsonify({
            "code": 401,
            "error": "Nao autorizado"
        })

    siteHorarios = sessao.get(URLS['menu_action_matricula'] + matricula)
    sitePerfil = sessao.get(URLS['perfil_perfil_action'])

    return jsonify({
        "codigo": 200,
        "data": {
            "academico": {
                "Matricula": pegaPropriedadePerfil(siteHorarios.content, '.Matrícula:'),
                "Curso": pegaPropriedadePerfil(siteHorarios.content, '.Curso:'),
                "Periodo Atual": pegaPropriedadePerfil(siteHorarios.content, '.Período Atual:')
            },
            "informacoes": {
                "Nome": pegaPropriedadePerfil(sitePerfil.content, '.Nome'),
                "Nome da Mae": pegaPropriedadePerfil(sitePerfil.content, '.Nome da Mãe'),
                "Nome do Pai": pegaPropriedadePerfil(sitePerfil.content, '.Nome da Pai'),
                "Nascimento": pegaPropriedadePerfil(sitePerfil.content, '.Nascimento'),
                            "Sexo":             pegaPropriedadePerfil(sitePerfil.content, '.Sexo'),
                            "Etnia":            pegaPropriedadePerfil(sitePerfil.content, '.Etnia'),
                            "Deficiencia":      pegaPropriedadePerfil(sitePerfil.content, '.Deficiência'),
                            "Tipo Sanguineo":   pegaPropriedadePerfil(sitePerfil.content, '.Tipo Sanguíneo'),
                            "Fator RH":         pegaPropriedadePerfil(sitePerfil.content, '.Fator RH'),
                            "Estado Civil":     pegaPropriedadePerfil(sitePerfil.content, '.Estado Civil'),
                            "Pagina Pessoal":   pegaPropriedadePerfil(sitePerfil.content, '.Página Pessoal'),
                            "Nacionalidade":    pegaPropriedadePerfil(sitePerfil.content, '.Nacionalidade'),
                            "Estado":           pegaPropriedadePerfil(sitePerfil.content, '.Estado'), #TODO: consertar bug, Estado obtem Estado Civil
                            "Naturalidade":     pegaPropriedadePerfil(sitePerfil.content, '.Naturalidade')
                        },
                        "endereco":{
                            "Tipo de endereco":     pegaPropriedadePerfil(sitePerfil.content, '.Tipo de endereço'),
                            "Tipo de logradouro":   pegaPropriedadePerfil(sitePerfil.content, '.Tipo de logradouro'),
                            "Logradouro":           pegaPropriedadePerfil(sitePerfil.content, '.Logradouro'),
                            "Numero":               pegaPropriedadePerfil(sitePerfil.content, '.Número'), #TODO: consertar bug, Numero não é encontrado
                            "Complemento":          pegaPropriedadePerfil(sitePerfil.content, '.Complemento'),
                            "Bairro":               pegaPropriedadePerfil(sitePerfil.content, '.Bairro'),
                            "Pais":                 pegaPropriedadePerfil(sitePerfil.content, '.País'),
                            "Estado":               pegaPropriedadePerfil(sitePerfil.content, '.Estado'), #TODO: consertar bug, Estado obtem Estado Civil
                            "Cidade": pegaPropriedadePerfil(sitePerfil.content, '.Cidade'),
                            "Distrito": pegaPropriedadePerfil(sitePerfil.content, '.Distrito'),
                            "CEP": pegaPropriedadePerfil(sitePerfil.content, '.CEP'),
                            "Caixa Postal": pegaPropriedadePerfil(sitePerfil.content, '.Caixa Postal'),
                            "E-mail": pegaPropriedadePerfil(sitePerfil.content, '.E-mail'),
                            "Tel. Residencial": pegaPropriedadePerfil(sitePerfil.content, '.Tel. Residencial'),
                            "Tel. Celular": pegaPropriedadePerfil(sitePerfil.content, '.Tel. Celular'),
                            "Tel. Comercial": pegaPropriedadePerfil(sitePerfil.content, '.Tel. Comercial'),
                            "Fax": pegaPropriedadePerfil(sitePerfil.content, '.Fax')
                        }
        }
    })


@app.route('/perfil/foto', methods=['GET'])
def perfilFoto():
    sessao = Session()

    cookie = request.args.get('cookie')
    sessao.cookies.set("JSESSIONID", cookie)

    if not Autenticado(cookie):
        return jsonify({
            "code": 401,
            "error": "Nao autorizado"
        })

    img_data = sessao.get(URLS['foto_action']).content
    img = io.BytesIO()
    img.write(img_data)
    img.seek(0)

    return send_file(
        img,
        as_attachment=True,
        attachment_filename='imagemPerfil.jpeg',
        mimetype='image/jpeg'
    )


@app.route('/horarios', methods=['GET'])
def horarios():
    '''
    sessao = Session()

    cookie = request.args.get('cookie')
    matricula = request.args.get('matricula')

    if (Autenticado(cookie)):
        
    sessao.cookies.set("JSESSIONID", cookie)
    
    siteHorarios = sessao.get("https://alunos.cefet-rj.br/aluno/ajax/aluno/quadrohorario/quadrohorario.action?matricula=" + matricula)
    siteHorariosBS = bs(siteHorarios.content, "html.parser")

    HorariosLinhas = siteHorariosBS.find(id = 'quadrohorario').find_all('tr')

    HorariosLinhasTratado = str(HorariosLinhas).replace("</div></td></div></td></div></td></div></td></div></td></div></td></tr>",'')

    HorariosLinhasTratadoBS = bs(HorariosLinhasTratado, "html.parser")

    print(HorariosLinhas)

    Horarios = []

    for linha in HorariosLinhas:
        HorariosCelulas = linha.find_all('td')

        horario = {}
        horario['intervalo'] = normalizacao(HorariosCelulas[0].get_text())
        print("-------------------------------------------")
        print(HorariosCelulas[0])
        print("-------------------------------------------")

        dias = {}
        dias['Dom'] = normalizacao(HorariosCelulas[1].get_text())
        dias['Seg'] = normalizacao(HorariosCelulas[2].get_text())
        dias['Ter'] = normalizacao(HorariosCelulas[3].get_text())
        dias['Qua'] = normalizacao(HorariosCelulas[4].get_text())
        dias['Qui'] = normalizacao(HorariosCelulas[5].get_text())
        dias['Sex'] = normalizacao(HorariosCelulas[6].get_text())
        dias['Sab'] = normalizacao(HorariosCelulas[7].get_text())

        horario['dias'] = dias

        Horarios.append(horario)

    return jsonify({"horarios":Horarios})

    TrLinhas = HorariosTabela.find_all('tr')

    for itemTrLinhas in TrLinhas:
        
        TdCelula = TrLinhas.find_all('td')
        
        for itemCelula in TdCelula:
            celula = itemCelula.find('a')
            print(celula.text)
'''
    return jsonify({
        "code": 501,
        "error": "Nao Implementado"
    })


@app.route('/relatorios', methods=['GET'])
def lista_relatorios():
    sessao = Session()

    cookie = request.args.get('cookie')
    matricula = request.args.get('matricula')

    if not Autenticado(cookie):
        return jsonify({
            "code": 401,
            "error": "Nao autorizado"
        })

    sessao.cookies.set("JSESSIONID", cookie)
    siteRelatorios = sessao.get(URLS['relatorio_action_matricula'] + matricula)
    siteRelatoriosBS = bs(siteRelatorios.content, "html.parser")

    RelatoriosBrutos = siteRelatoriosBS.find_all('a', {'title': 'Relatório em formato PDF'})

    Relatorios = []
    for item in RelatoriosBrutos:
        relatorio = {}
        relatorio['id'] = RelatoriosBrutos.index(item)
        relatorio['nome'] = normalizacao(item.previousSibling)
        relatorio['link'] = item['href'].replace("/aluno/aluno/relatorio/", '')
        Relatorios.append(relatorio)

        return jsonify({
            "codigo": 200,
            "data": Relatorios
        })


@app.route('/relatorios/pdf', methods=['GET'])
def geraRelatorio():
    sessao = Session()

    cookie = request.args.get('cookie')
    link = request.args.get('link')

    if not Autenticado(cookie):
        return jsonify({
            "code": 401,
            "error": "Nao autorizado"
        })

    sessao.cookies.set("JSESSIONID", cookie)

    pdf_data = sessao.get(URLS['aluno_relatorio'] + link).content
    pdf = io.BytesIO()
    pdf.write(pdf_data)
    pdf.seek(0)

    return send_file(
        pdf,
        as_attachment=True,
        attachment_filename='relatorio.pdf',
        mimetype='application/pdf'
    )


@app.route('/autenticacao', methods=['POST'])
def autenticacao():
    sessao = Session()

    usuario = request.get_json().get('usuario')
    senha = request.get_json().get('senha')

    sessao.headers.update({'referer': URLS['matricula']})
    sessao.get(URLS['aluno_login_action_error'])

    dados_login = {"j_username": usuario, "j_password": senha}

    sitePost = sessao.post(URLS['security_check'], data=dados_login)
    sitePostBS = bs(sitePost.content, "html.parser")

    Matricula = sitePostBS.find("input", id="matricula")["value"]
    Cookie = sessao.cookies.get_dict()

    if Cookie == '':
        return jsonify({
            "code": 401,
            "error": "Nao autorizado"
        })

    return jsonify({
        "code": 200,
        "data": {
            "matricula": Matricula,
            "cookie": Cookie['JSESSIONID']
        }
    })

@app.errorhandler(404)
def respond404(error):
    return jsonify({
        "code": 404,
        "error": "Nao encontrado"
    })

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)  # para prod, ative aqui!
    #app.run(debug=True, host='127.0.0.1', port=port)  # para dev, ative aqui!
