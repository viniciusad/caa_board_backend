import uuid
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    token = db.Column(db.String(64), index=True, unique=True)
    
    # Relationship to user_cards
    cards = db.relationship('UserCard', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self):
        if not self.token:
            self.token = uuid.uuid4().hex
            db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token = None
        db.session.add(self)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(64), index=True)
    icon_class = db.Column(db.String(128)) # e.g. "fas fa-apple-alt"
    card_type = db.Column(db.String(32))   # e.g. "noun", "verb", "connector"
    is_default = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # None for default cards

class UserCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    position = db.Column(db.Integer)       # Used to sort cards on the board
    is_hidden = db.Column(db.Boolean, default=False)
    
    card = db.relationship('Card')
