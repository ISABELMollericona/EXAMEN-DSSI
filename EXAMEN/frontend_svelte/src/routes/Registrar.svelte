<script>
import { onMount } from 'svelte'
import { fetchEstudiantes, fetchMaterias, postNota } from '../api'
let estudiantes = []
let materias = []
let mensaje = ''
let estSelected = ''
let matSelected = ''
let nota = ''

onMount(async () => {
  estudiantes = await fetchEstudiantes()
  materias = await fetchMaterias()
  const params = new URLSearchParams(window.location.hash.slice(window.location.hash.indexOf('?')))
  if(params.get('est')) estSelected = params.get('est')
})

async function guardar(e){
  e.preventDefault()
  mensaje = ''
  if(nota === '' || isNaN(nota) || Number(nota) < 0 || Number(nota) > 100){
    mensaje = 'La nota debe ser un número entre 0 y 100'
    return
  }
  const res = await postNota({estudiante_id: estSelected, materia_id: matSelected, nota})
  const data = await res.json()
  if(res.ok){ mensaje = data.message; nota='' }
  else mensaje = data.error || 'Error'
}
</script>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

<h1 class="mt-4">Registrar Nota</h1>
{#if mensaje}
  <div class="alert alert-info">{mensaje}</div>
{/if}
<form on:submit|preventDefault={guardar} class="mt-3">
  <div class="mb-3">
    <label class="form-label">Estudiante</label>
    <select bind:value={estSelected} class="form-select">
      {#each estudiantes as e}
        <option value={e[0]}>{e[1]}</option>
      {/each}
    </select>
  </div>
  <div class="mb-3">
    <label class="form-label">Materia</label>
    <select bind:value={matSelected} class="form-select">
      {#each materias as m}
        <option value={m[0]}>{m[1]}</option>
      {/each}
    </select>
  </div>
  <div class="mb-3">
    <label class="form-label">Nota</label>
    <input class="form-control" type="number" bind:value={nota} min="0" max="100" step="0.01" required />
  </div>
  <button class="btn btn-primary">Guardar</button>
</form>
