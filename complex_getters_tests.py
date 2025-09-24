from db.database import MongoDBConnection

def main():
    mongo = MongoDBConnection()
    if not mongo.connect():
        print("The connection is impossible")
        return

    # 1. Récupérer tous les projets d’un user triés par deadline
    user_pid = "6dd48a63-3ef8-4039-8b8f-3d3798f2e563"
    projects, stats = mongo.get_items(
        "Projects",
        {"teams": user_pid},
        fields=["name", "deadline"],
        sort={"deadline": 1},
        return_stats=True
    )
    print("Projects for user:", projects)
    print("Stats:", stats)

    # 2. Pagination sur les users (2 par page)
    page = 1
    users, stats = mongo.get_items(
        "Users",
        {},
        fields=["name", "role"],
        sort={"name": 1},
        skip=(page-1)*2,
        limit=2,
        return_stats=True
    )
    print("Page 1 users:", users)
    print("Stats:", stats)

    # 3. Compter le nombre de projets avec tag="urgent"
    urgent_projects = mongo.get_items(
        "Projects",
        {"tags": "urgent"}
    )
    print("Number of urgent projects:", len(urgent_projects))

    mongo.disconnect()

if __name__ == "__main__":
    main()