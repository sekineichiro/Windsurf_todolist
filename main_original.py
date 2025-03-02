import tkinter as tk
from tkinter import ttk, messagebox
import json
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

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todoリスト")
        self.root.geometry("500x600")
        
        self.tasks = []
        self.load_tasks()

        # タスク入力フレーム
        input_frame = ttk.Frame(root, padding="5")
        input_frame.pack(fill=tk.X)

        self.task_input = ttk.Entry(input_frame)
        self.task_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.priority_var = tk.StringVar(value="中")
        priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var, 
                                    values=["高", "中", "低"], width=5, state="readonly")
        priority_combo.pack(side=tk.LEFT, padx=(0, 5))
        
        add_button = ttk.Button(input_frame, text="追加", command=self.add_task)
        add_button.pack(side=tk.RIGHT)

        # タスクリスト
        self.task_list = ttk.Treeview(root, columns=("Priority", "Status", "Task"), 
                                    show="headings", selectmode="browse")
        self.task_list.heading("Priority", text="優先度")
        self.task_list.heading("Status", text="状態")
        self.task_list.heading("Task", text="タスク内容")
        self.task_list.column("Priority", width=70)
        self.task_list.column("Status", width=70)
        self.task_list.column("Task", width=300)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ボタンフレーム
        button_frame = ttk.Frame(root, padding="5")
        button_frame.pack(fill=tk.X)

        complete_button = ttk.Button(button_frame, text="完了/未完了", command=self.toggle_complete)
        complete_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        edit_button = ttk.Button(button_frame, text="編集", command=self.edit_task)
        edit_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        delete_button = ttk.Button(button_frame, text="削除", command=self.delete_task)
        delete_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # エンターキーでタスクを追加
        self.task_input.bind('<Return>', lambda e: self.add_task())
        
        # 初期表示
        self.refresh_task_list()

    def add_task(self):
        task_text = self.task_input.get().strip()
        if task_text:
            task = Task(task_text, self.priority_var.get())
            self.tasks.append(task)
            self.task_input.delete(0, tk.END)
            self.save_tasks()
            self.refresh_task_list()
        else:
            messagebox.showwarning("警告", "タスクを入力してください。")

    def toggle_complete(self):
        selected_id = self.task_list.selection()
        if selected_id:
            index = self.get_task_index(selected_id[0])
            self.tasks[index].completed = not self.tasks[index].completed
            self.save_tasks()
            self.refresh_task_list()
        else:
            messagebox.showwarning("警告", "タスクを選択してください。")

    def edit_task(self):
        selected_id = self.task_list.selection()
        if not selected_id:
            messagebox.showwarning("警告", "編集するタスクを選択してください。")
            return

        index = self.get_task_index(selected_id[0])
        task = self.tasks[index]

        # 編集ウィンドウを作成
        edit_window = tk.Toplevel(self.root)
        edit_window.title("タスクの編集")
        edit_window.geometry("400x250")
        
        # メインフレーム（パディング付き）
        main_frame = ttk.Frame(edit_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # タスク内容入力エリア
        task_frame = ttk.Frame(main_frame)
        task_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(task_frame, text="タスク内容:", font=("", 10)).pack(anchor=tk.W, pady=(0, 5))
        edit_entry = ttk.Entry(task_frame, width=50)
        edit_entry.insert(0, task.text)
        edit_entry.pack(fill=tk.X)

        # 優先度選択エリア
        priority_frame = ttk.Frame(main_frame)
        priority_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(priority_frame, text="優先度:", font=("", 10)).pack(anchor=tk.W, pady=(0, 5))
        priority_var = tk.StringVar(value=task.priority)
        priority_combo = ttk.Combobox(priority_frame, textvariable=priority_var,
                                    values=["高", "中", "低"], state="readonly", width=10)
        priority_combo.pack(anchor=tk.W)

        def save_edit():
            new_text = edit_entry.get().strip()
            if new_text:
                task.text = new_text
                task.priority = priority_var.get()
                self.save_tasks()
                self.refresh_task_list()
                edit_window.destroy()
            else:
                messagebox.showwarning("警告", "タスク内容を入力してください。")

        # ボタンエリア
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        save_button = ttk.Button(button_frame, text="保存", command=save_edit, width=15)
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="キャンセル", command=edit_window.destroy, width=15)
        cancel_button.pack(side=tk.LEFT, padx=5)

        # ウィンドウを親の中央に配置
        edit_window.transient(self.root)
        edit_window.grab_set()
        self.root.eval(f'tk::PlaceWindow {str(edit_window)} center')

    def delete_task(self):
        selected_id = self.task_list.selection()
        if selected_id:
            if messagebox.askyesno("確認", "選択したタスクを削除しますか？"):
                index = self.get_task_index(selected_id[0])
                del self.tasks[index]
                self.save_tasks()
                self.refresh_task_list()
        else:
            messagebox.showwarning("警告", "削除するタスクを選択してください。")

    def get_task_index(self, item_id):
        return int(item_id[1:]) - 1

    def refresh_task_list(self):
        for item in self.task_list.get_children():
            self.task_list.delete(item)
        
        for i, task in enumerate(self.tasks):
            status = "完了" if task.completed else "未完了"
            self.task_list.insert("", tk.END, iid=f"I{i+1}",
                                values=(task.priority, status, task.text))

    def save_tasks(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in self.tasks], f, ensure_ascii=False, indent=2)

    def load_tasks(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(task_data) for task_data in data]
        except FileNotFoundError:
            self.tasks = []

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
