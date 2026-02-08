import json
import os
from event import Event
from resource import Resource
from constraint import ConstraintManager

class StorageManager:
    def __init__(self, filename="fazbear_data.json"):
        self.filename = filename

    def save(self, events, resources, constraint_manager):
        
        data = {
            "resources": [r.to_dict() for r in resources.values()],
            "events": [e.to_dict() for e in events],
            "constraints": constraint_manager.to_dict()
        }
        
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Datos guardados en {self.filename}")

    def load(self):
        
        if not os.path.exists(self.filename):
            print(f"Archivo {self.filename} no encontrado. Creando datos iniciales...")
            return self.create_default_data()

        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        
        resources = {}
        for r_data in data.get("resources", []):
            resource = Resource.from_dict(r_data)
            resources[resource.name] = resource

        
        events = []
        for e_data in data.get("events", []):
            events.append(Event.from_dict(e_data))

        
        constraint_manager = ConstraintManager()
        constraint_manager.load_from_dict(data.get("constraints", {}))

        print(f"Datos cargados desde {self.filename}")
        return events, resources, constraint_manager

    def create_default_data(self):
        
        
        resources = {}
        
        
        animatronics = [
            ("Freddy Fazbear", "animatronic", 1),
            ("Bonnie la Guitarra", "animatronic", 1),
            ("Chica la Pollo", "animatronic", 1),
            ("Foxy el Pirata", "animatronic", 1),
            ("Golden Freddy", "animatronic", 1)
        ]
        
        
        rooms = [
            ("Escenario Principal", "room", 1),
            ("Sala de Mantenimiento", "room", 1),
            ("Cocina", "room", 1),
            ("Pasillo Este", "room", 1),
            ("Almacén", "room", 1)
        ]
        
        
        equipment = [
            ("Traje de Asistente (Springlock)", "equipment", 1),
            ("Kit de Herramientas", "equipment", 3),
            ("Cámara de Seguridad", "equipment", 4),
            ("Sistema de Audio", "equipment", 1)
        ]
        
        
        staff = [
            ("Técnico Nocturno", "staff", 2),
            ("Guardia de Seguridad", "staff", 1)
        ]
        
        
        all_resources = animatronics + rooms + equipment + staff
        for name, r_type, quantity in all_resources:
            resource = Resource(name, r_type, quantity)
            resources[name] = resource
        
        
        constraint_manager = ConstraintManager()
        
        constraint_manager.add_requirement("Traje de Asistente (Springlock)", "Técnico Nocturno")
        constraint_manager.add_requirement("Freddy Fazbear", "Chica la Pollo")
        constraint_manager.add_requirement("Freddy Fazbear", "Bonnie la Guitarra")
        constraint_manager.add_requirement("Cámara de Seguridad", "Guardia de Seguridad")
        constraint_manager.add_requirement("Cámara de Seguridad", "Técnico Nocturno")
        
        
        constraint_manager.add_exclusion("Golden Freddy", "Freddy Fazbear")
        constraint_manager.add_exclusion("Traje de Asistente (Springlock)", "Cocina")
        constraint_manager.add_exclusion("Foxy el Pirata", "Sala de Mantenimiento")
        constraint_manager.add_exclusion("Traje de Asistente (Springlock)", "Guardia de Seguridad")
        constraint_manager.add_exclusion("Cocina", "Sistema de Audio")
        
        
        events = []
        
        print("Datos iniciales creados correctamente.")
        return events, resources, constraint_manager