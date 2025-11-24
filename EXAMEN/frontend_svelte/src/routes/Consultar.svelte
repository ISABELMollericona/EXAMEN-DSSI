<script>
import { onMount } from 'svelte'
import { fetchNotasEstudiante, fetchEstudiantes } from '../api'
export let query = ''
let notas = []
let promedio = null
let estudianteNombre = ''
onMount(async () => {
  // parse id from query like /consultar?id=1
  const q = query || window.location.hash.slice(1)
  const params = new URLSearchParams(q.slice(q.indexOf('?')))
  const id = params.get('id')
  if(!id) return
  const ests = await fetchEstudiantes()
  const est = ests.find(s => String(s[0]) === String(id))
  estudianteNombre = est ? est[1] : 'Estudiante'
  const data = await fetchNotasEstudiante(id)
  notas = data.notas || []
  promedio = data.promedio
})
</script>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

<h1 class="mt-4">Notas de {estudianteNombre}</h1>
{#if notas.length === 0}
  <div class="alert alert-warning">No hay notas para este estudiante</div>
{:else}
  <table class="table mt-3">
    <thead><tr><th>Materia</th><th>Nota</th></tr></thead>
    <tbody>
      {#each notas as n}
        <tr><td>{n[1]}</td><td>{n[0]}</td></tr>
      {/each}
    </tbody>
  </table>
  <div class="fw-bold">Promedio: {promedio !== null ? Number(promedio).toFixed(2) : 'N/A'}</div>
{/if}
