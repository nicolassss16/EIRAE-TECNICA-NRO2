from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from . import api, database, models # Importamos los módulos

# --- 1. Inicializa la Base de Datos ---
database.init_db()


# --- 2. Crear la Aplicación FastAPI ---
app = FastAPI(title="Servidor Eirae v2.0")

# Monta la carpeta 'static'
# (Asegúrate de que 'app/static' sea la ruta correcta donde está tu CSS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
# Ubica la carpeta 'templates'
templates = Jinja2Templates(directory="app/templates")


# --- 3. Incluir las rutas de la API ---
app.include_router(api.router)


# --- 4. Definir la ruta de la Página Web (¡MODIFICADO!) ---
@app.get("/", response_class=HTMLResponse)
async def pagina_de_inicio(request: Request):
    """
    Sirve la página principal (index.html), que AHORA CONTIENE
    tanto la sección de inicio como el dashboard.
    """
    return templates.TemplateResponse("index.html", {"request": request})

# --- ¡YA NO NECESITAMOS ESTA RUTA! ---
# @app.get("/dashboard", response_class=HTMLResponse)
# async def pagina_de_dashboard(request: Request):
#     return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/test", response_class=HTMLResponse)
async def pagina_de_testing(request: Request):
    """
    Sirve una página de testing interna para inyectar datos.
    """
    return templates.TemplateResponse("test.html", {"request": request})


@app.on_event("startup")
def on_startup():
    """
    Se ejecuta una sola vez cuando el servidor arranca.
    Usamos esto para crear sensores de prueba si no existen.
    """
    db = database.SessionLocal()
    
    # Verificamos si ya existe un sensor de prueba
    sensor1 = db.query(models.Sensor).filter(models.Sensor.nombre == "Sensor-OBELISCO").first()
    if not sensor1:
        print("Creando sensor de prueba: Sensor-OBELISCO")
        sensor1 = models.Sensor(nombre="Sensor-OBELISCO", lat=-34.6037, lon=-58.3816)
        db.add(sensor1)
        
    sensor2 = db.query(models.Sensor).filter(models.Sensor.nombre == "Sensor-Palermo").first()
    if not sensor2:
        print("Creando sensor de prueba: Sensor-Palermo")
        sensor2 = models.Sensor(nombre="Sensor-Palermo", lat=-34.5830, lon=-58.4330)
        db.add(sensor2)
    
    db.commit()

    db.close()
