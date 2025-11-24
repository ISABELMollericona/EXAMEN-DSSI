# Backend — Instrucciones para usar PostgreSQL con Prisma

Este backend ahora está configurado para usar PostgreSQL a través de Prisma. A continuación se indican pasos rápidos para configurar el entorno en Windows (PowerShell).

1) Instalar dependencias (en la carpeta `backend`):

```powershell
npm install pg
npm install prisma --save-dev
npm install @prisma/client
```

2) Crear o editar el archivo `.env` en `backend/` con la variable `DATABASE_URL` (ejemplo ya incluido):

```
DATABASE_URL="postgresql://usuario:clave@localhost:5432/examen_dsii?schema=public"
```

3) Generar cliente Prisma y aplicar migraciones (opción A — migraciones con historial):

```powershell
npx prisma generate
npx prisma migrate dev --name init
```

O bien, sincronizar esquema sin crear migraciones (opción B):

```powershell
npx prisma db push
npx prisma generate
```

4) Notas adicionales:
- Si tu base de datos se ejecuta en un contenedor o puerto distinto, ajusta la `DATABASE_URL` en `.env`.
- Si prefieres usar el usuario `postgres`, cambia `usuario:clave` por tus credenciales reales.
- Si tienes scripts en `package.json` para Prisma, puedes usarlos en lugar de los comandos anteriores.

Si quieres, ejecuto aquí los comandos de instalación y/o genero la migración ahora (necesitaré que confirmes usar credenciales reales o usar un ejemplo genérico).