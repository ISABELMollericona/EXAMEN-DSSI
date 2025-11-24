import { prisma } from "../db.js";

export const crearNota = async (req, res) => {
  let { estudiante_id, materia_id, nota } = req.body;

  estudiante_id = Number(estudiante_id);
  materia_id = Number(materia_id);
  nota = Number(nota);

  if (nota === undefined || nota === null || isNaN(nota)) {
    return res.status(400).json({ error: "La nota es obligatoria" });
  }
  if (nota < 0 || nota > 100) return res.status(400).json({ error: "Nota inválida (0-100)" });

  const estudiante = await prisma.estudiantes.findUnique({ where: { id: estudiante_id } });
  if (!estudiante) return res.status(400).json({ error: "El estudiante no existe" });

  const materia = await prisma.materias.findUnique({ where: { id: materia_id } });
  if (!materia) return res.status(400).json({ error: "La materia no existe" });

  const newNota = await prisma.notas.create({
    data: { estudiante_id, materia_id, nota }
  });

  res.json(newNota);
};

export const getNotasPorEstudiante = async (req, res) => {
  const id = Number(req.params.id);

  const notas = await prisma.notas.findMany({
    where: { estudiante_id: id },
    include: { materia: true }
  });

  const promedio =
    notas.reduce((acc, n) => acc + n.nota, 0) / (notas.length || 1);

  res.json({ notas, promedio });
};
