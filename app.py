from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from synthgpt.cerebro import responder_pergunta, get_memoria

app = Flask(__name__)
CORS(app)  # libera cors para desenvolvimento local

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/perguntar", methods=["POST"])
def perguntar():
    data = request.get_json()
    entrada = data.get("entrada")
    usar_busca_web = data.get("usar_busca_web", False)
    resposta = responder_pergunta(entrada, usar_busca_web)
    return jsonify({"resposta": resposta})

@app.route("/memoria", methods=["GET"])
def memoria():
    return jsonify({"memoria": get_memoria()})

if __name__ == "__main__":
    app.run(debug=True)
