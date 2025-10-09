from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from Model.Users import User
from Model.Team import Team
from Model.Entity import *
from Model.Role import *

app = FastAPI()

USERS: List[User] = []
TEAMS: List[Team] = []

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    
class LoginRequest(BaseModel):
    username: str
    password: str
    
class CreateTeamRequest(BaseModel):
    name: str
    
class AddMemberRequest(BaseModel):
    username: str
    role_name: str = None
    
class AssignRoleRequest(BaseModel):
    username: str
    role_name: str
    

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/register")
def register_user(data: RegisterRequest):
    try:
        if any(u.username == data.username for u in USERS):
            return {"message": "Username already exists"}
        
        user = User()
        user.create_user(data.username, data.email, data.password)
        USERS.append(user)
        
        return {"Message": f"User '{data.username}' registered successfully."}
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/login")
def login_user(data: LoginRequest):
    try:
        user = next((u for u in USERS if u.username == data.username), None)
        if not user:
            return {"error": "User not found"}
        
        if user.connect(data.password, data.username):
            return {"message": f"User '{data.username}' logged in successfully."}
        else:
            return {"error": "Invalid credentials"}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/users")
def get_user():
    try:
        return {
            "users": [
                {
                    "username": user.username,
                    "email": user.email,
                    "password_hash": user.password_hash
                }
                for user in USERS
            ]
    }
    except Exception as e:
        return {"error": str(e)}

@app.get("/users/{username}")
def get_user(username: str):
    try:
        user = next((u for u in USERS if u.username == username), None)
        if not user:
            return {"error": "User not found."}
        return {
            "username": user.username,
            "email": user.email,
            "password_hash": str(user.password_hash)
        }
    except Exception as e:
        return {"error": str(e)}
        
@app.delete("/reset")
def reset_data():
    USERS.clear()
    TEAMS.clear()
    return {"message": "All data has been reset."}



@app.post("/teams")
def create_team(data: CreateTeamRequest):
    try:
        if any(t.name == data.name for t in TEAMS):
            return {"message": "Team name already exists"}
        
        team = Team(data.name)
        TEAMS.append(team)
        return {"message": f"Team '{data.name}' created successfully."}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/teams")
def get_teams():
    try:
        return {"teams": [t.name for t in TEAMS]}
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/teams/{team_name}/members")
def add_member_to_team(team_name: str, data: AddMemberRequest):
    try:
        team = next((t for t in TEAMS if t.name == team_name), None)
        if not team:
            return {"error": "Team not found"}
        
        user = next((u for u in USERS if u.username == data.username), None)
        if not user:
            return {"error": "User not found"}
        
        result = team.add_member(user, data.role_name)
        return {"message": result}
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/teams/{team_name}/assign_role")
def assign_role_to_member(team_name: str, data: AssignRoleRequest):
    try:
        team = next((t for t in TEAMS if t.name == team_name), None)
        if not team:
            return {"error": f"Team '{team_name}' not found"}
        
        player = next((p for p in team.members if p.username == data.username), None)
        if not player:
            return {"error": f"Player ({data.username}) not found in team '{team_name}'"}
        
        if any(p.current_role and p.current_role.name == data.role_name for p in team.members):
            return {"error": f"Role '{data.role_name}' is already taken in team '{team_name}'"}
        
        result = player.select_role(data.role_name)
        if not isinstance(result, str):
            return {"message": f"Role '{result.name}' assigned to '{player.username}' successfully."}
        else:
            return {"error": result}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/teams/{team_name}/members")
def get_team_members(team_name: str):
    try:
        team = next((t for t in TEAMS if t.name == team_name), None)
        if not team:
            return {"error": "Team not found"}
        
        return {
            "members": [
                {
                    "username": member.username,
                    "role": member.current_role.name if member.current_role else None
                }
                for member in team.members
            ]
        }
    except Exception as e:
        return {"error": str(e)}
    
@app.delete("/teams/{team_name}/members/{username}")
def remove_member_from_team(team_name: str, username: str):
    try:
        team = next((t for t in TEAMS if t.name == team_name), None)
        if not team:
            return {"error": "Team not found"}
        
        player = next((p for p in team.members if p.username == username), None)
        if not player:
            return {"error": "Player not found in team"}
        
        team.members.remove(player)
        return {"message": f"Player '{username}' removed from team '{team_name}'"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/game/zones")
def list_zones(game: Game):
    try:
        return {name: zone.is_accessible for name, zone in game.zones.items()}
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/game/zones/{zone_name}/access")
def access_zone(player_username: str, zone_name: str, game: Game):
    try:
        player = next((u for u in USERS if u.username == player_username), None)
        if not player:
            return {"error": "Player not found"}
        result = game.access_zone(player, zone_name)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/game/patients/{patient_name}")
def read_patient_record(player_username: str, patient_name: str, game: Game):
    try:
        player = next((u for u in USERS if u.username == player_username), None)
        if not player:
            return {"error": "Player not found"}
        return game.read_patient_record(player, patient_name)
    except Exception as e:
        return {"error": str(e)}



