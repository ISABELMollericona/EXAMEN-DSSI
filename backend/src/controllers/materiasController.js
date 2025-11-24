import { prisma } from "../db.js";

export const getMaterias = async (req, res) => {
  const data = await prisma.materias.findMany();
  res.json(data);
};
