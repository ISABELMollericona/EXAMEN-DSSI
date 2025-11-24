<script>
import { onMount } from 'svelte'
import { fetchEstudiantes } from '../api'
let estudiantes = []
onMount(async () => {
  estudiantes = await fetchEstudiantes()
})
</script>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

<h1 class="mt-4">Estudiantes</h1>
<table class="table mt-3">
  <thead>
    <tr><th>Id</th><th>Nombre</th><th>CI</th><th>Email</th><th>Acciones</th></tr>
  </thead>
  <tbody>
    {#each estudiantes as e}
      <tr>
        <td>{e[0]}</td>
        <td>{e[1]}</td>
        <td>{e[2]}</td>
        <td>{e[3]}</td>
        <td>
          <a class="btn btn-sm btn-outline-primary" href={`#/consultar?id=${e[0]}`}>Ver Notas</a>
          <a class="btn btn-sm btn-outline-success ms-2" href={`#/registrar?est=${e[0]}`}>Registrar Nota</a>
        </td>
      </tr>
    {/each}
  </tbody>
</table>
