# Job Radar

Automated job-hunting system: it collects vacancies from public job APIs,
stores them without duplicates and notifies only the new ones.

Built as a portfolio project to practice a full stack end to end, from the
scheduled data pipeline to the web interface.

## Stack

| Layer | Technology | Responsibility |
| --- | --- | --- |
| Frontend | React + Vite | Search, filters and vacancy listing |
| Backend | Django + DRF | REST API, business rules, deduplication |
| Database | PostgreSQL 16 (Docker) | Persistence |
| Automation | n8n (Docker) | Scheduled collection and notifications |

## How it works

A scheduled workflow runs every 6 hours and queries each source in parallel.
Every source has its own connector that maps the provider fields into a common
schema, so adding a new source never requires changes to the backend. The
normalized batch is posted to the ingestion endpoint, which deduplicates and
stores it. Only genuinely new vacancies trigger a Telegram notification.

Deduplication is enforced at the database level through a unique SHA-256 hash
of the vacancy URL, so re-running the pipeline can never create duplicates.

## Data sources

Remotive and Arbeitnow, both through their public APIs. Every vacancy keeps its
original URL and source, and the interface links back to the original posting,
so users always apply on the source site.

## API

| Endpoint | Method | Description |
| --- | --- | --- |
| /api/vacantes/ | GET | Paginated listing, filters by q and fuente |
| /api/vacantes/ingest/ | POST | Batch ingestion, protected with X-API-Key |

## Running it locally

Copy .env.example to .env and fill in the variables, then start PostgreSQL with
docker compose up -d. In backend/, create a virtualenv, install
requirements.txt, run migrate and start the server on 0.0.0.0:8000. In
frontend/, run npm install and npm run dev. The n8n workflows live in n8n/ and
can be imported from the n8n interface.

## Roadmap

- [x] Automated collection every 6 hours from two sources
- [x] URL-hash deduplication enforced by the database
- [x] Telegram notification for new vacancies only
- [x] Web listing with search, filters and pagination
- [ ] AI relevance scoring against the user profile
- [ ] Application tracking board
- [ ] Follow-up reminders
- [ ] Deployment
