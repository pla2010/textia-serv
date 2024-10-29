from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Utilise SQLite pour commencer
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle de l'utilisateur
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

# Modèle des publications
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(240), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Créer la base de données
with app.app_context():
    db.create_all()

# Route d'inscription
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Utilisateur déjà existant.'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Inscription réussie !'}), 201

# Route de connexion
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({'message': 'Connexion réussie !', 'user_id': user.id}), 200
    else:
        return jsonify({'message': 'Nom d’utilisateur ou mot de passe incorrect.'}), 401

# Route pour créer une publication
@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.json
    content = data.get('content')
    user_id = data.get('user_id')

    new_post = Post(content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Publication créée avec succès !'}), 201

# Route pour récupérer les publications
@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    output = []
    for post in posts:
        output.append({'id': post.id, 'content': post.content, 'user_id': post.user_id})
    return jsonify(output), 200

# Lancer l'application
if __name__ == '__main__':
    app.run(debug=True)
