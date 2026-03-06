from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Button, Static, Footer, Header, ListView, ListItem
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
        yield Static(self.label_text, id="label", markup=False)
    
    # Like a godot export property
    @property 
    def label_text(self) -> str:
        status = "X" if self.task_data["done"] else " "
        return f"[{status}] {self.task_data['id']}: {self.task_data['task']}"
    
    def toggle(self):
        self.task_data["done"] = not self.task_data["done"]
        # Query one is like get_node
        self.query_one("#label", Static).update(self.label_text)

class ConfirmDelete(ModalScreen[bool]):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Are you sure you want to delete this task?", markup=False),
            Static(""),
            Horizontal(Button("Yes", id="yes", variant="error"),Button("No", id="no", variant="primary")),
            id="dialog",
        )
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "yes")

class TaskApp(App):
    BINDINGS = [
        ("a", "add_task", "Add Task"), 
        ("d", "delete", "Delete"), 
        ("D", "toggle_dark", "Toggle dark mode"),
        ("space", "toggle_task", "Toggle"),
        ("q", "quit", "Quit"),
    ]
    def compose(self) -> ComposeResult:
        yield Header()
        
        yield Input(placeholder="Type task and press Enter", id="task_input")
        
        yield ListView(id="task_list")
        yield Footer()
    
    def on_mount(self) -> None:
        input_box = self.query_one("#task_input", Input)
        input_box.display = False
        
        list_view = self.query_one("#task_list", ListView)
        tasks = load_tasks()
        for task in tasks:
            list_view.append(TaskItem(task))
    
    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
    
    def action_add_task(self):
        input_box = self.query_one("#task_input", Input)
        input_box.display = True
        input_box.focus()
    
    def on_input_submitted(self, event: Input.Submitted):
        text = event.value.strip()
        
        if not text:
            return
            
        list_view = self.query_one("#task_list", ListView)
        tasks = [item.task_data for item in list_view.query(TaskItem)]
        
        new_id = 1 if not tasks else max(t["id"] for t in tasks) + 1
        
        new_task = {
            "id": new_id,
            "task": text,
            "done": False
        }
        
        # list_view.insert(0, [TaskItem(new_task)])
        list_view.append(TaskItem(new_task))
        save_tasks(tasks + [new_task])
        
        # Hide input again
        input_box = self.query_one("#task_input", Input)
        input_box.display = False
        input_box.value = ""
        list_view.index = None
        list_view.focus()
    
    def action_delete(self) -> None:
        list_view = self.query_one("#task_list", ListView)
        
        if list_view.highlighted_child is None: 
            return
        
        def check_result(confirmed: bool | None) -> None:
            if confirmed:
                selected_item = list_view.highlighted_child
                if selected_item:
                    list_view.remove_children([selected_item])
                    all_tasks = [item.task_data for item in list_view.query(TaskItem)]
                    save_tasks(all_tasks)
        self.push_screen(ConfirmDelete(), check_result)
    
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