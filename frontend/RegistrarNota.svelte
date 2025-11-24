<script>
  import { onMount } from 'svelte';

  let estudiantes = [];
  let materias = [];
  let estudiante_id = "";
  let materia_id = "";
  let nota = "";

  let errorMsg = "";
  let successMsg = "";
  let loading = false;

  onMount(() => {
    fetch("http://localhost:3000/estudiantes")
      .then(r => r.json())
      .then(d => estudiantes = d)
      .catch(() => { estudiantes = []; });

    fetch("http://localhost:3000/materias")
      .then(r => r.json())
      .then(d => materias = d)
      .catch(() => { materias = []; });
  });

  async function guardar() {
    errorMsg = "";
    successMsg = "";

    // Validaciones cliente
    if (!estudiante_id) { errorMsg = 'Seleccione un estudiante.'; return; }
    if (!materia_id) { errorMsg = 'Seleccione una materia.'; return; }
    if (nota === "" || nota === null) { errorMsg = 'Ingrese una nota.'; return; }

    const notaNum = Number(nota);
    if (isNaN(notaNum) || notaNum < 0 || notaNum > 100) {
      errorMsg = 'La nota debe ser un número entre 0 y 100.'; return;
    }

    loading = true;
    try {
      const res = await fetch("http://localhost:3000/notas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ estudiante_id: Number(estudiante_id), materia_id: Number(materia_id), nota: notaNum })
      });

      const data = await res.json();
      if (!res.ok) {
        errorMsg = data?.error || 'Error al registrar la nota';
      } else {
        successMsg = 'Nota registrada correctamente.';
        // limpiar formulario
        estudiante_id = "";
        materia_id = "";
        nota = "";
      }
    } catch (err) {
      errorMsg = 'No se pudo conectar con el servidor.';
    } finally {
      loading = false;
    }
  }
</script>

<h1>Registrar Nota</h1>

{#if errorMsg}
  <div style="color: #b00020">{errorMsg}</div>
{/if}

{#if successMsg}
  <div style="color: #006400">{successMsg}</div>
{/if}

<select bind:value={estudiante_id}>
  <option value="">Seleccione estudiante</option>
  {#each estudiantes as e}
    <option value={e.id}>{e.nombre}</option>
  {/each}
</select>

<select bind:value={materia_id}>
  <option value="">Seleccione materia</option>
  {#each materias as m}
    <option value={m.id}>{m.nombre}</option>
  {/each}
</select>

<input type="number" min="0" max="100" bind:value={nota} />

<button on:click={guardar} disabled={loading}>{loading ? 'Guardando...' : 'Guardar'}</button>
