import { useEffect, useState } from "react";
import { obtenerVacante } from "./api";

export default function DetalleVacante({ id, onCerrar }) {
  const [vacante, setVacante] = useState(null);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    setCargando(true);
    obtenerVacante(id)
      .then(setVacante)
      .catch(() => setVacante(null))
      .finally(() => setCargando(false));
  }, [id]);

  useEffect(() => {
    function alPresionar(e) {
      if (e.key === "Escape") onCerrar();
    }
    window.addEventListener("keydown", alPresionar);
    return () => window.removeEventListener("keydown", alPresionar);
  }, [onCerrar]);

  return (
    <div className="fondo" onClick={onCerrar}>
      <div className="panel" onClick={(e) => e.stopPropagation()}>
        <button className="cerrar" onClick={onCerrar}>×</button>

        {cargando && <p className="aviso">Cargando...</p>}

        {!cargando && !vacante && <p className="aviso error">No se pudo cargar</p>}

        {vacante && (
          <>
            <h2>{vacante.titulo}</h2>
            <p className="empresa">{vacante.empresa}</p>
            <p className="meta">
              {vacante.ubicacion}
              {vacante.tipo && ` · ${vacante.tipo}`}
              {vacante.categoria && ` · ${vacante.categoria}`}
              {` · via ${vacante.fuente}`}
            </p>

            <a className="postular" href={vacante.url} target="_blank" rel="noreferrer">
              Postular en el sitio original
            </a>

            <div className="descripcion">
              {(vacante.descripcion || "Sin descripcion disponible.")
                .split("\n")
                .filter((p) => p.trim())
                .map((p, i) => (
                  <p key={i}>{p}</p>
                ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}