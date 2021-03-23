<h1>Cadastro Usuário Web</h1>

<h2>Aplicação web para cadastro de usuários utilizando flask-login e flask-dance</h2>

<h3>Link Heroku</h3> 

https://pontotel-challenge.herokuapp.com/

<h3>Dados do cadastro</h3>

* nome
* email
* endereço do usuário
* País
* Estado
* Município
* CEP
* Rua
* Número
* Complemento
* CPF
* PIS
* Senha

**Login**: Por email, CPF ou PIS + senha 

<h2>Utilização</h2>

**Clonar o repositório**: `https://github.com/natalia-rios/desafio_pontotel.git`

**Selecionar a pasta**: `cd desafio_pontotel`

**Instalar bibliotecas necessárias**: `pip install -r requirements.txt`

**Ativar ambiente virtual**: `./.venv\Scripts\activate`

<h3>Para utilizar login por Github e Google:</h3>

**Acessar com github:**
* Acesse Settings -> Developer settings -> OAuth Apps

* Crie um OAuth App e coloque o Client Id o Cliente Secret na seguinte parte do código de _social_login.py_:

`github_blueprint = make_github_blueprint(client_id = 'xxxxxxx', client_secret = 'xxxxxxx')`

**Acessar com google:**
* Acessar o Google APIs Console - https://console.developers.google.com/apis/library?hl=pt-br

* Selecione _Novo projeto_ e siga as instruções

* Acesse Credentials -> Create Credentials -> OAuth client ID -> Selecionar _Web application_

* Siga as instruções e coloque o Client Id o Cliente Secret na seguinte parte do código de _social_login.py_:

`google_blueprint = make_google_blueprint(client_id= "xxxxxxxx", client_secret= "xxxxxxxx",  scope=[`
       `"openid",`
       `"https://www.googleapis.com/auth/userinfo.email",`
       `"https://www.googleapis.com/auth/userinfo.profile",`
   `]`
`)`

<h3>Executar aplicação</h3>

`flask run`

<h3>Executar testes</h3>

`python tests.py`
