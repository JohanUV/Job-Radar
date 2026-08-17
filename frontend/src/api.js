const BASE = "http://127.0.0.1:8000/api";

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