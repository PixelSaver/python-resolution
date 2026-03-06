from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll, Horizontal
from textual.widgets import Button, Static, Footer, Header, ListView, ListItem
import json
import os

TASKS_FILE = "tasks.json"

# load tasks from file
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return [{"id": 1, "task": "Initial Task", "done": False}]
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

class TaskList(ListView):
    def on_mount(self):
        self.refresh_tasks()
    
    def refresh_tasks(self):
        self.clear()
        
        tasks = load_tasks()
        
        if len(tasks) == 0:
            self.append(ListItem(Static("Press A to add a task")))
            return
        
        for task in tasks:
            status = "X" if task["done"] else " "
            row = f"[{status}] {task['id']}: {task['task']}"
            
            self.append(ListItem(Static(row)))
        
class TaskApp(App):
    BINDINGS = [
        ("a", "add_task", "Add Task"), 
        ("d", "mark_done", "Mark Done"), 
        ("D", "toggle_dark", "Toggle dark mode"),
        ("space", "toggle_task", "Toggle"),
        ("q", "quit", "Quit"),
    ]
    def compose(self) -> ComposeResult:
        yield Header()
        yield TaskList()
        yield Footer()
    
    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
    
    def action_toggle_task(self):
        list_view = self.query_one(TaskList)
        if list_view.index is None: 
            return
        
        selected_index = list_view.index
        tasks = load_tasks()
        
        if selected_index < len(tasks):
            tasks[selected_index]["done"] = not tasks[selected_index]["done"]
            
            save_tasks(tasks)
            list_view.refresh_tasks()
            
            list_view.index = selected_index
    
if __name__ == "__main__":
    app = TaskApp()
    app.run()