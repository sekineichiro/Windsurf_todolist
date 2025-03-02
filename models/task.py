from datetime import datetime

class Task:
    def __init__(self, text, priority="中", completed=False):
        self.text = text
        self.priority = priority
        self.completed = completed
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "text": self.text,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(data["text"])
        task.priority = data["priority"]
        task.completed = data["completed"]
        task.created_at = data["created_at"]
        return task
