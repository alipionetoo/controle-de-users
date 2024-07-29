from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
import os

app = Flask(__name__) # inicializa o Flask

# configuração do bd com o SQLite:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.urandom(24) # chave secreta para flash messages

db.init_app(app)# inicia o bd com o Flask

# rota principal para a página inicial:
@app.route('/')
def home():
    return render_template('index.html')

# rota para registrar usuarios:
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # dados do formulário:
        name = request.form['name'].strip()
        username = request.form['username'].strip().lower()  # convertendo o nome de usuário para minúsculas para não causar conflito em novos registros de usuarios
        password = generate_password_hash(request.form['password'])  # cria a hash da senha
        
        # verifica de já existe o user no bd:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Nome de usuário já existe. Por favor, escolha um novo nome.', 'danger')
            return redirect(url_for('home'))
        
        # cria um novo user e salva no bd:
        new_user = User(name=name, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário registrado com sucesso!', 'success')
        return redirect(url_for('home'))
    return render_template('index.html')

# rota do login de users:
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # dados do formulário:
        username = request.form['username'].strip().lower()
        password = request.form['password']

        # busca o usuário no bd:
        user = User.query.filter_by(username=username).first()

        # verifica a senha:
        if user and check_password_hash(user.password, password):
            return redirect(url_for('users'))
        flash('Credenciais inválidas', 'danger')
        return render_template('login.html'), 401
    return render_template('login.html')

# rota para listar os users:
@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

# listagem para todos os users:
@app.route('/api/users', methods=['GET'])
def api_list_users():
    users = User.query.all()
    return jsonify([user.username for user in users])

# registrar novos users:
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    name = data['name'].strip()
    username = data['username'].strip().lower()
    password = generate_password_hash(data['password'])
    
    # verifica se o user já está no bd:
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Nome de usuário já existe. Por favor, escolha um novo nome.'}), 400
    
    # cria um novo user e salva no bd:
    new_user = User(name=name, username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso'}), 201

# login de users:
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data['username'].strip().lower()
    password = data['password']

    # busca o user no bd:
    user = User.query.filter_by(username=username).first()

    # verifica a senha:
    if user and check_password_hash(user.password, password):
        return jsonify({'message': 'Login bem-sucedido'}), 200
    return jsonify({'message': 'Credenciais inválidas'}), 401

# executa a aplicação:
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # cria as tabelas no bd
    app.run(debug=True)  # executa a aplicação em modo debug
