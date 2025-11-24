**Evidencias / Capturas de pantalla**

A continuación se presentan las capturas de pantalla del sistema funcionando:


![Conexión BD 1](./images/Captura%20de%20pantalla%202025-11-24%20095910.png)



![Consulta BD](./images/Captura%20de%20pantalla%202025-11-24%20100103.png)

![Home - Lista de Estudiantes](./images/Captura%20de%20pantalla%202025-11-24%20100804.png)


![Registrar Nota](./images/Captura%20de%20pantalla%202025-11-24%20100816.png)


![Postman Estudiantes](./images/Captura%20de%20pantalla%202025-11-24%20182137.png)


![Postman Notas](./images/Captura%20de%20pantalla%202025-11-24%20182154.png)

----



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

