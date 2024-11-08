from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bancodedados.db'
db = SQLAlchemy(app)


class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    sexo = db.Column(db.String(1))
    foto_de_perfil = db.Column(db.String(100))
    forma_de_pagamento = db.Column(db.String(100))
    preferencia = db.Column(db.String(100))
    senha = db.Column(db.String(100))
    dinheiro = db.Column(db.Float, default=2000.00)

    def to_dict(self):
        return {
            'nome': self.nome,
            'email': self.email,
            'sexo': 'Masculino' if self.sexo == 'M' else 'Feminino',
            'foto_de_perfil': 'imagens_usarios/' + self.foto_de_perfil,
            'forma_de_pagamento': self.forma_de_pagamento,
            'preferencia': self.preferencia,
            'dinheiro': str(self.dinheiro).replace('.', ',')
        }


# Cadastro de usuário
@app.route('/cadastro', methods=['POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['username']
        email = request.form['email']
        senha = request.form['password']

        novo_usuario = Pessoa(nome=nome, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()

        return 'Usuário cadastrado com sucesso!'


# Login de usuário
@app.route('/login', methods=['POST'])
def login_usuario():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['password']

        pessoa = Pessoa.query.filter_by(email=email).first()
        if pessoa:
            if pessoa.senha == senha:
                return 'Login bem sucedido'
            else:
                return 'Senha incorreta'
        else:
            return 'Usuário não encontrado'


if __name__ == '__main__':
    app.run(debug=True)
