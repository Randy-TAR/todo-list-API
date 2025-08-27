from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# server validation model
class Todo(BaseModel):
    text: str = None
    is_done: bool = False

# model with optional fields for partial updates 
class TodoUpdate(BaseModel):
    text: Optional[str] = None
    is_done: Optional[bool] = None

# Home page 
@app.get("/")
def home():
    return {"This is my Todo list With simple CRUD operations"}

# todo_list = [
#   {"text": "eat", "is_done": False},
#   {"text": "play", "is_done": False},
#   {"text": "dance", "is_done": False},
#   {"text": "read", "is_done": False},
#   {"text": "work", "is_done": False},
#   {"text": "hag out", "is_done": False}
# ]

todo_list: List[Todo] = [
    Todo(text="eat", is_done=False),
    Todo(text="study", is_done=False)
]

# Adding a task to the to do list
@app.post("/add_task")
def add_task(task: List[Todo]):
    todo_list.append(task)
    # return todo_list
    return JSONResponse(content={"message": "Task updated successfully"}, status_code=200)


# getting task by id
@app.get("/get_task/{task_id}", response_model=Todo)
def get_task(task_id: int) -> Todo:
    if task_id < len(todo_list):
        return todo_list[task_id]
    else: 
        raise HTTPException(status_code=404, detail="task not found")


# getting all created task
@app.get("/all_task")
def all_task():
    return todo_list


# updating a task
@app.put("/update_task/{task_id}", response_model = Todo)
def update_task(task_id: int, task_update: Todo) -> Todo:
    if task_id < len(todo_list):
        todo_list[task_id] = task_update
        return JSONResponse(content={"message": "Task updated successfully"}, status_code=200)
    else: 
        raise HTTPException(status_code=404, detail="task not found")


# partially updating task
@app.patch("/partial_update/{task_id}", response_model=Todo)
def partial_task_uptade(task_id: int, task_update: TodoUpdate):
    if task_id < len(todo_list):
        updated_task = todo_list[task_id]

        # Updating only available feilds 
        if task_update.text is not None:
            updated_task.text = task_update.text
        if task_update.is_done is not None:
            updated_task.is_done = task_update.is_done

        todo_list[task_id] = updated_task
        return JSONResponse(content={"message": "Task partially updated successfully"}, status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Task not found")


#  delleting task
@app.delete("/delete_task/{task_id}", response_model=Todo)
def delete_task(task_id: int) -> Todo:
    if task_id < len(todo_list):
        todo_list.pop(task_id)
        return JSONResponse(content={"message": "Task deleted successfully"}, status_code=200)
    else:
        return HTTPException(status_code=404, detail="Task not found")