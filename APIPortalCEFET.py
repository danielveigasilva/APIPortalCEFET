#Daniel Veiga
#data.append({'f':var})
#cookie = s.cookies.get_dict()
#return send_file("teste.pdf", attachment_filename='teste.pdf')
#pip freeze > requirements.txt

#print(cookie['JSESSIONID'])
from flask import Flask, jsonify, request, send_file
import urllib.request      
import html
import unicodedata
import os

from requests import Session
from bs4 import BeautifulSoup as bs
import json

app = Flask(__name__)
sessao = Session()

def normalizacao(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

@app.route('/horarios/', methods=['GET'])
def horarios():
    cookie = request.args.get('cookie')
    matricula = request.args.get('matricula')
    
    sessao.cookies.set("JSESSIONID", cookie)
    siteHorarios = sessao.get("https://alunos.cefet-rj.br/aluno/aluno/quadrohorario/menu.action?matricula=" + matricula)
    siteHorariosBS = bs(siteHorarios.content, "html.parser")

    HorariosLink = siteHorariosBS.find('link', {'rel':'stylesheet'})['href']

    return jsonify({"HorariosLink":HorariosLink})



@app.route('/listaRelatorios/', methods=['GET'])
def lista_relatorios():

    cookie = request.args.get('cookie')
    matricula = request.args.get('matricula')
    
    sessao.cookies.set("JSESSIONID", cookie)
    siteRelatorios = sessao.get("https://alunos.cefet-rj.br/aluno/aluno/relatorio/relatorios.action?matricula=" + matricula)
    siteRelatoriosBS = bs(siteRelatorios.content, "html.parser")

    RelatoriosBrutos = siteRelatoriosBS.find_all('a', {'title':'Relatório em formato PDF'})

    Relatorios = []
    for item in RelatoriosBrutos:
        relatorio = {}
        relatorio['id'] = RelatoriosBrutos.index(item)
        relatorio['nome'] = normalizacao(item.previousSibling).replace('  ','')
        relatorio['link'] = "https://alunos.cefet-rj.br" + item['href']
        Relatorios.append(relatorio)

    return jsonify({"relatorios":Relatorios})

@app.route('/autenticacao/', methods=['GET'])
def login():

    usuario = request.args.get('usuario')
    senha = request.args.get('senha')

    sessao.headers.update({'referer': 'https://alunos.cefet-rj.br/aluno/login.action?error='})
    sessao.get("https://alunos.cefet-rj.br/aluno/login.action?error=")

    dados_login = {"j_username":usuario,"j_password":senha}

    sitePost = sessao.post("https://alunos.cefet-rj.br/aluno/j_security_check",data = dados_login)
    sitePostBS = bs(sitePost.content, "html.parser")

    try:
        Matricula = sitePostBS.find("input", id="matricula")["value"]
    except:
        Matricula = 0
    
    Cookie = sessao.cookies.get_dict()
    return jsonify({"site": str(sitePostBS.contents), "matri": Matricula})
    #return jsonify({
    #                    "autenticacao":{
    #                        "matricula": Matricula,
    #                        "cookie": Cookie['JSESSIONID']
    #                    }
    #                })

if __name__ == "__main__":
    #app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

#http://127.0.0.1:5000/

#------------------------LINKS-------------------------

#Perfil         - https://alunos.cefet-rj.br/aluno/aluno/perfil/perfil.action
#AlterarSenha   - https://alunos.cefet-rj.br/usuario/usuario/usuario.action?br.com.asten.si.geral.web.spring.interceptors.AplicacaoWebChangeInterceptor.aplicacaoWeb=1
#Matricula      - https://alunos.cefet-rj.br/aluno/aluno/matricula/solicitacoes.action?matricula=           +  siteMatricula
#OK - Relatorio      - https://alunos.cefet-rj.br/aluno/aluno/relatorio/relatorios.action?matricula=             +  siteMatricula
#Horarios       - https://alunos.cefet-rj.br/aluno/aluno/quadrohorario/menu.action?matricula=               +  siteMatricula
#Notas          - https://alunos.cefet-rj.br/aluno/aluno/nota/nota.action?matricula=                        +  siteMatricula
#Comunicacoes   - https://alunos.cefet-rj.br/comunicacoes/noticia/list.action?br.com.asten.si.geral.web.spring.interceptors.AplicacaoWebChangeInterceptor.aplicacaoWeb=1
#Manuais        - https://alunos.cefet-rj.br/aluno/manuais.action