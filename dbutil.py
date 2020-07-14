from pymongo import MongoClient

my_client = MongoClient('mongodb://localhost:27017/')
moyadb = my_client['moya']
users = moyadb['users']

userlist = users.find()

for user in userlist:
    print(user)