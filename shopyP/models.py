from datetime import datetime
from shopyP import db, login_manager # database instance, login-auth instance
from flask_login import UserMixin # used for login-auth, To satisfy the login_manager requirements

# To reset password
from shopyP import app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer # To reset user password with email
# To reset password

@login_manager.user_loader # Decorator used to find the user id, so we can perform a match and carry on
def load_user(user_id):
    user_id = int(user_id)
    if user_id >= 10000000000:
        return Admin.query.get(user_id)
    else:
        return User.query.get(user_id)


# Parent class for User + Admin
class Person():
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return f"Person('{self.username}', '{self.email}', '{self.image_file}')"
# Class format for user
class User(db.Model, Person, UserMixin):
    deliveryInfo = db.Column(db.Text)
    cart = db.relationship('CartItem', backref='owner')

    #JT
    posts = db.relationship('Post', backref='author', lazy=True)
    #JT
    # Ken
    purchaseRecords = db.relationship('purchaseRecord', backref='buyer')
    # Ken


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod # Telling the python not to take self as a paramenter
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        # Incase the token is expired
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
# Class format for admin
class Admin(db.Model, Person, UserMixin):
    def __repr__(self):
        return f"Admin('{self.username}', '{self.email}', '{self.image_file}')"

class purchaseRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    itemNum = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    review = db.Column(db.Text, default="User did't give any review, 5 stars by default")
    rating = db.Column(db.Integer, default=5)
    buyerId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Parent Class for the CartItem, HackingProduct
class GeneralGoods():
    id = db.Column(db.Integer, primary_key=True)

    price = db.Column(db.Float)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"GeneralGoods('{self.title}', 'S${self.price}', 'Date added:{self.date_added}')"
# Cart item
class CartItem(db.Model, GeneralGoods):
    title = db.Column(db.String(100), nullable=False)
    itemNum = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"CartItem('{self.title}', 'S${self.price}', 'Date added:{self.date_added}')"

# Hacking products to sell
class HackingProduct(db.Model, GeneralGoods):
    title = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)

    itemNum = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f"HackingProduct('{self.title}', 'S${self.price}', 'Date added:{self.date_added}')"


#Jt
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
#Jt
