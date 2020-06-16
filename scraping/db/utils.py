from models import db, Usernames, Techno, Doodle
from sqlalchemy.sql import exists

#label name -> object
labels_dict = {
            "techno": Techno
        }

#account name -> list: account object, labels associated
accounts_dict = {
            "doodlerecords": [Doodle, ["techno"]]
        }

#add username to table associated w/ label
def add_labels(username, labels):
    for label in labels:
        if label in labels_dict.keys():
            l = labels_dict[label](username=username)
            db.session.add(l)
            db.session.commit()
            print(f"label '{label}' added to {username}")
        else:
            print(f"{username} was not added to {label}, label does not exists")

#add user to account table and into appropriate labels' tables
def add_user(username, labels=[]):
    #check if in accounts table
    if (Usernames.query.filter_by(username=username).first() == None):
        user = Usernames(username=username)
        db.session.add(user)
        db.session.commit()
        print(f"{username} added to database")
        add_labels(username, labels)
    else:
        print(f"{username} not added, account already in database")

#add users to account table that have labels associated w/ account
def update_account(account_name):
    #check if acc exists
    if account_name not in accounts_dict.keys():
        print(f"{account_name} does not have table")
        return

    acc = accounts_dict[account_name][0]
    labels = accounts_dict[account_name][1]

    #add all users from labels associated to account to account's table
    #only add if not already in account's table
    for label in labels:
        l = labels_dict[label]
        users = db.session.query(l).filter(~ exists().where(acc.username==l.username)).all()
        for user in users:
            user_obj = acc(username=user.username, state="follow", date=None)
            db.session.add(user_obj)
            db.session.commit()
            print(f"{user.username} added to {account_name}'s table (from label: {label})")

#changes user state (follow, unfollow, done) in account_name's table
def change_state(username, account_name):
    #check if acc exists
    if account_name not in accounts_dict.keys():
        print(f"{account_name} does not have table")
        return

    acc = accounts_dict[account_name][0]
    #todo



"""
    Queries database for people with a birthday on today's date
    Returns dictionary where name is key and age is value
    birthdays = Birthday.query.filter_by(
        month = datetime.today().month,
        day = datetime.today().day
    ).all()

    bds = {}
    for bd in birthdays:
        name = bd.first_name
        if bd.last_name != '':
            name += bd.last_name
        if not bd.year:
            age = ''
        else:
            age = datetime.today().year - bd.year
        bds[name] = age
    return bds;

def add_birthday(first_name, last_name, day, month, year):
    bd = Birthday(first_name=first_name, last_name=last_name,
                    day=day, month=month, year=year
                 )
    db.session.add(bd)
    db.session.commit()

def update_birthday(first_name, last_name, day, month, year):
    bd = Birthday.query.filter_by(first_name=first_name, last_name=last_name).first()
    bd.day = day
    bd.month = month
    bd.year = year
    db.session.commit()
"""

#add_user('jdeeee', ['techno', 'zine'])
#add_user('jorge', ['techno'])

#update_account('doodlerecords')




