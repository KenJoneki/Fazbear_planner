from datetime import datetime, timedelta
from event import Event

class EventPlanner:
    def __init__(self, events, resources, constraint_manager):
        self.events = events
        self.resources = resources  
        self.constraint_manager = constraint_manager

    def can_schedule_event(self, new_event):
        
        for existing_event in self.events:
            if new_event.overlaps(existing_event):
                
                shared_resources = set(new_event.resources) & set(existing_event.resources)
                if shared_resources:
                    conflict_resources = ", ".join(shared_resources)
                    return False, f"Conflictos con '{existing_event.name}' en recursos: {conflict_resources}"

        
        resource_usage = self._count_resource_usage(new_event.start, new_event.end)
        for resource_name in new_event.resources:
            if resource_name not in self.resources:
                return False, f"Recurso '{resource_name}' no existe"
            
            resource = self.resources[resource_name]
            used_count = resource_usage.get(resource_name, 0)
            if not resource.is_available(used_count):
                return False, f"Recurso '{resource_name}' no disponible (usado {used_count}/{resource.quantity})"

        
        valid, message = self.constraint_manager.check_all_constraints(new_event.resources)
        if not valid:
            return False, f"Restricción violada: {message}"

        return True, ""

    def _count_resource_usage(self, start_time, end_time):
        
        usage = {}
        for event in self.events:
            
            if event.start < end_time and start_time < event.end:
                for resource_name in event.resources:
                    usage[resource_name] = usage.get(resource_name, 0) + 1
        return usage

    def find_next_available_slot(self, event_name, resources, duration_hours):
        
        current_time = datetime.now()
        
        
        for resource_name in resources:
            if resource_name not in self.resources:
                print(f"Recurso '{resource_name}' no encontrado.")
                return None, None
        
        
        for day_offset in range(7):
            day = current_time + timedelta(days=day_offset)
            
            for hour in range(8, 22):
                start_time = day.replace(hour=hour, minute=0, second=0, microsecond=0)
                end_time = start_time + timedelta(hours=duration_hours)
                
                if end_time.hour >= 22:  
                    continue
                
                
                test_event = Event(event_name, start_time, end_time, resources)
                can_schedule, _ = self.can_schedule_event(test_event)
                
                if can_schedule:
                    return start_time, end_time
        
        return None, None

    def add_event(self, event):
        
        can_schedule, message = self.can_schedule_event(event)
        if can_schedule:
            self.events.append(event)
            return True, "Evento programado exitosamente"
        else:
            return False, message

    def remove_event(self, event_index):
        
        if 0 <= event_index < len(self.events):
            removed = self.events.pop(event_index)
            return True, f"Evento '{removed.name}' eliminado"
        return False, "Índice de evento inválido"

    def get_resource_schedule(self, resource_name):
        
        schedule = []
        for event in self.events:
            if event.uses_resource(resource_name):
                schedule.append(event)
        return sorted(schedule, key=lambda e: e.start)
from datetime import datetime, timedelta
from event import Event

class EventPlanner:
    def __init__(self, events, resources, constraint_manager):
        self.events = events  
        self.resources = resources  
        self.constraint_manager = constraint_manager

    def can_schedule_event(self, new_event):
        
        for existing_event in self.events:
            if new_event.overlaps(existing_event):
                
                shared_resources = set(new_event.resources) & set(existing_event.resources)
                if shared_resources:
                    conflict_resources = ", ".join(shared_resources)
                    return False, f"Conflictos con '{existing_event.name}' en recursos: {conflict_resources}"

        
        resource_usage = self._count_resource_usage(new_event.start, new_event.end)
        for resource_name in new_event.resources:
            if resource_name not in self.resources:
                return False, f"Recurso '{resource_name}' no existe"
            
            resource = self.resources[resource_name]
            used_count = resource_usage.get(resource_name, 0)
            if not resource.is_available(used_count):
                return False, f"Recurso '{resource_name}' no disponible (usado {used_count}/{resource.quantity})"

        
        valid, message = self.constraint_manager.check_all_constraints(new_event.resources)
        if not valid:
            return False, f"Restricción violada: {message}"

        return True, ""

    def _count_resource_usage(self, start_time, end_time):
        
        usage = {}
        for event in self.events:
            
            if event.start < end_time and start_time < event.end:
                for resource_name in event.resources:
                    usage[resource_name] = usage.get(resource_name, 0) + 1
        return usage

    def find_next_available_slot(self, event_name, resources, duration_hours):
        
        current_time = datetime.now()
        
        
        for resource_name in resources:
            if resource_name not in self.resources:
                print(f"Recurso '{resource_name}' no encontrado.")
                return None, None
        
        
        for day_offset in range(7):
            day = current_time + timedelta(days=day_offset)
            
            for hour in range(8, 22):
                start_time = day.replace(hour=hour, minute=0, second=0, microsecond=0)
                end_time = start_time + timedelta(hours=duration_hours)
                
                if end_time.hour >= 22:  
                    continue
                
                
                test_event = Event(event_name, start_time, end_time, resources)
                can_schedule, _ = self.can_schedule_event(test_event)
                
                if can_schedule:
                    return start_time, end_time
        
        return None, None

    def add_event(self, event):
        
        can_schedule, message = self.can_schedule_event(event)
        if can_schedule:
            self.events.append(event)
            return True, "Evento programado exitosamente"
        else:
            return False, message

    def remove_event(self, event_index):
        
        if 0 <= event_index < len(self.events):
            removed = self.events.pop(event_index)
            return True, f"Evento '{removed.name}' eliminado"
        return False, "Índice de evento inválido"

    def get_resource_schedule(self, resource_name):
        
        schedule = []
        for event in self.events:
            if event.uses_resource(resource_name):
                schedule.append(event)
        return sorted(schedule, key=lambda e: e.start)