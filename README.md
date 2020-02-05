# APIPortalCEFET
API desenvolvida em linguagem Python para interação web com o portal online da instituição federal Centro Federal de Educação Tecnológica Celso Suckow da Fonseca (CEFET/RJ). 

## Sobre

### Objetivo
Este projeto tem por objetivo fomentar o desenvolvimento de aplicações que visam facilitar o acesso a informações referentes ao portal online de docentes e dicentes da instituição.

### O que é?

Application Programming Interface (API) é um conjunto de padrões de programação que permite acesso a um serviço em expecífico. Em resumo, é uma camada intermediária que promove a interação de uma aplicação com o serviço desejado, neste caso o [portal do aluno CEFET/RJ](https://alunos.cefet-rj.br/aluno/).

### Utilização

Atualmente a API está hospedada no site [Heroku](https://www.heroku.com/) e pode ser acessada através do da URL: [https://api-portal-cefet.herokuapp.com/](https://api-portal-cefet.herokuapp.com/).

#### Funções

1. **Autenticação (usuário , senha)**
    
    Esta função é responsável por autenticar uma nova sessão no portal. Deve seguir o padrão abaixo para sua execução:
    ```
    https://api-portal-cefet.herokuapp.com/autenticacao/?usuario=SUA_MATRICULA_AQUI&senha=SUA_SENHA_AQUI
    ```
    Se o login occorer corretamente o retorno será um json contendo um Cookie e uma Matrícula interna do site (**Atenação: a matrícula retornada não está ligada a matrícula acadêmica, se trata de um novo dado usado internamente pelo portal**).
    
    Exemplo de json de retorno:
    ```
    {
        "autenticacao":{
        "cookie":"B60E98A57D71D7BBEB80457A125436478",
        "matricula":"123456"
        }
    }
    ```

