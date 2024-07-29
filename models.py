from flask_sqlalchemy import SQLAlchemy

# inicia a extensão:
db = SQLAlchemy()

# define o modelo da tabela user:
class User(db.Model):

    # define as caracteristicas das colunas da tabela:
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # pepresentação do objeto User:
    def __repr__(self):
        return f'<User {self.username}>'
