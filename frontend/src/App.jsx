import { useEffect, useState } from "react";
import { crearPostulacion, obtenerVacantes } from "./api";
import "./App.css";
import DetalleVacante from "./DetalleVacante";
import Tablero from "./Tablero";

export default function App() {
  const [vista, setVista] = useState("vacantes");
  const [datos, setDatos] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);
  const [pagina, setPagina] = useState(1);
  const [q, setQ] = useState("");
  const [busqueda, setBusqueda] = useState("");
  const [fuente, setFuente] = useState("");
  const [seleccionada, setSeleccionada] = useState(null);
  const [guardadas, setGuardadas] = useState({});

  function guardarEnTablero(e, vacanteId) {
    e.stopPropagation();
    setGuardadas((g) => ({ ...g, [vacanteId]: "..." }));
    crearPostulacion(vacanteId)
      .then(() => setGuardadas((g) => ({ ...g, [vacanteId]: "ok" })))
      .catch(() => setGuardadas((g) => ({ ...g, [vacanteId]: "error" })));
  }

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
    <div className={vista === "tablero" ? "app ancha" : "app"}>
      <header>
        <h1>Radar de empleos</h1>
        {vista === "vacantes" && datos && (
          <p className="total">{datos.total} vacantes registradas</p>
        )}
        <nav className="vistas">
          <button
            className={vista === "vacantes" ? "activa" : ""}
            onClick={() => setVista("vacantes")}
          >
            Vacantes
          </button>
          <button
            className={vista === "tablero" ? "activa" : ""}
            onClick={() => setVista("tablero")}
          >
            Tablero
          </button>
        </nav>
      </header>

      {vista === "tablero" && <Tablero />}

      {vista === "vacantes" && (
        <>
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
        <button
          className="guardar"
          disabled={guardadas[v.id] === "ok" || guardadas[v.id] === "..."}
          onClick={(e) => guardarEnTablero(e, v.id)}
        >
          {guardadas[v.id] === "ok"
            ? "En el tablero"
            : guardadas[v.id] === "error"
            ? "Error, reintentar"
            : "Guardar en tablero"}
        </button>
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
        </>
      )}
      {seleccionada && (
  <DetalleVacante id={seleccionada} onCerrar={() => setSeleccionada(null)} />
)}
    </div>
  );
}
