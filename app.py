import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)

# Configuração do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco_dados.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Criando o modelo (tabela)
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, default=date.today)

if not os.path.exists("banco_dados.db"):
    with app.app_context():
        db.create_all()

@app.route('/')
def home():
    produtos = Produto.query.all()
    resultado = []
    for p in produtos:
        resultado.append({
            "id": p.id,
            "nome": p.nome,
            "valor": p.valor,
            "data": p.data
        })
    return render_template('index.html', produtos=resultado)
    
@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form.get('item')
    valor = float(request.form.get('valor'))
    novo = Produto(nome=nome, valor=valor)
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)





