import { useEffect, useState } from "react";
import {
  actualizarPostulacion,
  eliminarPostulacion,
  obtenerPostulaciones,
} from "./api";

const COLUMNAS = [
  ["guardada", "Guardadas"],
  ["postulada", "Postuladas"],
  ["entrevista", "Entrevista"],
  ["oferta", "Oferta"],
  ["rechazada", "Rechazadas"],
];

export default function Tablero() {
  const [postulaciones, setPostulaciones] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);
  const [sobre, setSobre] = useState(null);
  const [editando, setEditando] = useState(null);
  const [notas, setNotas] = useState("");

  useEffect(() => {
    obtenerPostulaciones()
      .then((d) => setPostulaciones(d.resultados))
      .catch((e) => setError(e.message))
      .finally(() => setCargando(false));
  }, []);

  useEffect(() => {
    function alPresionar(e) {
      if (e.key === "Escape") setEditando(null);
    }
    window.addEventListener("keydown", alPresionar);
    return () => window.removeEventListener("keydown", alPresionar);
  }, []);

  function moverA(id, estado) {
    const actual = postulaciones.find((p) => p.id === id);
    if (!actual || actual.estado === estado) return;

    const anterior = actual.estado;
    setPostulaciones((ps) =>
      ps.map((p) => (p.id === id ? { ...p, estado } : p))
    );
    setError(null);

    actualizarPostulacion(id, { estado }).catch((e) => {
      setPostulaciones((ps) =>
        ps.map((p) => (p.id === id ? { ...p, estado: anterior } : p))
      );
      setError(`No se pudo guardar el cambio: ${e.message}`);
    });
  }

  function quitar(id) {
    const previas = postulaciones;
    setPostulaciones((ps) => ps.filter((p) => p.id !== id));
    setError(null);

    eliminarPostulacion(id).catch((e) => {
      setPostulaciones(previas);
      setError(`No se pudo quitar: ${e.message}`);
    });
  }

  function abrirNotas(p) {
    setEditando(p);
    setNotas(p.notas);
  }

  function guardarNotas() {
    const id = editando.id;
    actualizarPostulacion(id, { notas })
      .then((actualizada) => {
        setPostulaciones((ps) =>
          ps.map((p) => (p.id === id ? actualizada : p))
        );
        setEditando(null);
      })
      .catch((e) => setError(`No se pudieron guardar las notas: ${e.message}`));
  }

  if (cargando) return <p className="aviso">Cargando...</p>;

  return (
    <>
      {error && <p className="aviso error">{error}</p>}

      <div className="tablero">
        {COLUMNAS.map(([estado, titulo]) => {
          const tarjetas = postulaciones.filter((p) => p.estado === estado);
          return (
            <section
              key={estado}
              className={`columna${sobre === estado ? " sobre" : ""}`}
              onDragOver={(e) => {
                e.preventDefault();
                setSobre(estado);
              }}
              onDragLeave={() => setSobre(null)}
              onDrop={(e) => {
                e.preventDefault();
                setSobre(null);
                const id = Number(e.dataTransfer.getData("text/plain"));
                if (id) moverA(id, estado);
              }}
            >
              <h3>
                {titulo} <span className="contador">{tarjetas.length}</span>
              </h3>

              {tarjetas.length === 0 && (
                <p className="columna-vacia">
                  {estado === "guardada"
                    ? "Guarda vacantes desde el listado"
                    : "Arrastra aquí una postulación"}
                </p>
              )}

              {tarjetas.map((p) => (
                <article
                  key={p.id}
                  className="tarjeta-post"
                  draggable
                  onDragStart={(e) =>
                    e.dataTransfer.setData("text/plain", String(p.id))
                  }
                >
                  <h4>{p.titulo}</h4>
                  <p className="empresa">{p.empresa}</p>
                  <p className="meta">via {p.fuente}</p>
                  <div className="acciones">
                    <a href={p.url} target="_blank" rel="noreferrer">
                      Ver oferta
                    </a>
                    <button onClick={() => abrirNotas(p)}>
                      {p.notas ? "Notas *" : "Notas"}
                    </button>
                    <button className="quitar" onClick={() => quitar(p.id)}>
                      Quitar
                    </button>
                    <select
                      className="estado"
                      value={p.estado}
                      onChange={(e) => moverA(p.id, e.target.value)}
                      aria-label="Cambiar estado"
                    >
                      {COLUMNAS.map(([valor, etiqueta]) => (
                        <option key={valor} value={valor}>
                          {etiqueta}
                        </option>
                      ))}
                    </select>
                  </div>
                </article>
              ))}
            </section>
          );
        })}
      </div>

      {editando && (
        <div className="fondo" onClick={() => setEditando(null)}>
          <div className="panel" onClick={(e) => e.stopPropagation()}>
            <button className="cerrar" onClick={() => setEditando(null)}>×</button>
            <h2>{editando.titulo}</h2>
            <p className="empresa">{editando.empresa}</p>
            <textarea
              className="notas"
              rows={8}
              placeholder="Notas de seguimiento..."
              value={notas}
              onChange={(e) => setNotas(e.target.value)}
            />
            <button className="guardar-notas" onClick={guardarNotas}>
              Guardar notas
            </button>
          </div>
        </div>
      )}
    </>
  );
}
