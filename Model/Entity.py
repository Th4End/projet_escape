from Model.Role import Doctor, Role, Tour_Guide, Analyst
from Users import User

class Entity:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

    def register_entity(self, entity_name, entity):
        self.attributes[entity_name] = entity
    
    def get_entity(self, entity_name):
        return self.attributes.get(entity_name, None)
    
class Patient(Entity):
    def __init__(self, name, age, symptoms=None, diagnosis=None, medications=None, allergies=None, notes=None):
        super().__init__(name, {
            "age": age,
            "symptoms": symptoms if symptoms else [],
            "diagnosis": diagnosis if diagnosis else "",
            "medications": medications if medications else [],
            "allergies": allergies if allergies else [],
            "notes": notes if notes else ""
        })

class Zone(Entity):
    def __init__(self, name, is_accessible=True, zone_dest=None, game=None):
        super().__init__(name, {
            "is_accessible": is_accessible
        })
        self.is_accessible = is_accessible
        return f"Zone {zone_dest.name} not found in game"

class Symptom(Entity):
    def __init__(self):
        self.information = {
            "is_contagious": True,
            "severity": "high",
            "common_treatments": ["rest", "hydration", "medication", "quarantine"],
            "description": {
                "cough": "A sudden, forceful hacking sound to release air and clear irritation in the throat or airway.",
                "fever": "An abnormally high body temperature, usually accompanied by shivering, headache, and in severe instances, delirium.",
                "headache": "A continuous pain in the head.",
                "fatigue": "Extreme tiredness resulting from mental or physical exertion or illness.",
                "nausea": "A feeling of sickness with an inclination to vomit."
            }
        }

class Medication(Entity):
    def __init__(self):
        self.information = {
            "name": ["Paracetamol", "Ibuprofen", "Amoxicillin", "Azithromycin"],
            "dosage": str,
            "description": {
                "Paracetamol": "Used to treat pain and fever.",
                "Ibuprofen": "Nonsteroidal anti-inflammatory drug (NSAID) used for pain relief.",
                "Amoxicillin": "Antibiotic used to treat bacterial infections.",
                "Azithromycin": "Antibiotic used for various types of infections."
            }
        }

class Player(Entity):
    def __init__(self):
        self.roles = {
            "Doctor": Doctor(),
            "Tour Guide": Tour_Guide(),
            "Analyst": Analyst()
        }
        self.username = User.username
        self.current_role = None

        self.attributes = {
            "roles": self.roles,
            "current_role": self.current_role,
            "username": self.username,
            "score": 0,
            "team_score": 0,
            "team_name": User.team_name
            }
        

    def select_role(self, role_name):
        if self.current_role is None:
            self.current_role = self.roles.get(role_name, None)
            return self.current_role
        else:
            return f"Role already selected: {self.current_role.name}"

class Game(Entity):
    def __init__(self):
        accessible=True 
        self.patients = {
            "p1": Patient("John Doe", 30, ["cough", "fever"]),
            "p2": Patient("Jane Smith", 25, ["headache"]),
            "p3": Patient("Alice Johnson", 40, ["fatigue", "nausea"])
        }
        self.zones = {
            "z1": Zone("Hotel", accessible= True),
            "z2": Zone("Security", accessible= False),
            "z3": Zone("Infirmary", accessible= True),
        }

        self.ressources = {
            "tests": 6,
            "medications": 10,
            "map": 1,
            "medical_folders": 3,
            "camera_access": 1,
            "radio": 3,
            "registration_list": 1,
            "masks": 4,
            "gloves": 1,
            "infirmary_keys": 1,
            "security_keys": 1,
            "hotel_keys": 1
        }

        self.cameras = {
            "c1": {"camera_id": 1, "Hotel": "Hotel Camera Feed"},
            "c2": {"camera_id": 2, "Security": "Security Camera Feed"},
            "c3": {"camera_id": 3, "Infirmary": "Infirmary Camera Feed"}
        }
    
    def access_camera(self, camera_id):
        try:
            if self.ressources["camera_access"] <= 0:
                return "No camera access available"
            for camera in self.cameras.values():
                if camera["camera_id"] == camera_id and self.ressources["camera_access"] > 0:
                    return camera
            return None
        except Exception as e:
            return f"Error accessing camera: {e}"

    def access_zone(self, zone_name):
        try:
            if Role == "Doctor" and zone_name == "Infirmary" and self.ressources["infirmary_keys"] > 0:
                z3 = self.zones["z3"]
                z3.is_accessible = True
                return z3
            if Role == "Tour Guide" and zone_name == "Hotel" and zone_name == "Security" and zone_name == "Infirmary" and self.ressources["hotel_keys"] > 0 and self.ressources["security_keys"] > 0 and self.ressources["infirmary_keys"] > 0:
                z1 = self.zones["z1"]
                z2 = self.zones["z2"]
                z3 = self.zones["z3"]
                z1.is_accessible = True
                z2.is_accessible = True
                z3.is_accessible = True
                return z1, z2, z3
            if Role == "Analyst" and zone_name == "Security" and self.ressources["security_keys"] > 0:
                z2 = self.zones["z2"]
                z2.is_accessible = True
                return z2
            else:
                return f"Zone {zone_name} access denied"
        except Exception as e:
            return f"Error accessing zone: {e}"
    
    def read_patient_record(self, patient_name):
        try:
            patient = self.patients.get(patient_name)
            if patient and Role == "Analyst":
                for patient_folder in self.ressources["medical_folders"]:
                    if patient_folder > 0:
                        return {
                            "Name": patient.name,
                            "Age": patient.attributes["age"],
                            "Symptoms": patient.attributes["symptoms"],
                            "Diagnosis": patient.attributes["diagnosis"],
                    "Medications": patient.attributes["medications"],
                    "Allergies": patient.attributes["allergies"],
                    "Notes": patient.attributes["notes"]
                }
            else:
                return f"Patient {patient_name} not found"
        except Exception as e:
            return f"Error reading patient record: {e}"
    
