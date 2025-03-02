import tkinter as tk
from tkinter import ttk, messagebox
from models.task import Task
from data.storage import TaskStorage
from gui.dialogs import TaskEditDialog

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todoリスト")
        self.root.geometry("500x600")
        
        self.storage = TaskStorage()
        self.tasks = []
        self.load_tasks()

        self._create_widgets()
        self.refresh_task_list()

    def _create_widgets(self):
        # タスク入力フレーム
        input_frame = ttk.Frame(self.root, padding="5")
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
        self.task_list = ttk.Treeview(self.root, columns=("Task", "Priority", "Status"), 
                                    show="headings", selectmode="browse")
        self.task_list.heading("Task", text="タスク内容")
        self.task_list.heading("Priority", text="優先度")
        self.task_list.heading("Status", text="状態")
        self.task_list.column("Task", width=300)
        self.task_list.column("Priority", width=70)
        self.task_list.column("Status", width=70)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ボタンフレーム
        button_frame = ttk.Frame(self.root, padding="5")
        button_frame.pack(fill=tk.X)

        complete_button = ttk.Button(button_frame, text="完了/未完了", command=self.toggle_complete)
        complete_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        edit_button = ttk.Button(button_frame, text="編集", command=self.edit_task)
        edit_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        delete_button = ttk.Button(button_frame, text="削除", command=self.delete_task)
        delete_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # エンターキーでタスクを追加
        self.task_input.bind('<Return>', lambda e: self.add_task())

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

        result = TaskEditDialog.show_dialog(self.root, task)
        if result:
            task.text = result["text"]
            task.priority = result["priority"]
            self.save_tasks()
            self.refresh_task_list()

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
                                values=(task.text, task.priority, status))

    def save_tasks(self):
        self.storage.save_tasks(self.tasks)

    def load_tasks(self):
        self.tasks = self.storage.load_tasks()
