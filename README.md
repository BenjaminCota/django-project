# Tienda Online — Django + React

Proyecto full stack: API REST con Django + DRF + JWT (MySQL) y frontend en
React (Vite). Incluye autenticación JWT, registro de usuarios, CRUD de
productos/categorías, un widget que consume una API de terceros (Dog CEO) y
un endpoint backend que consume un Web Service SOAP (CountryInfoService, vía
`zeep`).

## Estructura

```
├── tienda_online/   # proyecto Django (settings, urls)
├── products/        # app de productos/categorías + endpoint SOAP
├── users/            # app de usuarios (modelo custom, JWT, registro)
└── frontend/         # app de React (Vite)
```

## Backend (Django)

### Requisitos

- Python 3.11+
- MySQL Server corriendo localmente

### Instalación

```bash
cd django-project
python -m venv venv
./venv/Scripts/activate        # Windows
# source venv/bin/activate     # Linux / macOS

pip install -r requirements.txt
```

### Configuración

Copia `.env.example` a `.env` y completa tus valores (clave secreta,
credenciales de MySQL):

```bash
cp .env.example .env
```

Crea la base de datos en MySQL (si no existe):

```sql
CREATE DATABASE django_api CHARACTER SET utf8mb4;
```

### Migraciones y superusuario

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Correr el servidor

```bash
python manage.py runserver
```

- API: http://127.0.0.1:8000/api/v1/
- Swagger: http://127.0.0.1:8000/swagger/
- Redoc: http://127.0.0.1:8000/redoc/
- Admin: http://127.0.0.1:8000/admin/

### Tests

```bash
python manage.py test
```

### Endpoints principales

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| POST | `/api/v1/auth/token/` | Login (email + password) → access/refresh | No |
| POST | `/api/v1/auth/token/refresh/` | Refresca el access token | No |
| POST | `/api/v1/auth/register/` | Registro de usuarios nuevos | No |
| GET/PUT | `/api/v1/auth/me/` | Datos del usuario autenticado | Sí |
| CRUD | `/api/v1/users/` | Gestión de usuarios (solo admin) | Sí (admin) |
| CRUD | `/api/v1/products/`, `/api/v1/categories/` | Catálogo de productos | Sí |
| GET | `/api/v1/soap/pais/?iso=MX` | Consume el Web Service SOAP de países | Sí |

## Frontend (React + Vite)

### Instalación

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

La app queda en http://localhost:5173/ y espera el backend en
http://localhost:8000/ (configurable en `frontend/.env`).

### Páginas

- `/login` — inicio de sesión (JWT)
- `/register` — registro de usuarios
- `/dashboard` — panel protegido (requiere sesión), muestra los datos del
  usuario autenticado y el widget de la API de terceros
- `/`, `/home` — página pública

### Stack

React Router v6, Formik + Yup, Semantic UI React, SASS, react-toastify.

## Notas de seguridad

- `SECRET_KEY` y credenciales de MySQL se cargan desde `.env` (no están en
  el repo).
- Las contraseñas de usuario se hashean en el serializer (`set_password`),
  nunca se exponen en ninguna respuesta de la API.
- CORS restringido a los orígenes del frontend de desarrollo
  (`CORS_ALLOWED_ORIGINS` en `.env`).
