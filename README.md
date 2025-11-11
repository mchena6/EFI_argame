Proyecto API Flask - Biblioteca de Juegos
Esta es la documentación para la API backend del proyecto de biblioteca de juegos, desarrollada en Flask. La API gestiona juegos, usuarios, reseñas y géneros, e implementa autenticación basada en tokens JWT con un sistema de roles.

1. Instrucciones de Instalación 🔧
Sigue estos pasos para configurar el entorno de desarrollo local.

SSH:
git clone git@github.com:mchena6/EFI_argame.git
cd EFI_argame

HTTPS:
git clone https://github.com/mchena6/EFI_argame.git
cd EFI_argame

b. Crear y Activar un Entorno Virtual

En macOS/Linux:
python3 -m venv venv
source venv/bin/activate

En Windows:
python -m venv venv
.\venv\Scripts\activate

c. Crear una copia del archivo de ejemplo .env.example y llamarla .env

En Linux/macOS: 
cp .env.example .env

En Windows:
copy .env.example .env

d. Abrir el nuevo archivo .env, generar su propia clave secreta para JWT_SECRET_KEY y colocar las credenciales para la conexion a la base de datos

e. Instalar Dependencias
Usa el archivo requirements.txt provisto para instalar todas las librerías necesarias.

pip install -r requirements.txt


2. Cómo Ejecutar el Proyecto ▶️
Una vez que las dependencias estén instaladas y el entorno virtual esté activado, puedes iniciar el servidor de Flask.

flask run 

El servidor se iniciará en modo de depuración (debug) y estará accesible en la siguiente dirección: http://127.0.0.1:5000/

4. Documentación de Endpoints (API) 🗺️
A continuación se detallan los endpoints disponibles, agrupados por recurso.


🔐 Autenticación

POST /register

Descripción: Registra un nuevo usuario en el sistema.
Acceso: Público.

Crear admin:
Body (JSON):
{
  "username": "nuevo_admin",
  "name": "Nombre Apellido",
  "email": "admin@ejemplo.com",
  "password": "clave",
  "role_id": 1 
}

Crear usuario:
Body (JSON):
{
  "username": "nuevo_usuario",
  "name": "Nombre Apellido",
  "email": "usuario@ejemplo.com",
  "password": "clave",
  "role_id": 2 
}

Crear moderator:
Body (JSON):
{
  "username": "nuevo_moderador",
  "name": "Nombre Apellido",
  "email": "moderador@ejemplo.com",
  "password": "clave",
  "role_id": 3 
}


POST /login

Descripción: Inicia sesión y devuelve un token de acceso JWT.
Acceso: Público.
Body (JSON):
{
  "email": "usuario@ejemplo.com",
  "password": "clave"
}


🎮 Juegos (Games)

GET /games

Descripción: Obtiene la lista de todos los juegos publicados (is_published=True).
Acceso: Público.


POST /games

Descripción: Añade un nuevo juego a la base de datos.
Acceso: Admin. (Requiere token JWT).
Body (JSON):
{
  "name": "Nombre del Juego",
  "price": 19.99,
  "release_date": "YYYY-MM-DD",
  "thumbnail": "http://url.com/imagen.png",
  "description": "Descripción del juego...",
  "developer_id": 1,
  "editor_id": 1
}


GET /games/<int:id>

Descripción: Obtiene los detalles de un juego específico por su ID.
Acceso: Público.


PATCH /games/<int:id>

Descripción: Modifica parcialmente un juego existente.
Acceso: Admin. (Requiere token JWT).
Body (JSON) (Cualquier campo del schema de juego es opcional) :
{
  "name": "Nuevo Nombre del Juego",
  "price": 25.00
}


DELETE /games/<int:id>

Descripción: Desactiva un juego (lo marca como is_published=False).
Acceso: Admin. (Requiere token JWT).


👤 Usuarios (Users)

GET /users

Descripción: Obtiene la lista de todos los usuarios activos (is_active=True).
Acceso: Admin. (Requiere token JWT).


GET /users/<int:id>

Descripción: Obtiene los detalles de un usuario específico por su ID.
Acceso: Admin o User (solo si es el propietario de la cuenta). (Requiere token JWT).


PATCH /users/<int:id>

Descripción: Modifica los datos de un usuario (username o email).
Acceso: Admin. (Requiere token JWT).
Body (JSON):
{
  "username": "nuevo_username",
  "email": "nuevo_email@ejemplo.com"
}


DELETE /users/<int:id>

Descripción: Desactiva un usuario (lo marca como is_active=False).
Acceso: Admin. (Requiere token JWT).


📚 Biblioteca de Usuario (User Library)

GET /users/<int:id>/games

Descripción: Obtiene la biblioteca de juegos (juegos reclamados) de un usuario.
Acceso: Admin o User (propietario). (Requiere token JWT).


POST /users/<int:id>/games

Descripción: Añade un juego a la biblioteca del usuario. El ID del usuario en la URL debe coincidir con el ID del usuario en el token.
Acceso: User. (Requiere token JWT).
Body (JSON):
{
  "game_id": 5
}


⭐ Reseñas (Reviews)

GET /games/<int:id>/reviews

Descripción: Obtiene todas las reseñas (visibles) de un juego específico.
Acceso: Público.


POST /games/<int:id>/reviews

Descripción: Publica una nueva reseña para un juego. El ID de usuario se toma del token JWT.
Acceso: User. (Requiere token JWT).
Body (JSON):
{
  "rating": 5,
  "text_review": "¡Este juego es increíble!"
}


DELETE /reviews/<int:id>

Descripción: Desactiva una reseña (la marca como is_visible=False).
Acceso: Admin, Moderator o User (solo si es el propietario de la reseña). (Requiere token JWT).


🏷️ Géneros (Genres)

GET /genres

Descripción: Obtiene la lista de todos los géneros.
Acceso: Público.


POST /genres

Descripción: Crea un nuevo género.
Acceso: Admin o Moderator. (Requiere token JWT).
Body (JSON):
{
  "name": "Estrategia"
}


PUT /genres/<int:id>

Descripción: Modifica el nombre o el estado de un género existente.
Acceso: Admin o Moderator. (Requiere token JWT).
Body (JSON):
{
  "name": "Estrategia en Tiempo Real",
  "is_active": true
}


DELETE /genres/<int:id>

Descripción: Desactiva un género (lo marca como is_active=False).
Acceso: Admin. (Requiere token JWT).


👨‍💻 Developers

GET /developers

Descripción: Obtiene la lista de todos los desarrolladores.
Acceso: Admin, Moderator o User. (Requiere token JWT).

GET /developers/<int:id>

Descripción: Obtiene los detalles de un desarrollador por su ID.
Acceso: Admin, Moderator o User. (Requiere token JWT).


🏢 Editors

GET /editors

Descripción: Obtiene la lista de todos los editores.
Acceso: Admin, Moderator o User. (Requiere token JWT).

GET /editors/<int:id>

Descripción: Obtiene los detalles de un editor por su ID.
Acceso: Admin, Moderator o User. (Requiere token JWT).


📊 Estadísticas (Stats)

GET /stats

Descripción: Obtiene estadísticas generales del sitio (total de usuarios, juegos, reseñas y publicaciones de la última semana).
Acceso: Admin o Moderator. (Requiere token JWT).


5. Credenciales de prueba

Admin:
{
  "email": "admin@gmail.com",
  "password": "admin"
}

User:
{
  "email": "zous@gmail.com",
  "password": "zous"
}

Moderator:
{
  "email": "moderator@gmail.com",
  "password": "moderator"
}