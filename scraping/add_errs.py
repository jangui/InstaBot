from db import add_user

#labels = []

with open("errs", 'r') as f:
    for line in f:
        username = line.strip()
        try:
            add_user(username, labels)
        except Exception as e:
            print(f"could not add {username} to db: {e}")
