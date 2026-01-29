class ConstraintManager:
    def __init__(self):
        self.requires = []  
        self.excludes = [] 

    def add_requirement(self, resource_a: str, resource_b: str):
        
        self.requires.append((resource_a, resource_b))

    def add_exclusion(self, resource_a: str, resource_b: str):
        
        self.excludes.append((resource_a, resource_b))

    def check_all_constraints(self, resources: list) -> (bool, str):
        
        for req_a, req_b in self.requires:
            if req_a in resources and req_b not in resources:
                return False, f"El recurso '{req_a}' requiere también '{req_b}'"
            if req_b in resources and req_a not in resources:
                return False, f"El recurso '{req_b}' requiere también '{req_a}'"

        
        for excl_a, excl_b in self.excludes:
            if excl_a in resources and excl_b in resources:
                return False, f"Los recursos '{excl_a}' y '{excl_b}' no pueden usarse juntos"

        return True, ""

    def load_from_dict(self, constraints_dict: dict):
        
        self.requires = constraints_dict.get("requires", [])
        self.excludes = constraints_dict.get("excludes", [])

    def to_dict(self):
        
        return {
            "requires": self.requires,
            "excludes": self.excludes
        }

    def __str__(self):
        result = "Restricciones:\n"
        if self.requires:
            result += "  Co-requisitos:\n"
            for a, b in self.requires:
                result += f"    - {a} requiere {b}\n"
        if self.excludes:
            result += "  Exclusiones:\n"
            for a, b in self.excludes:
                result += f"    - {a} y {b} no pueden usarse juntos\n"
        return result