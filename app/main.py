from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json
import os

app = FastAPI()

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

@app.post("/add")
async def add_task(task: str = Form(...)):
    tasks.append({"title": task, "done": False})
    save_tasks(tasks) # ✅ Save to file
    return RedirectResponse("/", status_code=303)

