from uuid import uuid4
from datetime import datetime, timedelta
from random import choice, randint
from db.database import MongoDBConnection

mongo = MongoDBConnection()
if not mongo.connect():
    print("Impossible de se connecter à MongoDB")
    exit()

def generate_user(name, email, role="user", created_by=None):
    now = datetime.now()
    user = {
        "pid": str(uuid4()),
        "name": name,
        "email": email,
        "role": role,
        "created_at": now,
        "updated_at": now
    }
    if created_by:
        user["created_by"] = created_by
    return user

def generate_team(name, members, created_by=None):
    now = datetime.now()
    team = {
        "pid": str(uuid4()),
        "name": name,
        "members": members,
        "created_at": now,
        "updated_at": now
    }
    if created_by:
        team["created_by"] = created_by
    return team

def generate_project(name, teams, tags, budget, deadline, created_by=None):
    now = datetime.now()
    project = {
        "pid": str(uuid4()),
        "name": name,
        "teams": teams,
        "tags": tags,
        "budget": budget,
        "deadline": deadline,
        "created_at": now,
        "updated_at": now
    }
    if created_by:
        project["created_by"] = created_by
    return project

def seed():
    print("Seeding database...")

    user_data = [
        ("Thomas", "thomas@example.com", "admin"),
        ("Ilyan", "ilyan@example.com", "user"),
        ("Mila", "mila@example.com", "user"),
        ("Yohan", "yohan@example.com", "user")
    ]
    users = [generate_user(*u, created_by="seeder") for u in user_data]
    user_ids = mongo.create_items("Users", users, created_by="seeder")
    print(f"{len(user_ids)} users created")

    team_names = ["Team1", "Team2", "Team3"]
    teams = []
    for name in team_names:
        members = [choice(user_ids) for _ in range(randint(1, len(user_ids)))]
        teams.append(generate_team(name, members, created_by="seeder"))
    team_ids = mongo.create_items("Teams", teams, created_by="seeder")
    print(f"{len(team_ids)} teams created")

    project_names = ["Project A", "Project B", "Project C"]
    tags_pool = ["Dev", "Crea", "Com", "JV", "3D"]
    projects = []
    for name in project_names:
        project_teams = [choice(team_ids) for _ in range(randint(1, len(team_ids)))]
        tags = [choice(tags_pool) for _ in range(randint(1, 3))]
        budget = randint(5000, 50000)
        deadline = datetime.now() + timedelta(days=randint(30, 180))
        projects.append(generate_project(name, project_teams, tags, budget, deadline, created_by="seeder"))
    project_ids = mongo.create_items("Projects", projects, created_by="seeder")
    print(f"{len(project_ids)} projects created")

    print("Seeding completed ✅")

if __name__ == "__main__":
    seed()
