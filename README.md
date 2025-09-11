# NASA Mega API Backend

Backend unificado en Python para consumir varias APIs de la NASA y devolver información en JSON.  
No necesita frontend y se puede probar directamente desde Swagger UI o Postman.

---

## 📦 Tecnologías

- Python 3.10+
- FastAPI
- Uvicorn
- Requests
- Python-Dotenv

---

## 🗂 Estructura del proyecto

<img width="563" height="440" alt="image" src="https://github.com/user-attachments/assets/739c9b5c-9f19-40ff-aac0-280e81e45938" />

---

## ⚡ Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/TU_USUARIO/nasa-mega-api-backend.git
cd nasa-mega-api-backend
```

2. Crear y activar el entorno virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

```
3. Instalar dependencias:
   
```bash
pip install -r requirements.txt
```

4. Crear archivo .env con tu NASA API Key:
   
```bash
NASA_API_KEY=TU_API_KEY_DE_NASA
```

5. 🚀 Levantar el backend:

python run.py
- Servidor disponible en: http://127.0.0.1:8000/
- Swagger UI (documentación interactiva) en: http://127.0.0.1:8000/docs


## 🛰 Endpoints principales

1. / – Bienvenida

- Descripción: JSON con guía rápida y endpoints disponibles.
- Ejemplo de respuesta:

```json
{
  "message": "🚀 Bienvenido al NASA Mega API Backend!",
  "docs": "/docs",
  "endpoints": [
    { "url": "/apod", "description": "Astronomy Picture of the Day" },
    { "url": "/neo", "description": "Near Earth Objects" },
    { "url": "/mars-rover", "description": "Fotos de Marte" },
    { "url": "/space-weather", "description": "Imágenes EPIC de la Tierra" }
  ]
}
```

2. /apod – Astronomy Picture of the Day

- Parámetros opcionales: date (YYYY-MM-DD)
- Ejemplo:
```json
[
  {
    "name": "Asteroide 123",
    "size": "123 m",
    "is_potentially_hazardous": true,
    "close_approach_date": "2025-09-10"
  }
]
```

3. /neo – Near Earth Objects

- Parámetros obligatorios: start_date, end_date (YYYY-MM-DD)
- Parámetro opcional: limit para acotar la cantidad de resultados
- Notas: el backend combina automáticamente rangos de 7 días por request
- Validaciones:
     -end_date >= start_date.
     -Rango máximo: 7 días.
- Ejemplo:
```json
[
  {
    "name": "Asteroide 123",
    "diameter_min": 123.4,
    "diameter_max": 234.5,
    "is_potentially_hazardous": true,
    "close_approach_date": "2025-09-10",
    "relative_velocity_km_s": "12.34",
    "miss_distance_km": "56789.0"
  }
]

```

4. /mars-rover – Mars Rover Photos

- Parámetros opcionales:
  - rover (ejemplos: curiosity, opportunity, spirit)
  - sol (día marciano desde el inicio de la misión)
  - camera (FHAZ, RHAZ, NAVCAM, etc.)
  - limit (cantidad máxima de fotos, default: 20)
  - Ejemplo:
 ```json
[
  {
    "id": 102693,
    "img_src": "https://mars.nasa.gov/...",
    "earth_date": "2015-06-03",
    "camera": "Front Hazard Avoidance Camera"
  }
]
 ```

 
5. /space-weather – EPIC Earth Images

- Parámetro obligatorio: date (YYYY-MM-DD, mínimo 2015-06-13)
- Notas: no todas las fechas tienen imágenes; si no hay, devuelve mensaje en JSON
- Ejemplo:
```json
[
  {
    "image": "https://epic.gsfc.nasa.gov/archive/natural/2025/09/10/png/epic_image.png",
    "caption": "Vista de la Tierra",
    "date": "2025-09-10"
  }
]

```


## 💻 Ejemplos de requests (curl/Postman)

### 1. `/apod`

```bash
curl -X GET "http://127.0.0.1:8000/apod?date=2025-09-10"
```

## 2. /neo

```bash
curl -X GET "http://127.0.0.1:8000/neo?start_date=2025-09-01&end_date=2025-09-07&limit=10"
```

## 3. /mars-rover

```bash
curl -X GET "http://127.0.0.1:8000/mars-rover?rover=curiosity&sol=1000&camera=FHAZ&limit=5"
```

## 4. /space-weather

```bash
curl -X GET "http://127.0.0.1:8000/space-weather?date=2025-09-01"
```

##🔹 Consejos para Postman

- Crear una nueva colección: NASA Mega API Backend.
- Agregar cada endpoint como request GET.
- Configurar parámetros desde la pestaña Params.
- Ejecutar y ver JSON de respuesta directamente.

## 🧪 Testing con pytest

1. Instalar dependencias de testing (si no están ya instaladas):
```bash
pip install pytest pytest-asyncio httpx
```

2. Ejecutar tareas:

```bash
python -m pytest -v
```
- Verifica endpoints, códigos de respuesta y límites de resultados.
- Ejemplo de salida:
```arduino
collected 11 items
tests/test_endpoints.py::test_root PASSED
tests/test_endpoints.py::test_apod PASSED
tests/test_endpoints.py::test_neo PASSED
tests/test_endpoints.py::test_mars_rover PASSED
tests/test_endpoints.py::test_space_weather PASSED
tests/test_endpoints.py::test_neo_exceed_range PASSED (422 esperado)
tests/test_endpoints.py::test_neo_start_after_end PASSED (422 esperado)
```

🌟 Buenas prácticas aplicadas y sugeridas

  ✅ Aplicadas
  
    - Modularidad: separación de configuración, servicios y routers.
    - Validación de parámetros con Pydantic v2 (FieldValidator, reglas por campo).
    - Control de errores con códigos HTTP claros (400, 422).
    - Configuración segura con .env.
    - Testing automatizado con pytest y FastAPI TestClient.
    - Documentación interactiva con Swagger UI.
    - Control de resultados grandes con limit.

⚠️ Sugeridas

    - Logging de requests y errores.
    - Tests más avanzados de integración y rendimiento.
    - CI/CD para ejecutar tests automáticamente.

📝 Licencia

Este proyecto se distribuye bajo licencia MIT.

---




