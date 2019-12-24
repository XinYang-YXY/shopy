from datetime import datetime
from shopyP import db, login_manager # database instance, login-auth instance
from flask_login import UserMixin # used for login-auth, To satisfy the login_manager requirements

@login_manager.user_loader # Decorator used to find the user id, so we can perform a match and carry on
def load_user(user_id):
    return User.query.get(int(user_id))

# Class format for user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    cart = db.relationship('CartItem', backref='owner')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
# Cart item
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
