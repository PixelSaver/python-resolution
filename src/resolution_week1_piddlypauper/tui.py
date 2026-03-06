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

class TaskItem(ListItem):
    def __init__(self, task_data:dict):
        super().__init__()
        self.task_data = task_data
    
    def compose(self) -> ComposeResult:
        yield Static(self.label_text, id="label")
    
    # Like a godot export property
    @property 
    def label_text(self) -> str:
        status = "X" if self.task_data["done"] else " "
        # Backslash to escape markdown
        return f"\[{status}] {self.task_data['id']}: {self.task_data['task']}"
    
    def toggle(self):
        self.task_data["done"] = not self.task_data["done"]
        # Query one is like get_node
        self.query_one("#label", Static).update(self.label_text)
        
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
        yield ListView(id="task_list")
        yield Footer()
    
    def on_mount(self) -> None:
        list_view = self.query_one("#task_list", ListView)
        tasks = load_tasks()
        for task in tasks:
            list_view.append(TaskItem(task))
    
    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
    
    def action_toggle_task(self):
        list_view = self.query_one("#task_list", ListView)
        
        if list_view.highlighted_child is None: 
            return
        
        selected_item = list_view.highlighted_child
        if isinstance(selected_item, TaskItem):
            selected_item.toggle()
        
            all_tasks = [item.task_data for item in list_view.query(TaskItem)]
            save_tasks(all_tasks)
    
if __name__ == "__main__":
    app = TaskApp()
    app.run()