import express from "express";
import { getEstudiantes } from "../controllers/estudiantesController.js";

const router = express.Router();

router.get("/", getEstudiantes);

export default router;
