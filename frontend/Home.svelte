<script>
  let estudiantes = [];

  fetch("http://localhost:3000/estudiantes")
    .then(r => r.json())
    .then(data => estudiantes = data);
</script>

<h1>Estudiantes</h1>

<ul>
  {#each estudiantes as e}
    <li>
      {e.nombre}
      <a href={`/estudiante/${e.id}`}>Ver notas</a>
      <a href="/registrar">Registrar nota</a>
    </li>
  {/each}
</ul>
