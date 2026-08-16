# Job Radar

Sistema que capta vacantes de empleo de forma automatica, las almacena sin
duplicados y notifica solo las nuevas.

## Stack

- **Frontend:** React + Vite
- **Backend:** Django + Django REST Framework
- **Base de datos:** PostgreSQL 16 (Docker)
- **Automatizacion:** n8n (Docker)

## Fuentes de datos

Remotive y Arbeitnow, ambas via API publica. Cada vacante conserva su URL y
fuente original; el usuario postula siempre en el sitio de origen.

## Como levantarlo

```bash
cp .env.example .env        # completar las variables
docker compose up -d        # PostgreSQL
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

```bash
cd frontend && npm install && npm run dev
```

Los flujos de n8n estan en `n8n/` y se importan desde la interfaz.

## Estado

- [x] Captacion automatica cada 6 horas desde dos fuentes
- [x] Deduplicacion por hash de URL
- [x] Notificacion por Telegram de vacantes nuevas
- [x] Listado web con busqueda, filtros y paginacion
- [ ] Evaluacion de afinidad con IA
- [ ] Tablero de seguimiento de postulaciones
- [ ] Despliegue
