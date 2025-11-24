<script>
import Home from './routes/Home.svelte'
import Registrar from './routes/Registrar.svelte'
import Consultar from './routes/Consultar.svelte'

let route = window.location.hash.slice(1) || '/'

window.addEventListener('hashchange', () => {
  route = window.location.hash.slice(1) || '/'
})
</script>

<style>
  .container { max-width: 900px; margin: 2rem auto; padding: 1rem; }
  nav a { margin-right: 0.5rem }
</style>

<div class="container">
  <nav>
    <a href="#/" class="btn btn-outline-primary">Home</a>
    <a href="#/registrar" class="btn btn-outline-success">Registrar Nota</a>
  </nav>

  {#if route === '/'}
    <Home />
  {:else if route === '/registrar'}
    <Registrar />
  {:else if route.startsWith('/consultar')}
    <Consultar query={route} />
  {:else}
    <Home />
  {/if}
</div>
