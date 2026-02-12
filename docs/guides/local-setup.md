# Local setup

Run API and frontend locally. Use either Supabase (Postgres in the cloud) or Docker for databases.

## Option A: Supabase + Docker (Redis/Mongo only)

1. Create a Supabase project and get the **Session pooler** connection string.
2. In repo root `.env`: set `DATABASE_URL` to that string and set `JWT_SECRET`.
3. Start Redis and MongoDB only:
   ```bash
   docker compose -f infrastructure/docker/docker-compose.yml up -d redis mongodb
   ```
4. Run the API and frontend (see below).

## Option B: Fully local (Postgres + Redis + MongoDB in Docker)

1. Start all services:
   ```bash
   docker compose -f infrastructure/docker/docker-compose.yml up -d
   ```
2. In repo root `.env`:
   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5434/prism_catalyst
   JWT_SECRET=your-secret
   ```
   (Port 5434 avoids conflict with local Postgres on 5432/5433.)
3. Create the `users` table (run the SQL from [database-schemas.md](../architecture/database-schemas.md) in a SQL client, or use the API after applying migrations).
4. Run the API and frontend (see below).

**Data pipeline (Phase 2):** In repo root `.env`, set `ALPHA_VANTAGE_API_KEY` for market data. See [data-pipeline.md](data-pipeline.md).

Optional env for later phases (when using Docker; ports chosen to avoid conflict with local installs):
- `REDIS_URL=redis://localhost:6380`
- `MONGODB_URI=mongodb://localhost:27018/prism`

## Run API and frontend

From repo root:

**Terminal 1 – API**
```bash
cd backend/api-service
npm ci
npm run dev
```
API: http://localhost:3000

**Terminal 2 – Frontend**
```bash
cd frontend
npm ci
npm run dev
```
App: http://localhost:5173 (proxies `/api` to the API).

## Verify

- `GET http://localhost:3000/api/v1/health` → `{ "data": { "status": "ok", "db": "connected" } }` when `DATABASE_URL` is set and reachable.
- Open http://localhost:5173, sign up, then sign in.
