import express from "express";
import cors from "cors";
import estudiantesRoutes from "./routes/estudiantes.js";
import materiasRoutes from "./routes/materias.js";
import notasRoutes from "./routes/notas.js";

const app = express();
app.use(cors());
app.use(express.json());

app.use("/estudiantes", estudiantesRoutes);
app.use("/materias", materiasRoutes);
app.use("/notas", notasRoutes);

app.listen(3000, () => console.log("Servidor corriendo en http://localhost:3000"));
