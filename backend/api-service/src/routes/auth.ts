import { Router, Request, Response } from 'express';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { getPool, hasDb } from '../db.js';
import { env } from '../config.js';
import { logger } from '../logger.js';

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const MIN_PASSWORD_LENGTH = 8;

export const authRouter = Router();

authRouter.post('/auth/register', async (req: Request, res: Response): Promise<void> => {
  if (!hasDb()) {
    res.status(503).json({ error: 'Service unavailable' });
    return;
  }
  const { email, password, display_name: displayName } = req.body ?? {};
  if (!email || typeof email !== 'string' || !password || typeof password !== 'string') {
    res.status(400).json({ error: 'email and password required' });
    return;
  }
  const emailNorm = String(email).trim().toLowerCase();
  if (!emailRegex.test(emailNorm)) {
    res.status(400).json({ error: 'Invalid email' });
    return;
  }
  if (password.length < MIN_PASSWORD_LENGTH) {
    res.status(400).json({ error: `Password must be at least ${MIN_PASSWORD_LENGTH} characters` });
    return;
  }
  const passwordHash = await bcrypt.hash(password, 10);
  const pool = getPool();
  try {
    const r = await pool.query(
      `INSERT INTO users (email, password_hash, display_name) VALUES ($1, $2, $3)
       RETURNING id, email, display_name, created_at`,
      [emailNorm, passwordHash, displayName ? String(displayName).trim().slice(0, 100) : null]
    );
    const row = r.rows[0];
    const token = env.jwtSecret ? jwt.sign(
      { sub: row.id, email: row.email },
      env.jwtSecret,
      { expiresIn: '7d' }
    ) : null;
    res.status(201).json({
      data: {
        user: { id: row.id, email: row.email, display_name: row.display_name, created_at: row.created_at },
        token: token ?? undefined,
      },
    });
  } catch (e: unknown) {
    const msg = e && typeof e === 'object' && 'code' in e && (e as { code: string }).code === '23505'
      ? 'Email already registered'
      : 'Registration failed';
    logger.error('Register failed', { email: emailNorm, error: String(e) });
    res.status(400).json({ error: msg });
  }
});

authRouter.post('/auth/login', async (req: Request, res: Response): Promise<void> => {
  if (!hasDb()) {
    res.status(503).json({ error: 'Service unavailable' });
    return;
  }
  const { email, password } = req.body ?? {};
  if (!email || typeof email !== 'string' || !password || typeof password !== 'string') {
    res.status(400).json({ error: 'email and password required' });
    return;
  }
  const emailNorm = String(email).trim().toLowerCase();
  const pool = getPool();
  const r = await pool.query(
    'SELECT id, email, password_hash, display_name FROM users WHERE email = $1',
    [emailNorm]
  );
  const row = r.rows[0];
  if (!row || !(await bcrypt.compare(password, row.password_hash))) {
    res.status(401).json({ error: 'Invalid email or password' });
    return;
  }
  if (!env.jwtSecret) {
    res.status(503).json({ error: 'Auth not configured' });
    return;
  }
  const token = jwt.sign(
    { sub: row.id, email: row.email },
    env.jwtSecret,
    { expiresIn: '7d' }
  );
  res.json({
    data: {
      user: { id: row.id, email: row.email, display_name: row.display_name },
      token,
    },
  });
});
