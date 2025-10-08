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
    
    async def camera_access(self, camera_id: int, game: Game):
        for camera in game.cameras:
            if camera.camera_id == camera_id:
                return camera.feed
        return f"Camera {camera_id} not found"
    
    async def read_register(self, folder_name: str, game: Game):
        for folder in game.registers:
            if folder.name == folder_name:
                return folder.contents
        return f"Folder {folder_name} not found"
    
    async def read_patient_record(self, patient: Patient, game: Game):
        patient_data = {
            "Name": patient.name,
            "Age": patient.age,
            "Symptoms": patient.symptoms,
            "Diagnosis": patient.diagnosis,
            "Medications": patient.medications,
            "Allergies": patient.allergies,
            "Notes": patient.notes
        }
        return patient_data


class Coordinator(Role):
    def __init__(self):
        super().__init__("Coordinator")
        self.register_action("Coordinate Team", self.coordinate_team)
        self.register_action("Organize Resources", self.organize_resources)
    
    async def take_decision(self, decision: str, game: Game):
        game.decisions.append(decision)