words = ['cat', 'window', 'defenestrate']
for w in words:
    print(w, len(w))

users = {'Hans': 'active', 'Éléonore': 'inactive', '景太郎': 'active'}
active_users = {}
for user, status in users.items():
    if status == 'active':
        active_users[user] = status