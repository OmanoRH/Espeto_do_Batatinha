from flask import Flask, render_template, request, redirect, url_for

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

# Página com os conteúdos de Python (estruturação, repetição, etc.)
@app.route("/conteudo")
def conteudo():
    return render_template("conteudo.html")

# Página do dicionário com listagem de termos
@app.route("/dicionario")
def dicionario():
    termos = []
    try:
        with open(CAMINHO_TERMO, "r", encoding="utf-8") as f:
            for linha in f:
                termo, definicao = linha.strip().split("=")
                termos.append((termo, definicao))
    except FileNotFoundError:
        pass  # Arquivo ainda não existe
    return render_template("dicionario.html", termos=termos)

# Página para adicionar um novo termo ao dicionário
@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if request.method == "POST":
        termo = request.form["termo"]
        definicao = request.form["definicao"]
        with open(CAMINHO_TERMO, "a", encoding="utf-8") as f:
            f.write(f"{termo}={definicao}\n")
        return redirect(url_for("dicionario"))
    return render_template("adicionar_termo.html")

# Página para editar um termo existente
@app.route("/editar/<termo>", methods=["GET", "POST"])
def editar(termo):
    termos = []
    with open(CAMINHO_TERMO, "r", encoding="utf-8") as f:
        for linha in f:
            t, d = linha.strip().split("=")
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

# Excluir um termo
@app.route("/excluir/<termo>")
def excluir(termo):
    termos = []
    with open(CAMINHO_TERMO, "r", encoding="utf-8") as f:
        for linha in f:
            t, d = linha.strip().split("=")
            if t != termo:
                termos.append((t, d))

    with open(CAMINHO_TERMO, "w", encoding="utf-8") as f:
        for t, d in termos:
            f.write(f"{t}={d}\n")

    return redirect(url_for("dicionario"))

# Página de dúvidas com integração Gemini (placeholder por enquanto)
@app.route("/perguntas", methods=["GET", "POST"])
def perguntas():
    resposta = ""
    if request.method == "POST":
        pergunta = request.form["pergunta"]
        # Aqui você vai futuramente integrar com a API do Gemini
        resposta = f"Simulação de resposta da IA para: {pergunta}"
    return render_template("perguntas.html", resposta=resposta)

# Roda o app
if __name__ == "__main__":
    app.run(debug=True)
