import tkinter as tk
from tkinter import ttk, messagebox

class TaskEditDialog:
    def __init__(self, parent, task):
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("タスクの編集")
        self.dialog.geometry("400x250")
        
        # メインフレーム（パディング付き）
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # タスク内容入力エリア
        task_frame = ttk.Frame(main_frame)
        task_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(task_frame, text="タスク内容:", font=("", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.edit_entry = ttk.Entry(task_frame, width=50)
        self.edit_entry.insert(0, task.text)
        self.edit_entry.pack(fill=tk.X)

        # 優先度選択エリア
        priority_frame = ttk.Frame(main_frame)
        priority_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(priority_frame, text="優先度:", font=("", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.priority_var = tk.StringVar(value=task.priority)
        priority_combo = ttk.Combobox(priority_frame, textvariable=self.priority_var,
                                    values=["高", "中", "低"], state="readonly", width=10)
        priority_combo.pack(anchor=tk.W)

        # ボタンエリア
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        save_button = ttk.Button(button_frame, text="保存", command=self.save, width=15)
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="キャンセル", command=self.cancel, width=15)
        cancel_button.pack(side=tk.LEFT, padx=5)

        # ダイアログの設定
        self.dialog.transient(parent)
        self.dialog.grab_set()
        parent.eval(f'tk::PlaceWindow {str(self.dialog)} center')

    def save(self):
        text = self.edit_entry.get().strip()
        if text:
            self.result = {
                "text": text,
                "priority": self.priority_var.get()
            }
            self.dialog.destroy()
        else:
            messagebox.showwarning("警告", "タスク内容を入力してください。")

    def cancel(self):
        self.dialog.destroy()

    @classmethod
    def show_dialog(cls, parent, task):
        dialog = cls(parent, task)
        parent.wait_window(dialog.dialog)
        return dialog.result
