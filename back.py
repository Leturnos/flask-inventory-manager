from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <form action="/adicionar" method="post" onsubmit="Adicionado()">
        <input type="text" name="item" id="iname" placeholder="Nome do item a ser adicionado" required>
        <label for="item"></label>

        <input type="number" step="0.01" name="valor" id="ivalor" placeholder="$ do item a ser adicionado" required>
        <label for="valor"></label>

        <input type="submit" value="Adicionar">
    </form>
    '''

conn = sqlite3.connect("testeConexao.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS item (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            nome VARCHAR(100) NOT NULL
            valor REAL NOT NULL
        )
''')

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['item']
    valor = request.form['valor']

    cursor.execute('''
    INSERT INTO item (nome, valor)
    VALUES (%s, %f);
    ''', (nome, valor))
    conn.commit()

@app.route('/dados', methods=['GET'])
def BuscarDados():
    cursor.execute("SELECT * FROM item")
    resultados = cursor.fetchall()
    nome = "nome" in resultados
    valor = "valor" in resultados
    
    return jsonify({
        "nome": nome,
        "valor": valor
    })

if __name__ == '__main__':
    app.run(debug=True)





