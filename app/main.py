# # app/main.py

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import shutil
import os

from app.auth.auth import register_user, login_user
from app.messaging.messaging import send_message, read_messages, init_user_keys
from app.files.files import encrypt_file, decrypt_file

from app.blockchain.blockchain import Blockchain

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    secret = register_user(username, password)
    init_user_keys(username)
    return HTMLResponse(f"""
        <h2>Registered</h2>
        <p>TOTP Secret (add to Authenticator): {secret}</p>
        <a href="/">Back</a>
    """)



@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    totp: str = Form(...)
):
    if login_user(username, password, totp):
        response = RedirectResponse(
            url=f"/dashboard?user={username}",
            status_code=302
        )
        # Устанавливаем куки пользователя
        response.set_cookie(key="user", value=username, httponly=True)
        return response

    return HTMLResponse("<h2>Login failed</h2><a href='/'>Back</a>")


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, user: str):
    messages = read_messages(user)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "messages": messages
        }
    )


@app.post("/send")
def send(request: Request, receiver: str = Form(...), message: str = Form(...)):
    # Получаем текущего пользователя из cookie
    sender = request.cookies.get("user")
    if not sender:
        # Если нет cookie, редиректим на главную
        return RedirectResponse("/", status_code=302)

    # Отправляем сообщение
    send_message(sender, receiver, message)

    # Перенаправляем обратно на dashboard
    return RedirectResponse(
        url=f"/dashboard?user={sender}",
        status_code=302
    )


@app.post("/encrypt-file")
async def encrypt_file_web(request: Request, file: UploadFile = File(...)):
    username = request.cookies.get("user")
    if not username:
        return RedirectResponse("/", status_code=302)

    temp_dir = "app/temp"
    os.makedirs(temp_dir, exist_ok=True)
    input_path = os.path.join(temp_dir, file.filename)
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    encrypted_path = encrypt_file(username, input_path)

    return FileResponse(
        encrypted_path,
        filename=os.path.basename(encrypted_path),
        media_type="application/octet-stream"
    )


@app.post("/decrypt-file")
async def decrypt_file_web(request: Request, file: UploadFile = File(...)):
    username = request.cookies.get("user")
    if not username:
        return RedirectResponse("/", status_code=302)

    temp_dir = "app/temp"
    os.makedirs(temp_dir, exist_ok=True)
    enc_path = os.path.join(temp_dir, file.filename)
    with open(enc_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_filename = file.filename.replace(".enc", "")
    output_path = os.path.join(temp_dir, f"decrypted_{output_filename}")
    decrypt_file(username, enc_path, output_path)

    return FileResponse(
        output_path,
        filename=os.path.basename(output_path),
        media_type="application/octet-stream"
    )

@app.get("/audit", response_class=HTMLResponse)
def audit(request: Request):
    bc = Blockchain()
    return templates.TemplateResponse(
        "audit.html",
        {
            "request": request,
            "chain": bc.chain,
            "valid": bc.is_chain_valid()
        }
    )