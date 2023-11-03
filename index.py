from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Configure sua chave de API da OpenAI
api_key = 'sua_chave_de_api_aqui'

# Rota para receber perguntas e retornar respostas
@app.route('/pergunta', methods=['POST'])
def perguntar():
    pergunta = request.json['pergunta']

    # Use a chave da API para enviar a pergunta para o modelo da OpenAI
    resposta = openai.Completion.create(
        engine="text-davinci-002",
        prompt=pergunta,
        max_tokens=50,
        api_key=api_key
    )

    return jsonify({'resposta': resposta.choices[0].text})

if __name__ == '__main__':
    app.run(debug=True)
