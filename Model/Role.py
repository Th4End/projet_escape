from Model.Entity import Patient, Zone, Game

class Role:
    def __init__(self, name: str):
        self.name = name
        self.actions = {}
    
    def register_action(self, action: str, func):
        self.actions[action] = func
    
    def can_do(self, action_name):
        return action_name in self.actions
    
    async def do(self, action_name, *args, **kwargs):
        if self.can_do(action_name):
            return await self.actions[action_name](*args, **kwargs)
        else:
            raise PermissionError(f"Action '{action_name}' is not permitted for this role.")
        
class Doctor(Role):
    def __init__(self):
        super().__init__("Doctor")
        self.register_action("make_diagnosis", self.make_diagnosis)
        self.register_action("Read Patient Record", self.read_patient_record)
        self.register_action("Prescribe Medication", self.prescribe_medication)

    async def make_diagnosis(self, patient: Patient, game: Game):
        if game.ressources["tests"] <= 0:
            return "No tests available"
        game.ressources["tests"] -= 1
        patient.tests.append("diagnosis")
        return "Diagnosis made on the patient"

    async def prescribe_medication(self, patient: Patient, medication: str):
        patient.medications.append(medication)
        return f"Prescribed {medication} to {patient.name}"

class Tour_Guide(Role):
    def __init__(self):
        super().__init__("Tour Guide")
        self.register_action("Conduct Tour", self.conduct_tour)

    async def conduct_tour(self, zone_dest: Zone, game: Game):
        for zone in game.zones:
            if zone.name == zone_dest.name:
                if zone.is_accessible:
                    return f"Tour conducted to {zone.name}"
                else:
                    return f"Zone {zone.name} is not accessible"
            else:
                return f"Zone {zone_dest.name} not found"
        

class Analyst(Role):
    def __init__(self):
        super().__init__("Analyst")
        self.register_action("Camera Access", self.camera_access)
        self.register_action("Read Folders", self.read_folders)
        self.register_action("Read Patient Record", self.read_patient_record)
    
    async def camera_access(self, camera_id: int, game: Game):
        try:
            if game.ressources.get("camera_access", 0) <= 0:
                return "No camera access available"
            
            for camera in game.cameras:
                if camera.camera_id == camera_id:
                    game.ressources["camera_access"] -= 1
                    return camera.feed
            return f"Camera {camera_id} not found"
        except Exception as e:
            return f"Error accessing camera: {e}"
    
    async def read_folders(self, folder_name: str, game: Game):
        try:
            if game.ressources.get("client_register", 0) <= 0:
                return "No client register access available"
            
            for folder in game.client_registers:
                if folder.name == folder_name:
                    game.ressources["client_register"] -= 1
                    return folder.content
            return f"Folder {folder_name} not found"
        except Exception as e:
            return f"Error reading folders: {e}"
    
    async def read_patient_record(self, patient: Patient, game: Game):
        try:
            if game.ressources.get("medical_folders", 0) <= 0:
                return "No medical folders available"

            game.ressources["medical_folders"] -= 1
            return {
                "Name": patient.name,
                "Age": patient.age,
                "Symptoms": patient.symptoms,
                "Diagnosis": patient.diagnosis,
                "Medications": patient.medications,
                "Allergies": patient.allergies,
                "Notes": patient.notes
            }
        except Exception as e:
            return f"Error reading patient record: {e}"


class Coordinator(Role):
    def __init__(self):
        super().__init__("Coordinator")
        self.register_action("Coordinate Team", self.coordinate_team)
        self.register_action("Organize Resources", self.organize_resources)
        
    async def coordinate_team(self, game: Game, message: str=''):
        try:
            if not hasattr(game, 'decisions'):
                game.decisions = []
            game.decisions.append({"from": self.name, "message":message })
            return f"Team coordinated with message: {message}"
        except Exception as e:
            return f"Error coordinating team: {e}"
        
    async def organize_resources(self, game: Game, resource: str, amount: int):
        try:
            if resource not in game.ressources:
                return f"Resource {resource} not found"
            
            game.ressources[resource] = game.ressources.get(resource, 0) + amount
            return f"Organized {amount} of {resource}"
        except Exception as e:
            return f"Error organizing resources: {e}"