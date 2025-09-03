import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)

# Configuração do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco_dados.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # para economizar recursos
db = SQLAlchemy(app)

# Criando o modelo (tabela)
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=date.today)

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
            "nome": p.name,
            "valor": p.value,
            "data": p.date.strftime('%d/%m/%Y')
        })
    return render_template('index.html', produtos=resultado)
    
@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form.get('item').lower()
    valor = float(request.form.get('valor'))
    novo = Produto(name=nome, value=valor)

    # Verificando se já existe o produto
    nome_produtos = Produto.query.filter(Produto.name==nome).first()
    if nome_produtos is not None:
        return redirect(url_for('home'))
    else:
        db.session.add(novo)
        db.session.commit()
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)





