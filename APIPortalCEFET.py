
#cookie = s.cookies.get_dict()

#print(cookie['JSESSIONID'])

from requests import Session
from bs4 import BeautifulSoup as bs
import json

s = Session()

s.headers.update({'referer': 'https://alunos.cefet-rj.br/matricula/'})
s.get("https://alunos.cefet-rj.br/aluno/login.action?error=")

#bs_content = bs(site.content, "html.parser")

login_data = {"j_username":"matricula","j_password":"senha"}

sitePost = s.post("https://alunos.cefet-rj.br/aluno/j_security_check",data = login_data)

siteGet = s.get("https://alunos.cefet-rj.br/aluno/index.action")

siteConteudo = bs(sitePost.content, "html.parser")
siteMatricula = siteConteudo.find('input', id='matricula')['value']
print(siteMatricula)

#------------------------LINKS-------------------------

#Perfil         - https://alunos.cefet-rj.br/aluno/aluno/perfil/perfil.action
#AlterarSenha   - https://alunos.cefet-rj.br/usuario/usuario/usuario.action?br.com.asten.si.geral.web.spring.interceptors.AplicacaoWebChangeInterceptor.aplicacaoWeb=1
#Matricula      - https://alunos.cefet-rj.br/aluno/aluno/matricula/solicitacoes.action?matricula=           +  siteMatricula
#Relatorio      - https://alunos.cefet-rj.br/aluno/aluno/relatorio/relatorios.action?matricula=             +  siteMatricula
#Horarios       - https://alunos.cefet-rj.br/aluno/aluno/quadrohorario/menu.action?matricula=               +  siteMatricula
#Notas          - https://alunos.cefet-rj.br/aluno/aluno/nota/nota.action?matricula=                        +  siteMatricula
#Comunicacoes   - https://alunos.cefet-rj.br/comunicacoes/noticia/list.action?br.com.asten.si.geral.web.spring.interceptors.AplicacaoWebChangeInterceptor.aplicacaoWeb=1
#Manuais        - https://alunos.cefet-rj.br/aluno/manuais.action