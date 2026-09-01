const BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000/api";

export async function obtenerVacantes({ pagina = 1, q = "", fuente = "" } = {}) {
  const params = new URLSearchParams({ pagina });
  if (q) params.append("q", q);
  if (fuente) params.append("fuente", fuente);

  const res = await fetch(`${BASE}/vacantes/?${params}`);
  if (!res.ok) throw new Error(`Error ${res.status}`);
  return res.json();
}
export async function obtenerVacante(id) {
  const res = await fetch(`${BASE}/vacantes/${id}/`);
  if (!res.ok) throw new Error(`Error ${res.status}`);
  return res.json();
}

const CHAT_ID = import.meta.env.VITE_TELEGRAM_CHAT_ID;
const API_KEY = import.meta.env.VITE_API_KEY;

export async function obtenerPostulaciones() {
  const res = await fetch(`${BASE}/perfil/${CHAT_ID}/postulaciones/`);
  if (!res.ok) throw new Error(`Error ${res.status}`);
  return res.json();
}

export async function crearPostulacion(vacanteId, estado = "guardada") {
  const res = await fetch(`${BASE}/postulaciones/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-API-Key": API_KEY },
    body: JSON.stringify({ telegram_chat_id: CHAT_ID, vacante: vacanteId, estado }),
  });
  if (!res.ok) throw new Error(`Error ${res.status}`);
  return res.json();
}

export async function actualizarPostulacion(id, cambios) {
  const res = await fetch(`${BASE}/postulaciones/${id}/`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json", "X-API-Key": API_KEY },
    body: JSON.stringify(cambios),
  });
  if (!res.ok) throw new Error(`Error ${res.status}`);
  return res.json();
}

export async function eliminarPostulacion(id) {
  const res = await fetch(`${BASE}/postulaciones/${id}/`, {
    method: "DELETE",
    headers: { "X-API-Key": API_KEY },
  });
  if (!res.ok) throw new Error(`Error ${res.status}`);
}