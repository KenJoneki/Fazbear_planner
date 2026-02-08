import datetime
from event import Event
from resource import Resource
from constraint import ConstraintManager
from storage import StorageManager
from planner import EventPlanner

class FazbearEventPlanner:
    def __init__(self):
        self.storage = StorageManager()
        self.events, self.resources, self.constraint_manager = self.storage.load()
        self.planner = EventPlanner(self.events, self.resources, self.constraint_manager)
        self.running = True

    def print_menu(self):
        print("\n" + "="*50)
        print("   FAZBEAR'S PIZZA - PLANIFICADOR DE EVENTOS")
        print("="*50)
        print("1. Ver eventos programados")
        print("2. Planificar nuevo evento")
        print("3. Buscar hueco para evento")
        print("4. Eliminar evento")
        print("5. Ver agenda de un recurso")
        print("6. Ver restricciones")
        print("7. Ver recursos disponibles (por categoría)")
        print("8. Guardar y salir")
        print("="*50)

    def run(self):
        while self.running:
            self.print_menu()
            choice = input("\nSeleccione una opción (1-8): ").strip()

            if choice == "1":
                self.show_events()
            elif choice == "2":
                self.schedule_event()
            elif choice == "3":
                self.find_slot()
            elif choice == "4":
                self.remove_event()
            elif choice == "5":
                self.show_resource_schedule()
            elif choice == "6":
                self.show_constraints()
            elif choice == "7":
                self.show_resources_by_category()
            elif choice == "8":
                self.exit_program()
            else:
                print("Opción inválida. Intente nuevamente.")

    def show_events(self):
        print("\n--- EVENTOS PROGRAMADOS ---")
        if not self.events:
            print("No hay eventos programados.")
            return
        
        for i, event in enumerate(self.events):
            print(f"{i+1}. {event}")
            print(f"   Recursos: {', '.join(event.resources)}")
            print()

    def schedule_event(self):
        print("\n--- PLANIFICAR NUEVO EVENTO ---")
        
        name = input("Nombre del evento: ").strip()
        if not name:
            print("El nombre no puede estar vacío.")
            return

        
        self.show_resources_by_category()

        resources_input = input("\nRecursos (separados por coma): ").strip()
        resources = [r.strip() for r in resources_input.split(",") if r.strip()]

        
        missing_resources = [r for r in resources if r not in self.resources]
        if missing_resources:
            print(f"Recursos no encontrados: {', '.join(missing_resources)}")
            return

        
        try:
            date_str = input("Fecha (YYYY-MM-DD): ").strip()
            time_str = input("Hora de inicio (HH:MM): ").strip()
            duration = float(input("Duración (horas): ").strip())
            
            start_time = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            end_time = start_time + datetime.timedelta(hours=duration)
            
            if start_time < datetime.datetime.now():
                print("Error: No se puede programar en el pasado.")
                return
        except ValueError as e:
            print(f"Error en formato de fecha/hora: {e}")
            return

        
        new_event = Event(name, start_time, end_time, resources)
        success, message = self.planner.add_event(new_event)
        
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ Error: {message}")

    def find_slot(self):
        print("\n--- BUSCAR HUECO DISPONIBLE ---")
        
        name = input("Nombre del evento: ").strip()
        
        
        self.show_resources_by_category()

        resources_input = input("\nRecursos necesarios (separados por coma): ").strip()
        resources = [r.strip() for r in resources_input.split(",") if r.strip()]
        
        try:
            duration = float(input("Duración (horas): ").strip())
        except ValueError:
            print("Duración inválida.")
            return

        start, end = self.planner.find_next_available_slot(name, resources, duration)
        
        if start:
            print(f"\n✓ Hueco encontrado:")
            print(f"  Fecha: {start.strftime('%Y-%m-%d')}")
            print(f"  Hora: {start.strftime('%H:%M')} - {end.strftime('%H:%M')}")
            
            schedule = input("\n¿Programar en este horario? (s/n): ").lower()
            if schedule == 's':
                event = Event(name, start, end, resources)
                success, message = self.planner.add_event(event)
                if success:
                    print(f"✓ {message}")
                else:
                    print(f"✗ Error: {message}")
        else:
            print("✗ No se encontró hueco disponible en los próximos 7 días.")

    def remove_event(self):
        self.show_events()
        if not self.events:
            return
        
        try:
            index = int(input("\nNúmero del evento a eliminar: ").strip()) - 1
            success, message = self.planner.remove_event(index)
            print(message)
        except ValueError:
            print("Número inválido.")

    def show_resource_schedule(self):
        print("\n--- AGENDA DE RECURSO ---")
        resource_name = input("Nombre del recurso: ").strip()
        
        if resource_name not in self.resources:
            print("Recurso no encontrado.")
            return
        
        schedule = self.planner.get_resource_schedule(resource_name)
        
        if schedule:
            print(f"\nAgenda de '{resource_name}':")
            for event in schedule:
                print(f"  • {event}")
        else:
            print(f"El recurso '{resource_name}' no tiene eventos programados.")

    def show_constraints(self):
        print("\n" + str(self.constraint_manager))

    def show_resources_by_category(self):
        print("\n--- RECURSOS DISPONIBLES ---")
        
        
        categories = {}
        for resource in self.resources.values():
            if resource.type not in categories:
                categories[resource.type] = []
            categories[resource.type].append(resource)
        
        
        for category in sorted(categories.keys()):
            print(f"\n【{category.upper()}】")
            for resource in sorted(categories[category], key=lambda x: x.name):
                print(f"  • {resource}")

    def exit_program(self):
        self.storage.save(self.events, self.resources, self.constraint_manager)
        print("\n¡Datos guardados! ¡Hasta la próxima!")
        self.running = False

if __name__ == "__main__":
    app = FazbearEventPlanner()
    app.run()