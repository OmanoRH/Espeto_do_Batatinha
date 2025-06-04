from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Carrega variáveis de ambiente do .env
load_dotenv()

# Configura a chave da API Gemini a partir do .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Inicializa o modelo Gemini
modelo = genai.GenerativeModel("gemini-2.0-flash")
chat = modelo.start_chat()

# Flask app
app = Flask(__name__)

# Caminho do arquivo que armazenará os termos do dicionário
CAMINHO_TERMO = "termos.txt"

# Página inicial
@app.route("/")
def index():
    return render_template("index.html")

# Página sobre a equipe
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

# Páginas individuais dos conteúdos Python
@app.route("/selecao")
def selecao():
    return render_template("conteudo/selecao.html")

@app.route("/repeticao")
def repeticao():
    return render_template("conteudo/repeticao.html")

@app.route("/vetores")
def vetores():
    return render_template("conteudo/vetores_matrizes.html")

@app.route("/funcoes")
def funcoes():
    return render_template("conteudo/funcoes_procedimentos.html")

@app.route("/excecoes")
def excecoes():
    return render_template("conteudo/excecoes.html")

# Página do dicionário com listagem de termos
@app.route("/dicionario")
def dicionario():
    termos = []
    try:
        with open(CAMINHO_TERMO, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if "=" in linha:
                    termo, definicao = linha.split("=", 1)
                    termos.append((termo, definicao))
    except FileNotFoundError:
        pass
    return render_template("dicionario.html", termos=termos)

# Adicionar termo
@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if request.method == "POST":
        termo = request.form["termo"]
        definicao = request.form["definicao"]
        with open(CAMINHO_TERMO, "a", encoding="utf-8") as f:
            f.write(f"{termo}={definicao}\n")
        return redirect(url_for("dicionario"))
    return render_template("adicionar_termo.html")

# Editar termo
@app.route("/editar/<termo>", methods=["GET", "POST"])
def editar(termo):
    termos = []
    with open(CAMINHO_TERMO, "r", encoding="utf-8") as f:
        for linha in f:
            if "=" in linha:
                t, d = linha.strip().split("=", 1)
                termos.append((t, d))

    if request.method == "POST":
        nova_definicao = request.form["definicao"]
        with open(CAMINHO_TERMO, "w", encoding="utf-8") as f:
            for t, d in termos:
                if t == termo:
                    f.write(f"{t}={nova_definicao}\n")
                else:
                    f.write(f"{t}={d}\n")
        return redirect(url_for("dicionario"))

    definicao_atual = dict(termos).get(termo, "")
    return render_template("editar_termo.html", termo=termo, definicao=definicao_atual)

# Excluir termo
@app.route("/excluir/<termo>")
def excluir(termo):
    termos = []
    with open(CAMINHO_TERMO, "r", encoding="utf-8") as f:
        for linha in f:
            if "=" in linha:
                t, d = linha.strip().split("=", 1)
                if t != termo:
                    termos.append((t, d))

    with open(CAMINHO_TERMO, "w", encoding="utf-8") as f:
        for t, d in termos:
            f.write(f"{t}={d}\n")

    return redirect(url_for("dicionario"))

# Página de perguntas com integração do Gemini
@app.route("/perguntas", methods=["GET", "POST"])
def perguntas():
    resposta = ""
    if request.method == "POST":
        pergunta = request.form["pergunta"]
        try:
            resposta = chat.send_message(pergunta).text
        except Exception as e:
            resposta = f"Erro ao gerar resposta: {e}"
    return render_template("perguntas.html", resposta=resposta)

# Roda o app
if __name__ == "__main__":
    app.run(debug=True)
