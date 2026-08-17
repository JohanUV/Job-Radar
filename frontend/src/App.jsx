import { useEffect, useState } from "react";
import { obtenerVacantes } from "./api";
import "./App.css";
import DetalleVacante from "./DetalleVacante";

export default function App() {
  const [datos, setDatos] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);
  const [pagina, setPagina] = useState(1);
  const [q, setQ] = useState("");
  const [busqueda, setBusqueda] = useState("");
  const [fuente, setFuente] = useState("");
  const [seleccionada, setSeleccionada] = useState(null);

  useEffect(() => {
    setCargando(true);
    setError(null);
    obtenerVacantes({ pagina, q: busqueda, fuente })
      .then(setDatos)
      .catch((e) => setError(e.message))
      .finally(() => setCargando(false));
  }, [pagina, busqueda, fuente]);

  function buscar(e) {
    e.preventDefault();
    setPagina(1);
    setBusqueda(q);
  }

  return (
    <div className="app">
      <header>
        <h1>Radar de empleos</h1>
        {datos && <p className="total">{datos.total} vacantes registradas</p>}
      </header>

      <form className="filtros" onSubmit={buscar}>
        <input
          type="text"
          placeholder="Buscar por titulo o empresa..."
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <select value={fuente} onChange={(e) => { setFuente(e.target.value); setPagina(1); }}>
          <option value="">Todas las fuentes</option>
          <option value="remotive">Remotive</option>
          <option value="arbeitnow">Arbeitnow</option>
        </select>
        <button type="submit">Buscar</button>
      </form>

      {cargando && <p className="aviso">Cargando...</p>}
      {error && <p className="aviso error">No se pudo conectar: {error}</p>}

      {datos && !cargando && (
        <>
          <ul className="lista">
            {datos.resultados.map((v) => (
                    <li key={v.id} className="tarjeta" onClick={() => setSeleccionada(v.id)}>
        <h2>{v.titulo}</h2>
        <p className="empresa">{v.empresa}</p>
        <p className="meta">
          {v.ubicacion} · via {v.fuente}
        </p>
      </li>
            ))}
          </ul>

          <nav className="paginacion">
            <button disabled={pagina <= 1} onClick={() => setPagina(pagina - 1)}>
              Anterior
            </button>
            <span>
              Pagina {datos.pagina} de {datos.paginas}
            </span>
            <button
              disabled={pagina >= datos.paginas}
              onClick={() => setPagina(pagina + 1)}
            >
              Siguiente
            </button>
          </nav>
        </>
      )}
      {seleccionada && (
  <DetalleVacante id={seleccionada} onCerrar={() => setSeleccionada(null)} />
)}
    </div>
  );
}
