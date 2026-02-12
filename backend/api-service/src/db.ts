import pg from 'pg';
import { env } from './config.js';
import { logger } from './logger.js';

let pool: pg.Pool | null = null;

export function getPool(): pg.Pool {
  if (!pool) {
    if (!env.databaseUrl) throw new Error('DATABASE_URL is required');
    pool = new pg.Pool({ connectionString: env.databaseUrl });
    pool.on('error', (err) => logger.error('Pool error', { error: String(err) }));
  }
  return pool;
}

export function hasDb(): boolean {
  return Boolean(env.databaseUrl);
}

export async function closePool(): Promise<void> {
  if (pool) {
    await pool.end();
    pool = null;
  }
}
