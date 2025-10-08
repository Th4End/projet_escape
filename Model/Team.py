from Entity import *
from Role import *
from Users import *

class Team:
    def __init__(self, name):
        self.team_id = id(self)
        self.name = name
        self.members = []
        self.current_game = None
        self.status = "waiting"
        self.score = 0
        
    def add_member(self, user, role_name: str = None):
        if self.is_full():
            return "Team is full"
        
        player = Player(user.username, self.name)
        
        if role_name:
            player.select_role(role_name)
        
        self.members.append(player)
        return f"Player {user.username} added to team {self.name}."
    
    def remove_member(self, username: str):
        self.members = [m for m in self.members if m.username != username]
        
    def is_full(self):
        return len(self.members) >= 4
    
    def assign_roles(self):
        available_roles = ["Doctor", "Tour Guide", "Analyst", "Coordinator"]
        for player, role_name in zip(self.members, available_roles):
            player.select_role(role_name)
        return "Roles assigned successfully."
    
    def start_game(self):
        if not self.is_full():
            return "Not enough members to start the game."
        
        self.current_game = Game()
        self.assign_roles()
        self.status = "in_progress"
        return f"Game started successfully for team {self.name}."
    
    def end_game(self):
        self.status = "completed"
        return f"Game over for team {self.name}."