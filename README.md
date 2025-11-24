# Sistema de Registro de Notas — Especificaciones Técnicas

Este repositorio contiene el backend y frontend del examen práctico "Registro de Notas" para la materia Desarrollo de Sistemas II.

Contenido del repositorio
- `backend/` — API REST en Node.js + Express usando Prisma como ORM (conector: MySQL por defecto en esta copia).
- `frontend/` — Cliente en Svelte (Vite) con las pantallas para listar estudiantes, registrar notas y consultar notas por estudiante.

**Objetivo**: permitir registrar notas, listar estudiantes y materias, consultar las notas de un estudiante y obtener su promedio.

----

**Requisitos mínimos**
- Node.js 16+ (recomendado 18+)
- npm 8+
- Base de datos: MySQL (configurable a PostgreSQL cambiando `prisma/schema.prisma` y `backend/.env`)

----

**Estructura del proyecto**

- `backend/`
	- `package.json` — scripts y dependencias
	- `prisma/schema.prisma` — modelos de datos (Prisma)
	- `.env` — variable `DATABASE_URL`
	- `src/app.js` — punto de entrada del servidor
	- `src/db.js` — inicialización de `PrismaClient`
	- `src/controllers/` — lógica de los endpoints
	- `src/routes/` — definición de rutas: `/estudiantes`, `/materias`, `/notas`

- `frontend/`
	- `App.svelte`, `Home.svelte`, `RegistrarNota.svelte`, `EstudianteNotas.svelte`
	- `package.json`, `vite.config.js` (configuración típica de Svelte + Vite)

----

**Base de datos / Modelos (Prisma)**

Archivo: `backend/prisma/schema.prisma`

Modelos principales:

```prisma
model estudiantes {
	id     Int      @id @default(autoincrement())
	nombre String
	notas  notas[]
}

model materias {
	id     Int      @id @default(autoincrement())
	nombre String
	notas  notas[]
}

model notas {
	id            Int          @id @default(autoincrement())
	nota          Int
	estudiante_id Int
	materia_id    Int
	estudiante    estudiantes  @relation(fields: [estudiante_id], references: [id])
	materia       materias     @relation(fields: [materia_id], references: [id])
}
```

Datasource: en esta copia `provider = "mysql"` y `url = env("DATABASE_URL")`. Puedes cambiar a `postgresql` si lo deseas.

----

**Variables de entorno**

Coloca en `backend/.env` la variable:

```
DATABASE_URL="mysql://<usuario>:<clave>@<host>:<puerto>/<nombre_bd>"
```

Ejemplo (archivo incluido en el repo):

```
DATABASE_URL="mysql://root:moll4503@localhost:3306/examen_dsii"
```

Si cambias a PostgreSQL, la URL debe tener el formato: `postgresql://user:pass@host:5432/dbname?schema=public`

----

**API — Endpoints obligatorios**

Base URL: `http://localhost:3000`

1) GET `/estudiantes`
- Descripción: devuelve la lista completa de estudiantes.
- Respuesta: 200 OK, JSON array de objetos `{ id, nombre }`.

Ejemplo cURL:
```
curl http://localhost:3000/estudiantes
```

2) GET `/materias`
- Descripción: devuelve la lista completa de materias.
- Respuesta: 200 OK, JSON array de objetos `{ id, nombre }`.

3) POST `/notas`
- Descripción: registra una nueva nota.
- Request body (JSON): `{ "estudiante_id": number, "materia_id": number, "nota": number }`.
- Validaciones (backend):
	- `nota` obligatorio y numérico entre 0 y 100 (incluidos).
	- `estudiante_id` existente.
	- `materia_id` existente.
- Respuestas:
	- 200 OK — devuelve el objeto nota creado.
	- 400 Bad Request — devuelve `{ error: "mensaje" }` si falla validación.

Ejemplo cURL:
```
curl -X POST http://localhost:3000/notas -H "Content-Type: application/json" -d '{"estudiante_id":1,"materia_id":2,"nota":85}'
```

4) GET `/notas/estudiante/:id`
- Descripción: obtiene todas las notas de un estudiante, incluyendo nombre de materia y el promedio general.
- Respuesta: 200 OK — `{ "notas": [ { id, nota, materia: { id, nombre } } ], "promedio": number }`.

----

**Validaciones y errores esperados**
- Nota vacía o no numérica: 400 `{ error: "La nota es obligatoria" }` o `{ error: "La nota debe ser un número entre 0 y 100." }`.
- Nota fuera de rango: 400 `{ error: "Nota inválida (0-100)" }`.
- Estudiante o materia inexistente: 400 `{ error: "El estudiante no existe" }` / `{ error: "La materia no existe" }`.

----

**Frontend — pantallas y comportamientos**

- `/` o `Home.svelte`: lista estudiantes, botones "Ver Notas" y "Registrar Nota".
- `/registrar` o `RegistrarNota.svelte`: formulario con selects (estudiante, materia) y `input type=number` para la nota; validación cliente (0-100), muestra errores del backend y mensajes de éxito.
- `/estudiante/:id` o `EstudianteNotas.svelte`: muestra tabla materias+notas y el promedio.

Notas de implementación:
- Los selects se obtienen desde `GET /estudiantes` y `GET /materias`.
- El formulario convierte valores a `Number` y maneja `loading`, `error` y `success` en la UI.

----

**Scripts y comandos**

Backend (`backend/`):

```powershell
npm install
npm install mysql2 prisma --save-dev
npm install @prisma/client

# Generar cliente prisma
npx prisma generate

# Migraciones (opción A, crear historial)
npx prisma migrate dev --name init

# O sincronizar sin migraciones
npx prisma db push

# Iniciar servidor en desarrollo (nodemon)
npm run dev

# Iniciar servidor producción
npm start
```

Frontend (`frontend/`):

```powershell
npm install
npm run dev
```

----

**Seeds / Datos de ejemplo**

Recomiendo crear un script `prisma/seed.js` o usar migraciones para insertar algunos `estudiantes` y `materias` de ejemplo (por ejemplo 5 estudiantes y 5 materias). Puedes usar `npx prisma db seed` si configuras `package.json` y `prisma` para ello.

Ejemplo rápido (manual): insertar filas usando MySQL Workbench / línea de comandos en la base `examen_dsii`.

----

**Postman / Pruebas rápidas**

- Crea una colección con los 4 endpoints: `GET /estudiantes`, `GET /materias`, `POST /notas`, `GET /notas/estudiante/:id`.
- Añade ejemplos de request/response y variables de entorno `baseUrl = http://localhost:3000`.

Ejemplos cURL incluidos arriba.

----

**Despliegue (sugerencias)**

- Backend: puede desplegarse en Heroku, Render, Railway o Azure App Service. Asegúrate de configurar la variable de entorno `DATABASE_URL` en el entorno de producción.
- Base de datos: MySQL en un servicio gestionado (ClearDB, Amazon RDS, PlanetScale) o MySQL en un contenedor Docker.
- Frontend: Vercel, Netlify o un hosting estático que sirva la app compilada (si usas Vite, `vite build`).

SSL / CORS: el backend incluye `cors()` por defecto. En producción limita `origin` a tu dominio.

----

**Checklist de entrega (para el examen)**

- [ ] Repositorio Backend en GitHub con todo el código.
- [ ] Repositorio Frontend en GitHub con todo el código.
- [ ] `README.md` en cada repo con instrucciones de instalación y ejecución.
- [ ] Colección Postman exportada (.json).
- [ ] Base de datos poblada o instrucciones/seed para poblarla.
- [ ] Capturas de pantalla: conexión BD en Workbench/pgAdmin, Postman con endpoints funcionando, vistas del frontend.
- [ ] Documento PDF final con enlaces y capturas.

----

**Notas finales y próximos pasos recomendados**

1. Asegúrate de que `backend/.env` contiene las credenciales correctas para tu entorno local.
2. Ejecuta `npx prisma migrate dev --name init` o `npx prisma db push` para crear las tablas.
3. Pobla la base con datos de prueba (seed) para poder usar el frontend sin errores.
4. Genera la colección Postman y exporta el JSON para añadirla al entregable.
5. Completa las capturas de pantalla y crea el PDF final con las instrucciones y evidencias.

Si quieres, puedo:
- Crear un `prisma/seed` de ejemplo con estudiantes y materias.
- Generar la colección Postman básica y añadirla al repo.
- Crear `frontend/README.md` con pasos de ejecución específicos.

Indica cuál de las tareas deseas que haga a continuación y la ejecuto.

