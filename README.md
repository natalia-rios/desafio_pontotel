<h1>Cadastro Usuário Web</h1>

<h2>Aplicação web para cadastro de usuários utilizando flask-login</h2>

**Link Heroku**: https://pontotel-challenge.herokuapp.com/

**Dados do cadastro:** 
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
*Settings -> Developer settings -> OAuth Apps
*Crie um OAuth App e coloque o Client Id o Cliente Secret na seguinte parte do código de `social_login.py`
`github_blueprint = make_github_blueprint(client_id = 'xxxxxxx', client_secret = 'xxxxxxx')`

**Acessar com google:**
*Acessar o Google APIs Console - https://console.developers.google.com/apis/library?hl=pt-br
*Selecione `Novo projeto` e siga as instruções
*Vá para Credentials -> Create Credentials -> OAuth client ID -> Selecionar `Web application`
*Siga as instruções e coloque o Client Id o Cliente Secret na seguinte parte do código de `social_login.py`

`google_blueprint = make_google_blueprint(client_id= "xxxxxxxx", client_secret= "xxxxxxxx",  scope=[`
       `"openid",`
       `"https://www.googleapis.com/auth/userinfo.email",`
       `"https://www.googleapis.com/auth/userinfo.profile",`
   `]`
`)`

**Executar aplicação**: `flask run`