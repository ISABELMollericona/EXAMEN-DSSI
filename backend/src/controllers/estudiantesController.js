import { prisma } from "../db.js";

export const getEstudiantes = async (req, res) => {
  const data = await prisma.estudiantes.findMany();
  res.json(data);
};
