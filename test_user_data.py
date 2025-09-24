from db.database import MongoDBConnection

def main():
    mongo = MongoDBConnection()
    if not mongo.connect():
        print("The connection is impossible")
        return
    
    # --- Test 1 : créer 1 user ---
    user = {"name": "Mathis", "email": "mathis@gmail.com"}
    user_id = mongo.create_item("users", user, created_by="admin")  # <-- ici
    print("User ID créé :", user_id)

    # --- Test 2 : créer plusieurs users ---
    users = [
        {"name": "Thierry", "email": "thierry@example.com"},
        {"name": "Jean", "email": "jean@example.com"}
    ]
    user_ids = mongo.create_items("users", users, created_by="admin")
    print("Users IDs créés :", user_ids)

if __name__ == "__main__":
    main()
