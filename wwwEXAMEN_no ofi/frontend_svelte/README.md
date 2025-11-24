# Frontend Svelte para Examen

Instrucciones rápidas:

1. Ir al directorio `frontend_svelte`:

```powershell
cd .\frontend_svelte
```

2. Instalar dependencias:

```powershell
npm install
```

3. Arrancar en modo desarrollo (Vite, con proxy a Flask):

```powershell
npm run dev
```

El dev server estará en `http://localhost:5173`. Las llamadas a la API usan prefijo `/api` y se proxearán a `http://localhost:5000`.

Endpoints usados por el frontend:
- `GET /api/estudiantes`
- `GET /api/materias`
- `POST /api/notas` (JSON)
- `GET /api/notas/estudiante/:id`

Asegúrate de que el backend Flask esté corriendo en `http://localhost:5000` antes de usar el frontend.
