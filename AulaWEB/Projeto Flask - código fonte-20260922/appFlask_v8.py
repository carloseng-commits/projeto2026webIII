from pathlib import Path

from flask import Flask, render_template
from flask import request   #para trabalhar com os métodos GET e POST
from flask import flash     #para msgs popup
from flask import redirect  #para redirecionar páginas


# os templates ficam em uma subpasta do projeto. Definimos o caminho absoluto para
# evitar erros quando a aplicação é iniciada a partir da pasta raiz do repositório.
base_dir = Path(__file__).resolve().parent
template_dir = base_dir / "t_templates"

app_carlos = Flask(__name__, template_folder=str(template_dir))
# no caso de usar flash pede a configuração de uma chave secreta
app_carlos.config['SECRET_KEY'] = "palavra-secreta-IFRO"

@app_carlos.route("/", endpoint="index")       #se no navegador digitar / ou /index
@app_carlos.route("/index", endpoint="index")  
def indice():
    return render_template ("t_index.html") 

@app_carlos.route("/contato", endpoint="contato")
def contato():
    return render_template("t_contato.html") 

#rota /usuarios COM passagem de argumentos
@app_carlos.route("/usuario/<nome_usuario>;<nome_profissao>", endpoint="dados_usuario")
#rota /usuarios SEM passagem de argumentos --> definir valor padrão com defaults
@app_carlos.route("/usuario", defaults={"nome_usuario":"usuário?","nome_profissao":""}, endpoint="dados_usuario")  
def usuarios (nome_usuario, nome_profissao):
    dados_usu = {"profissao": nome_profissao, "disciplina":"Desenvolvimento Web III"}
    return render_template ("t_usuario.html", nome=nome_usuario, dados = dados_usu)  


@app_carlos.route("/login")
def login():
    return render_template("t_login_flash_js_cadastro.html") 


"""
Para poder recuperar os argumentos passados nos parâmetros na URL precisa importar o pacote
from flask import request

Também precisa colocar que essa página aceita requisições de tipo GET ou POST
O GET é padrão, mas no caso do POST altere no html method="POST"


"""
@app_carlos.route("/autenticar", methods=['GET','POST']) 
def autenticar():
    #método POST - pega nos fields (campos) do formulário
    usuario = request.form.get('nome_usuario')
    senha = request.form.get('senha')
    if verificar_login(usuario, senha):
        msg = "Login e senha corretos. Acesso permitido."
        return f"{msg} para {usuario} "
    else:
        #para não dar msg. na outra página, vamos manter na própria página com flash
        #adicionar import flash
        flash("Dados inválidos!")
        flash("Login ou senha incorretos. Acesso negado.")
        return redirect ('/login') #adicionar import redirect

# a rota /autenticar tem uma forte dependência do front-end (formulário HTML)
# tanto na entrada de dados como no retorno
# não é uma API. 

"""  FUNÇÕES Auxiliares """
# Base de dados de login e senha usando um dicionário com o par chave:valor -> usuario:senha
tabelaUsuarios = {
    "carlos": "SuperSenh@2000",
    "alunoIFRO": "SuperSenh@2000",
    "visitante": "SuperSenh@2000"
}

# Verificação de login e senha
def verificar_login(login, senha):
    if login in tabelaUsuarios and tabelaUsuarios[login] == senha:
        return True
    else:
        return False

@app_carlos.route("/novocadastro/<nome_usuario>" , methods=['POST'])
@app_carlos.route("/novocadastro/", defaults={"nome_usuario":""} , methods=['POST'])
def cadastroUsuario(nome_usuario):
    nome_usuario = request.form.get('nome_usuario')
    return render_template("t_cadastro.html", nome_login = nome_usuario ) 

if __name__ == "__main__": 
     app_carlos.run(port = 8000) 
     
