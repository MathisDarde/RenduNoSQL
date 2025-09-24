from db.database import MongoDBConnection

def main():
    mongo = MongoDBConnection()
    if not mongo.connect():
        print("The connection is impossible")
        return

    # Ajouter un membre dans team.members
    team_pid = "13345a81-c5a8-49ec-b878-5aa4ed77f7f1"
    member_to_add = {"pid": "6dd48a63-3ef8-4039-8b8f-3d3798f2e563", "name": "Jeremy"}
    modified = mongo.array_push_item_by_pid("Teams", team_pid, "members", member_to_add, updated_by="admin")
    print("Members added:", modified)

    # Supprimer un membre de team.members
    modified = mongo.array_pull_item_by_pid("Teams", team_pid, "members", {"pid": "6dd48a63-3ef8-4039-8b8f-3d3798f2e563"}, updated_by="admin")
    print("Members removed:", modified)

    # Ajouter un tag à un projet
    project_pid = "97981673-f6df-4f32-af1b-022bb93288ac"
    modified = mongo.array_push_item_by_pid("Projects", project_pid, "tags", "urgent", updated_by="admin")
    print("Tag added:", modified)

    # Supprimer un tag spécifique d’un projet spécifique
    modified = mongo.array_pull_item_by_pid("Projects", project_pid, "tags", "urgent", updated_by="admin")
    print("Tag removed:", modified)

    # Supprimer un tag spécifique de tous les projets
    modified = mongo.array_pull_item_by_attr("Projects", {}, "tags", "obsolete", updated_by="admin")
    print("Tags 'obsolete' removed from all projects:", modified)

    mongo.disconnect()

if __name__ == "__main__":
    main()
