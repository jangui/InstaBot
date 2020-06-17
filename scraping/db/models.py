from .app import db

"""
The accounts tables keeps names of all accounts
accounts can be labeled as interested in subjects by being a foreign key in that subjects table i.e techno

When using the database for a specific account, it is required to know what followers have been already followed,
need to be followed, or should be unfollowed. This information is kept in one table for that account. i.e. Doodle
    info stored: usename, state (follow, unfollow, done), date (used to keep track when to unfollow accs)

"""

#All accounts
class Usernames(db.Model):
    def __init__(self, **kwargs):
        super(Usernames, self).__init__(**kwargs)

    __tablename__ = 'usernames'
    username = db.Column(db.String(30), index=True, nullable=False, primary_key=True)

#Label
class Techno(db.Model):
    def __init__(self, **kwargs):
        super(Techno, self).__init__(**kwargs)

    __tablename__ = 'techno'
    username = db.Column(db.String(30), db.ForeignKey('usernames.username'), index=True, nullable=False, primary_key=True)

# @doodlerecords info
class Doodle(db.Model):
    def __init__(self, **kwargs):
        super(Doodle, self).__init__(**kwargs)

    __tablename__ = 'doodle'
    username = db.Column(db.String(30), db.ForeignKey('usernames.username'), index=True, nullable=False, primary_key=True)
    state = db.Column(db.String(8), index=True, nullable=False)
    date = db.Column(db.String(10))

#create tables
if __name__ == "__main__":
    db.create_all()
