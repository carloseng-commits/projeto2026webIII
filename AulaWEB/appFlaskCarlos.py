from flask import Flask, render_template, request

meu_site = Flask(__name__, template_folder='Projeto Flask - código fonte-20260922/t_templates')  #cria o objeto Flask, que é a aplicação web, e define a pasta templates como pasta de templates


@meu_site.route('/ola')
def raiz():   #esta função está vinculada a rota  /ola
    return render_template('homepage.html')  #retorna o arquivo index.html que está na pasta templates

#veja que o id é um parâmetro da rota e faz parte da URL, e não vai confundir com a rota /ola
@meu_site.route('/ola/<id>') 
def saudacao(id):
    return render_template('homepage_nome.html', campoNome=id)

#retorna o arquivo homepage.html que está na pasta templates. No .html tem o campo {{campoNome}} que vai receber o valor do parâmetro id da rota

from flask import Flask, render_template
from flask import request   #para trabalhar com os métodos GET e POST
from flask import flash     #para msgs popup
from flask import redirect  #para redirecionar páginas


# os templates coloca em outra pasta. 
# Por padrão, fica na pasta templates e não precisa informar no template_folder,
# mas se quiser armazenar em outra pasta indique nesse parâmetro.
app_carlos = Flask(__name__, template_folder='Projeto Flask - código fonte-20260922/t_templates')
# no caso de usar flash pede a configuração de uma chave secreta
app_carlos.config['SECRET_KEY'] = "palavra-secreta-IFRO"


@app_carlos.route("/")       #se no navegador digitar / ou /index
@app_carlos.route("/index")  
def index():
    return render_template ("t_index.html") #optei por prefixar com t_ os nomes dos arquivos que usam template

@app_carlos.route("/contato")
def contato():
    return render_template("t_contato.html") 

#rota /usuarios COM passagem de argumentos
@app_carlos.route("/usuario/<nome_usuario>;<nome_profissao>")
#rota /usuarios SEM passagem de argumentos --> definir valor padrão com defaults
@app_carlos.route("/usuario", defaults={"nome_usuario":"usuário?","nome_profissao":""})  

def dados_usuario (nome_usuario, nome_profissao):
    dados_usu = {"profissao": nome_profissao, "disciplina":"Desenvolvimento Web III"}
    return render_template ("t_usuario.html", nome=nome_usuario, dados = dados_usu)  

#new
@app_carlos.route("/login")
def login():
    return render_template("t_login_flash_js_cadastro.html")
    
#new
"""++++
Para poder recuperar os argumentos passados nos parâmetros na URL precisa importar o pacote
from flask import request

Também precisa colocar que essa página aceita requisições de tipo GET ou POST
O GET é padrão, mas no caso do POST altere no html method="POST"
"""
@app_carlos.route("/autenticar", methods=['GET', 'POST']) 
def autenticar():
    #método POST - pega nos fields (campos) do formulário
    usuario = request.form.get('nome_usuario')
    senha = request.form.get('senha')
    
    if usuario == "admin" and senha == "ifro":
        return f"usuario: {usuario} e senha: {senha}"
    else:
        #para não dar msg. na outra página, vamos manter na própria página com flash
        #adicionar import flash
        flash("Dados inválidos!")
        flash("Login ou senha inválidos!")
        return redirect ('/login') #adicionar import redirect


if __name__ == "__main__": 
     app_carlos.run(port = 8000) 
     
#@meu_site.route('/ola/<id>')
#def saudacao():
#    nome = request.args.get("id")
#    return render_template('homepage_nome.html', campoNome= nome) #retorna o arquivo homepage.html que está na pasta templates

@meu_site.route('/')
@meu_site.route('/index')
def index():   #esta função está vinculada a rota raíz / e rota /index
    return render_template('t_index.html', nome ="Turma 2025") 

@meu_site.route('/contato')
def contato():
    return render_template('t_contato.html')  

@meu_site.route('/usuario')
def dados_usuario():
    #nome_usuario="Mariela"
    dados_usu = {"nome": "Carlos", "profissao": "Professora EBTT", "disciplina":"Desenvolvimento Web III"}
    return render_template("t_usuario.html", dados = dados_usu)
                                           #parâmetro recebe argumento
                                           #colocar o site no ar

@meu_site.route('/usuario/<p_nome>/<p_profissao>/<p_disciplina>')
def dados_usuario2(p_nome, p_profissao, p_disciplina):
    dados_usu = {"nome": p_nome, "profissao": p_profissao, "disciplina": p_disciplina}
    return render_template("usuario.html", dados = dados_usu)

@meu_site.route('/login')
def login():
    return render_template("t_login.html")

@meu_site.route('/autenticar', methods=['GET','POST'])
def autenticarUsuario():
    if request.method == 'POST':
       usuario = request.form.get("nome_usuario")
       senha = request.form.get("senha")
    else:   
       usuario = request.args.get("nome_usuario")
       senha = request.args.get("senha")

    return f"usuario: {usuario} e senha: {senha} recebidos com sucesso!"


#esta função não está vinculado a rota, mas pode ser usada dentro de uma rota ou outra função ou invocada de fora
def saudacaoes(nome): 
    return f"Boa noite, {nome}!. Tudo bem?"

#maiores detalhes nos slides que estão no AVA.
if __name__ == '__main__':  #verifica se o arquivo está sendo executado diretamente, e não importado
    meu_site.run(port=7000)

meu_site.run( port=6000)    #executa caso o o arquivo seja importado, mas não é uma boa prática, pois pode gerar conflito de portas