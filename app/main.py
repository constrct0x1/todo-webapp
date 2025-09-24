from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI ()

# Templates Folder
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Temporary task storage (without JSON yet)
tasks = []

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.post("/add", response_class=HTMLResponse)
async def add_task(request: Request, task: str = Form(...)):
    tasks.append({"text": task, "done": False})
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

