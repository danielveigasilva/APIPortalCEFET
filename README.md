<p align="center">
    <img src="/imagens/logo.PNG" width="80%">
    <br></br>
    API desenvolvida em linguagem Python para interação web com o portal online da 
    nstituição federal Centro Federal de Educação Tecnológica Celso Suckow da Fonseca (CEFET/RJ).
</p>


## Sobre

Application Programming Interface (API) é um conjunto de padrões de programação que 
permite acesso a um serviço em expecífico. Em resumo, é uma camada intermediária que 
promove a interação de uma aplicação com o serviço desejado, neste caso o 
[portal do aluno CEFET/RJ](https://alunos.cefet-rj.br/aluno/).

<p align="center">
    <img src="/imagens/api.png" width="80%">
</p>

## Objetivo

Este projeto tem por objetivo fomentar o desenvolvimento de aplicações que visam facilitar 
o acesso a informações referentes ao portal online de docentes e dicentes da instituição.

## Desenvolvimento

Este projeto ainda está em desenvolvimento, novas funcionalidades estão sendo adicionadas constantemente. 
Abaixo segue o andamento das implementações:
- **Autenticação**
    
    :heavy_check_mark: autenticacao   **[Atualizada** :triangular_flag_on_post: **]**
- **Relatórios**
    
    :heavy_check_mark: listaRelatorios
    
    :heavy_check_mark: geraRelatorio
- **Perfil**
    
    :warning: perfilDados *[BETA]*
    
    :heavy_check_mark: perfilDadosGerais
    
    :heavy_check_mark: perfilFoto

## Utilização

Atualmente a API está hospedada no site [Heroku](https://www.heroku.com/) e pode ser acessada através da URL: 

```url
https://api-portal-cefet.herokuapp.com
```

### Funções

1. **Autenticação**
    - **/token/{matricula}/{senha}** _[ GET ]_
    
        Esta função é responsável por autenticar uma nova sessão no portal.
        
        URL:
        ```bash
       curl -XPOST -H "Content-type: application/json" -d '{"usuario" : "%matricula%",  "senha" : "%senha%"}' 'https://api-portal-cefet.herokuapp.com/auth'
        ```
        
        Se o login occorer corretamente o retorno será um json contendo um *token* de autenticação.
    
        Exemplo de json de retorno:
        ```json
        {
	        "code": 200,
            "data": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6Im9jdCJ9.eyJjb29raWUiOiJjb29raWUtdGVzdGUiLCJtYXRyaWN1bGEiOiIxMjM0NTY3R0NPTSJ9.gq7p3CgzqJyb_MTM30zCkI0K9dEJY4BrGV9d43l9uvw"
            } 
        }
        ```

2. **Perfil**

    - **/perfil** _[ GET ]_
    
        Esta função é responsável por listar os dados principais 
        (*Nome, Curso, Matrícula Acadêmica e Período*).
         
        ```bash
        curl -XGET -H 'X-Token: {token}' 'https://api-portal-cefet.herokuapp.com/perfil'
        ```
        Se o token for válido o retorno será um json contendo 
        o código 200 e uma lista de dados.
    
        Exemplo de json de retorno:
        
        ```json
        {
            "codigo": 200,
            "data":{
                "Curso":"PET - CURSO DE ENGENHARIA DE COMPUTACAO",
                "Matricula":"1234567GCOM",
                "Periodo Atual":"5",
                "Nome":"Luke Skywalker"
            }
        }
        ```

    - **/perfil/geral** _[ GET ] [BETA]_
    
        Esta função é responsável por listar os dados cadastrados, 
        tais como *endereço*, *número de telefone*, *E-mail* e etc. 
        
        ```url
        curl -XGET -H 'X-Token: {token}' 'https://api-portal-cefet.herokuapp.com/perfil/geral'
        ```
        Se o token for válido o retorno será um json contendo o 
        código 200 e uma lista de dados divididos em quadro tipos: 
        *academico*, *informacoes*, *endereco* e *documentos*.
    
        Exemplo de json de retorno:
        
        ```json
        {
            "codigo": 200,
            "data": {
                "academico":{
                    "Curso":"PET - CURSO DE ENGENHARIA DE COMPUTACAO",
                    "Matricula":"1234567GCOM",
                    "Periodo Atual":"5"
                },
                "endereco":{
                    "Bairro":"CENTRO",
                    "CEP":"00000-000",
                    "Cidade":"Tatooine"
                },
                "informacoes":{
                    "Nascimento":"18/11/1977",
                    "Nome":"Luke Skywalker",
                    "Nome da Mae":"Padmé Amidala",
                    "Nome do Pai":"Anakin Skywalker"
                }
            }
        }
        ```
        
    - **/perfil/foto** _[ GET ]_
    
        Esta função é responsável por obter a foto de perfil cadastrada no portal. 
        
        ```bash
        curl -XGET -H 'X-Token: {token}' 'https://api-portal-cefet.herokuapp.com/perfil/foto'
        ```
        Se o token for válido o retorno será um arquivo *imagemPerfil.jpeg*.

     

3. **Relatórios**

    - **/relatorios** _[ GET ]_
    
        Esta função é responsável por listar os relatórios disponíveis para o seu perfil. 
        
        ```bash
        curl -XGET -H 'X-Token: {token}' 'https://api-portal-cefet.herokuapp.com/relatorios'
        ```
        Se o token for válido o retorno será um json contendo o código 200
        e uma lista de relatórios contendo *ID*, *Nome* e *Link*.
    
        Exemplo de json de retorno:
        ```json
        {
           "codigo": 200,
           "data":[
                {
                    "id":0,
                    "link":"atestadoTrancamento.action?matricula=123456",
                    "nome":"Atestado Trancamento"
                },
                {
                    "id":1,
                    "link":"boletimEscolar.action?matricula=123456",
                    "nome":"Boletim Escolar"
                }
           ]
        }
        ```

    - **/relatorios/{link}** _[ GET ]_
    
        Esta função é responsável por gerar um relatório expecificado pelo link.
        
        ```url
        curl -XGET -H 'X-Token: {token}' 'https://api-portal-cefet.herokuapp.com/relatorios/{link}/pdf'
        ```
        Se o token for válido o retorno será um arquivo *relatorio.pdf*.
        