from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    _password = db.Column("password", db.String)

    @property
    def password(self):
        # for objects modified in runtime display real password, for objects from DB display hash
        return self.raw_password if hasattr(self, 'raw_password') else self._password

    @password.setter
    def password(self, password):
        self.set_password(password)

    def __init__(self, password='', *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)
        self.set_password(password)

    def __repr__(self):
        return '<User %r>' % self.name

    def set_password(self, password):
        self.raw_password = password
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    def get_id(self):
        return unicode(self.id)
