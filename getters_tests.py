from db.database import MongoDBConnection

def main():
    mongo = MongoDBConnection()
    if not mongo.connect():
        print("The connection is impossible")
        return

    # 1. récupérer un user via pid
    user = mongo.get_item_by_pid("Users", pid="6dd48a63-3ef8-4039-8b8f-3d37d582e563")
    print(user)

    # 2. récupérer un user via email
    user = mongo.get_item_by_attr("Users", {"email": "thomas@example.com"}, fields=["name"])
    print(user) 

    # 3. récupérer tous les champs de l'user
    user = mongo.get_item_by_attr("Users", {"email": "thomas@example.com"}, fields=[])
    print(user) 

if __name__ == "__main__":
    main()