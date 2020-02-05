![logo](/imagens/logo.PNG)
<p align="center">
    API desenvolvida em linguagem Python para interação web com o portal online da instituição federal Centro Federal de Educação Tecnológica Celso Suckow da Fonseca (CEFET/RJ).
</p>

### Objetivo
Este projeto tem por objetivo fomentar o desenvolvimento de aplicações que visam facilitar o acesso a informações referentes ao portal online de docentes e dicentes da instituição.

### O que é?

Application Programming Interface (API) é um conjunto de padrões de programação que permite acesso a um serviço em expecífico. Em resumo, é uma camada intermediária que promove a interação de uma aplicação com o serviço desejado, neste caso o [portal do aluno CEFET/RJ](https://alunos.cefet-rj.br/aluno/).

### Utilização

Atualmente a API está hospedada no site [Heroku](https://www.heroku.com/) e pode ser acessada através da URL: [https://api-portal-cefet.herokuapp.com/](https://api-portal-cefet.herokuapp.com/).

#### Funções

1. **Autenticação**
    - **autenticacao (usuario , senha)**
    
        Esta função é responsável por autenticar uma nova sessão no portal. Deve seguir o padrão abaixo para sua execução:
        ```url
        https://api-portal-cefet.herokuapp.com/autenticacao/?usuario=SUA_MATRICULA_AQUI&senha=SUA_SENHA_AQUI
        ```
        Se o login occorer corretamente o retorno será um json contendo um *Cookie* e uma *Matrícula* interna do site (**Atenção: a matrícula retornada não está ligada a matrícula acadêmica, se trata de um novo dado usado internamente pelo portal**).
    
        Exemplo de json de retorno:
        ```json
        {
            "autenticacao":{
            "cookie":"B60E98A57D71D7BBEB80457A125436478",
            "matricula":"123456"
            }
        }
        ```

2. **Relatórios**

    - **listaRelatorios (cookie , matricula)**
    
        Esta função é responsável por listar os relatórios disponíveis para o seu perfil. Deve seguir o padrão abaixo para sua execução:
        ```url
        https://api-portal-cefet.herokuapp.com/listaRelatorios/?cookie=COOKIE_AUTENTICADO_AQUI&matricula=MATRICULA_INTERNA_AQUI
        ```
        Se o cookie e a matrícula forem válidos o retorno será um json contendo o código 200 e uma lista de relatórios contendo *ID*, *Nome* e *Link*.
    
        Exemplo de json de retorno:
        ```json
        {
           "codigo":"200",
           "relatorios":[
                {
                    "id":0,
                    "link":"atestadoTrancamento.action?matricula=123456",
                    "nome":"Atestado Trancamento"
                },
                {
                    "id":1,
                    "link":"boletimEscolar.action?matricula=123456",
                    "nome":"Boletim Escolar"
                }]
        }
        ```

    - **geraRelatorio (cookie , link)**
    
        Esta função é responsável por gerar um relatório expecificado pelo link (item passado pela função listaRelatorios). Deve seguir o padrão abaixo para sua execução:
        ```url
        https://api-portal-cefet.herokuapp.com/geraRelatorio/?cookie=COOKIE_AUTENTICADO_AQUI&link=LINK_RELATORIO_AQUI
        ```
        Se o cookie e o link forem válidos o retorno será um arquivo *relatorio.pdf*.

3. **Perfil**

    - **perfilDados (cookie , matricula)** *[BETA]*
    
        Esta função é responsável por listar os dados cadastrados, tais como *endereço*, *número de telefone*, *E-mail* e etc. Deve seguir o padrão abaixo para sua execução:
        ```url
        https://api-portal-cefet.herokuapp.com/perfilDados/?cookie=COOKIE_AUTENTICADO_AQUI&matricula=MATRICULA_INTERNA_AQUI
        ```
        Se o cookie e a matrícula forem válidos o retorno será um json contendo o código 200 e uma lista de dados divididos em quadro tipos: *academico*, *informacoes*, *endereco* e *documentos*.
    
        Exemplo de json de retorno:
        
        ```json
        {
            "academico":{
                "Curso":"PET - CURSO DE ENGENHARIA DE COMPUTACAO",
                "Matricula":"1234567GCOM",
                "Periodo Atual":"5"
             },
             "codigo":"200",
             "endereco":{
                "Bairro":"CENTRO",
                "CEP":"00000-000",
                "Cidade":"Tatooine"
             },
             "informacoes":{
                "Nascimento":"18/11/1977",
                "Nome":"Luke Skywalker",
                "Nome da Mae":"Padmé Amidala",
                "Nome do Pai":"Anakin Skywalker",
             }
        }
        ```
        
     - **perfilDadosGerais (cookie , matricula)**
    
        Esta função é responsável por listar os dados principais (*Nome, Curso, Matrícula Acadêmica e Período*). Deve seguir o padrão abaixo para sua execução:
        ```url
        https://api-portal-cefet.herokuapp.com/listaRelatoriosGerais/?cookie=COOKIE_AUTENTICADO_AQUI&matricula=MATRICULA_INTERNA_AQUI
        ```
        Se o cookie e a matrícula forem válidos o retorno será um json contendo o código 200 e uma lista de dados.
    
        Exemplo de json de retorno:
        
        ```json
        {
            "informacoes":{
                "Curso":"PET - CURSO DE ENGENHARIA DE COMPUTACAO",
                "Matricula":"1234567GCOM",
                "Periodo Atual":"5",
                "Nome":"Luke Skywalker"
             },
             "codigo":"200"
        }
        ```
        
     - **perfilFoto (cookie)**
    
        Esta função é responsável por obter o foto de perfil cadastrada no portal. Deve seguir o padrão abaixo para sua execução:
        ```url
        https://api-portal-cefet.herokuapp.com/perfilFoto/?cookie=COOKIE_AUTENTICADO_AQUI
        ```
        Se o cookie for válido o retorno será um arquivo *imagemPerfil.jpeg*.

     
