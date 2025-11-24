// simple wrapper to call backend proxied at /api
export async function fetchEstudiantes(){
  const res = await fetch('/api/estudiantes');
  return res.json();
}
export async function fetchMaterias(){
  const res = await fetch('/api/materias');
  return res.json();
}
export async function postNota(payload){
  const res = await fetch('/api/notas', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(payload)
  });
  return res;
}
export async function fetchNotasEstudiante(id){
  const res = await fetch(`/api/notas/estudiante/${id}`);
  return res.json();
}
