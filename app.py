from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Pour permettre les requêtes cross-origin

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle de l'utilisateur
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

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
        return jsonify({'message': 'Connexion réussie !'}), 200
    else:
        return jsonify({'message': 'Nom d’utilisateur ou mot de passe incorrect.'}), 401

# Route de déconnexion
@app.route('/api/logout', methods=['GET'])
def logout():
    return jsonify({'message': 'Déconnexion réussie !'}), 200

# Lancer l'application
if __name__ == '__main__':
    app.run(debug=True)