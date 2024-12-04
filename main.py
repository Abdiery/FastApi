from fastapi import FastAPI, Depends, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
import datetime
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
import models
from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Configuración de Jinja2 para manejar las plantillas
templates = Jinja2Templates(directory="templates")

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para ver el listado de usuarios
@app.get("/users/list", response_class=HTMLResponse)
def get_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    today = datetime.datetime.now()  # Obtén la fecha actual
    users_with_age = []
    
    # Calcular la edad de cada usuario
    for user in users:
        if isinstance(user.year_of_birth, str):  # Si es una cadena, conviértela
            # Ajusta el formato para considerar la hora "00:00:00"
            user.year_of_birth = datetime.datetime.strptime(user.year_of_birth, "%Y-%m-%d %H:%M:%S")
        age = today.year - user.year_of_birth.year - ((today.month, today.day) < (user.year_of_birth.month, user.year_of_birth.day))
        users_with_age.append({**user.__dict__, "age": age})  # Añadir la edad al usuario
    
    return templates.TemplateResponse("list.html", {"request": request, "users": users_with_age, "today": today})

# Ruta para cargar el formulario
@app.get("/", response_class=HTMLResponse)
def read_form(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    max_date = datetime.datetime.now().date()
    return templates.TemplateResponse("form.html", {
        "request": request,
        "users": users,
        "max_date": max_date,
        "today": datetime.datetime.now()  # Pasa la fecha de hoy a la plantilla
    })

# Ruta para crear un nuevo usuario (POST)
@app.post("/users/", response_class=HTMLResponse)
def create_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    year_of_birth: str = Form(...),
    career: str = Form(...),
    db: Session = Depends(get_db),
):
    # Verificar si el correo ya está en uso
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        users = db.query(models.User).all()
        return templates.TemplateResponse(
            "form.html",
            {
                "request": request,
                "error": "El correo electrónico ya está en uso, por favor usa otro.",
                "users": users,
            },
        )

    # Verificar si la fecha de nacimiento es válida
    try:
        birth_date = datetime.datetime.strptime(year_of_birth, "%Y-%m-%d")
    except ValueError:
        users = db.query(models.User).all()
        return templates.TemplateResponse(
            "form.html",
            {"request": request, "error": "La fecha de nacimiento no es válida.", "users": users},
        )

    # Calcular la edad
    today = datetime.datetime.now()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    # Crear el nuevo usuario
    user = models.User(name=name, email=email, year_of_birth=birth_date, career=career)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    users = db.query(models.User).all()
    return templates.TemplateResponse(
        "form.html",
        {
            "request": request,
            "message": f"Usuario creado exitosamente! Edad: {age} años",
            "users": users,
        },
    )
