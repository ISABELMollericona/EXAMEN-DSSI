<script>
  import { onMount } from 'svelte';
  export let params;
  let data = { notas: [], promedio: 0 };
  let loading = true;
  let errorMsg = "";

  onMount(async () => {
    loading = true;
    errorMsg = "";
    try {
      const res = await fetch(`http://localhost:3000/notas/estudiante/${params.id}`);
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        errorMsg = err?.error || 'Error al obtener notas';
        data = { notas: [], promedio: 0 };
      } else {
        data = await res.json();
      }
    } catch (e) {
      errorMsg = 'No se pudo conectar con el servidor.';
      data = { notas: [], promedio: 0 };
    } finally {
      loading = false;
    }
  });
</script>

<h1>Notas del estudiante</h1>

{#if loading}
  <div>Cargando notas...</div>
{:else}
  {#if errorMsg}
    <div style="color: #b00020">{errorMsg}</div>
  {:else}
    {#if data.notas.length === 0}
      <div>No hay notas registradas para este estudiante.</div>
    {:else}
      <table border="1">
        <tr>
          <th>Materia</th>
          <th>Nota</th>
        </tr>

        {#each data.notas as n}
          <tr>
            <td>{n.materia.nombre}</td>
            <td>{n.nota}</td>
          </tr>
        {/each}
      </table>

      <h3>Promedio: {data.promedio}</h3>
    {/if}
  {/if}
{/if}
