#Daniel Veiga

#cookie = s.cookies.get_dict()

#print(cookie['JSESSIONID'])
from flask import Flask, jsonify, request
import urllib.request      
import html

from requests import Session
from bs4 import BeautifulSoup as bs
import json

app = Flask(__name__)
sessao = Session()

def login(usuario,senha):

    sessao.headers.update({'referer': 'https://alunos.cefet-rj.br/aluno/login.action?error='})
    sessao.get("https://alunos.cefet-rj.br/aluno/login.action?error=")

    dados_login = {"j_username":usuario,"j_password":senha}

    sitePost = sessao.post("https://alunos.cefet-rj.br/aluno/j_security_check",data = dados_login)
    siteConteudo = bs(sitePost.content, "html.parser")

    siteMatricula = siteConteudo.find('input', id='matricula')['value']

    return siteMatricula

@app.route('/dados/', methods=['GET'])
def dados():

    usuario = request.args.get('usuario')
    senha = request.args.get('senha')

    siteMatricula = login(usuario,senha)

    site = sessao.get("https://alunos.cefet-rj.br/aluno/aluno/relatorio/relatorios.action?matricula="+siteMatricula)

    print(site.content)

if __name__ == "__main__":
    app.run(debug=True)

#http://127.0.0.1:5000/

#------------------------LINKS-------------------------

#Perfil         - https://alunos.cefet-rj.br/aluno/aluno/perfil/perfil.action
#AlterarSenha   - https://alunos.cefet-rj.br/usuario/usuario/usuario.action?br.com.asten.si.geral.web.spring.interceptors.AplicacaoWebChangeInterceptor.aplicacaoWeb=1
#Matricula      - https://alunos.cefet-rj.br/aluno/aluno/matricula/solicitacoes.action?matricula=           +  siteMatricula
#Relatorio      - https://alunos.cefet-rj.br/aluno/aluno/relatorio/relatorios.action?matricula=             +  siteMatricula
#Horarios       - https://alunos.cefet-rj.br/aluno/aluno/quadrohorario/menu.action?matricula=               +  siteMatricula
#Notas          - https://alunos.cefet-rj.br/aluno/aluno/nota/nota.action?matricula=                        +  siteMatricula
#Comunicacoes   - https://alunos.cefet-rj.br/comunicacoes/noticia/list.action?br.com.asten.si.geral.web.spring.interceptors.AplicacaoWebChangeInterceptor.aplicacaoWeb=1
#Manuais        - https://alunos.cefet-rj.br/aluno/manuais.action