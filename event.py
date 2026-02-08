import datetime

class Event:
    def __init__(self, name: str, start: datetime.datetime, end: datetime.datetime, resources: list):
        self.name = name
        self.start = start
        self.end = end
        self.resources = resources  

    def overlaps(self, other_event) -> bool:
        
        return self.start < other_event.end and other_event.start < self.end

    def uses_resource(self, resource_name: str) -> bool:
        
        return resource_name in self.resources

    def to_dict(self):
        
        return {
            "name": self.name,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "resources": self.resources
        }

    @classmethod
    def from_dict(cls, data):
        
        return cls(
            name=data["name"],
            start=datetime.datetime.fromisoformat(data["start"]),
            end=datetime.datetime.fromisoformat(data["end"]),
            resources=data["resources"]
        )

    def __str__(self):
        return f"{self.name} ({self.start.strftime('%Y-%m-%d %H:%M')} - {self.end.strftime('%H:%M')})"