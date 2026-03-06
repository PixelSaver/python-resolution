from textual.app import App, ComposeResult
from textual.widgets import Static, Footer, Header
import json
import os

TASKS_FILE = "tasks.json"

# load tasks from file
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

class TaskApp(App):
    BINDINGS = [
        ("a", "add_task", "Add Task"), 
        ("d", "mark_done", "Mark Done"), 
        ("D", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]
    def compose(self) -> ComposeResult:
        tasks = load_tasks()
        
        text = "Task Manager\n\n"
        
        for task in tasks:
            status = "x" if task["done"] else " "
            text += f"[{status}] {task['id']}: {task['task']}\n"
        
        text += "\n Press a=add, d=done, q=quit"
        yield Header()
        yield Static(text)
        yield Footer()
    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
    
if __name__ == "__main__":
    app = TaskApp()
    app.run()