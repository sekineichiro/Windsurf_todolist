import json
from models.task import Task

class TaskStorage:
    def __init__(self, filename="tasks.json"):
        self.filename = filename

    def save_tasks(self, tasks):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in tasks], f, ensure_ascii=False, indent=2)

    def load_tasks(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Task.from_dict(task_data) for task_data in data]
        except FileNotFoundError:
            return []
