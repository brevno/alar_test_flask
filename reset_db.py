from app import db
from app.models import User

db.drop_all()
db.create_all()
db.session.commit()

first_user = User(name=u'admin', is_admin=True, password=u'crnagora')
db.session.add(first_user)

db.session.commit()

print 'Reset DB OK'
