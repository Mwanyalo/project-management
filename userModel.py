from main import db

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    # CREATE User to DB (Register)
    def createUser(self):
        db.session.add(self)
        db.session.commit()

    # Check if email exists in DB (Register)
    @classmethod
    def emailChecker(cls, email):
        user = UserModel.query.filter_by(email=email)
        if user.first():
            return True
        else:
            return False

    # Select User from DB (Login)
    @classmethod
    def fetchUser(cls, email, password):
        user = UserModel.query.filter_by(email=email, password=password)
        if user.first():
            return True
        else:
            return False

