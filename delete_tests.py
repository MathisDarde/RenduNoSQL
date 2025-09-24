from db.database import MongoDBConnection

def main():
    mongo = MongoDBConnection()
    if not mongo.connect():
        print("The connection is impossible")
        return
    
    users = mongo.get_collection("Users")
    teams = mongo.get_collection("Teams")

    # --- Test 1 : supprimer 1 user par pid ---
    user = users.find_one({})
    if user:
        deleted = mongo.delete_item_by_pid("Users", user["pid"])
        print("Deleted 1 user by pid:", deleted)

    # --- Test 2 : supprimer tous les users avec rôle "tester" ---
    deleted = mongo.delete_items_by_attr("Users", {"role": "tester"})
    print("Deleted users with role 'tester':", deleted)

    # --- Test 3 : supprimer une team entière ---
    team = teams.find_one({})
    if team:
        deleted = mongo.delete_item_by_pid("Teams", team["pid"])
        print("Deleted team:", deleted)
        members_pids = team.get("members", [])
        remaining_members = list(users.find({"pid": {"$in": members_pids}}))
        print("Remaining members count:", len(remaining_members))

    mongo.disconnect()

if __name__ == "__main__":
    main()