import { Router } from 'express';
import { getPool, hasDb } from '../db.js';

export const healthRouter = Router();

healthRouter.get('/health', async (_req, res) => {
  if (!hasDb()) {
    res.status(503).json({ data: { status: 'degraded', db: 'not_configured' } });
    return;
  }
  try {
    const pool = getPool();
    await pool.query('SELECT 1');
    res.json({ data: { status: 'ok', db: 'connected' } });
  } catch {
    res.status(503).json({ error: 'Service unavailable', data: { db: 'disconnected' } });
  }
});
