from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates Folder
templates = Jinja2Templates(directory="app/templates")

DATA_FILE = "data.json"

# Helpers for JSON storage
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)
        
# Load tasks at startup
tasks = load_tasks()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.post("/add", response_class=HTMLResponse)
async def add_task(request: Request, task: str = Form(...)):
    tasks.append({"text": task, "done": False})
    save_tasks(tasks)  # save to JSON
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.post("/toggle/{task_id}", response_class=HTMLResponse)
async def toggle_task(request: Request, task_id: int):
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = not tasks[task_id]["done"]
        save_tasks(tasks)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.post("/delete/{task_id}", response_class=HTMLResponse)
async def delete_task(request: Request, task_id: int):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

