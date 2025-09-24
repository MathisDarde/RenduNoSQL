from db.database import MongoDBConnection

def main():
    mongo = MongoDBConnection()
    if not mongo.connect():
        print("The connection is impossible")
        return

    users = mongo.get_collection("Users")

    first_user = users.find_one({})
    pid = first_user["pid"]

    # --- Test 1 : modifier le name via pid ---
    mongo.update_item_by_pid("Users", pid, {"name": "Thomas Updated"}, updated_by="admin")
    u1 = users.find_one({"pid": pid})
    print("Name after update:", u1["name"], "Updated_at:", u1["updated_at"], "Updated_by:", u1["updated_by"])

    # --- Test 2 : modifier tous les users avec un rôle particulier ---
    mongo.update_items_by_attr("Users", {"role": "tester"}, {"role": "developer"}, updated_by="admin")
    for u in users.find({"role": "developer"}):
        print("Updated role:", u["name"], "->", u["role"], "Updated_at:", u["updated_at"])

    # --- Test 3 : vérifier que updated_at change à chaque update ---
    before = u1["updated_at"]
    mongo.update_item_by_pid("Users", pid, {"name": "Thomas Final"}, updated_by="superadmin")
    after = users.find_one({"pid": pid})["updated_at"]
    print("Updated_at changed?", before != after, "New Updated_at:", after)

if __name__ == "__main__":
    main()