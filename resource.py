class Resource:
    def __init__(self, name: str, resource_type: str, quantity: int = 1):
        self.name = name
        self.type = resource_type  
        self.quantity = quantity  
        self.max_quantity = quantity

    def is_available(self, used_count: int) -> bool:
        return used_count < self.quantity

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "quantity": self.quantity
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            resource_type=data["type"],
            quantity=data.get("quantity", 1)
        )

    def __str__(self):
        return f"{self.name} ({self.type})" + (f" x{self.quantity}" if self.quantity > 1 else "")