import express from "express";
import { getMaterias } from "../controllers/materiasController.js";

const router = express.Router();

router.get("/", getMaterias);

export default router;
