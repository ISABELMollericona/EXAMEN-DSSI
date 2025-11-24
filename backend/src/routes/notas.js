import express from "express";
import { crearNota, getNotasPorEstudiante } from "../controllers/notasController.js";

const router = express.Router();

router.post("/", crearNota);
router.get("/estudiante/:id", getNotasPorEstudiante);

export default router;
