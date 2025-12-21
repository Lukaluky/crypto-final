from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.auth.auth import register, login
import pyotp

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/register")
def do_register(username: str = Form(...), password: str = Form(...)):
    secret = pyotp.random_base32()
    register(username, password, secret)
    return {"totp_secret": secret}

@app.post("/login")
def do_login(username: str = Form(...), password: str = Form(...), code: str = Form(...)):
    token = login(username, password)
    if not token:
        return {"error": "login failed"}
    return {"session": token}
