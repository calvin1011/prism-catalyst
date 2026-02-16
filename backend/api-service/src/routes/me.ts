import { Router, Request, Response } from 'express';
import { requireAuth, JwtPayload } from '../middleware/auth.js';
import { getPool, hasDb } from '../db.js';

const router = Router();
router.use(requireAuth);

router.get('/', async (req: Request, res: Response): Promise<void> => {
  if (!hasDb()) {
    res.status(503).json({ error: 'Service unavailable' });
    return;
  }
  const payload = (req as Request & { user: JwtPayload }).user;
  const pool = getPool();
  const r = await pool.query(
    'SELECT id, email, display_name, created_at FROM users WHERE id = $1',
    [payload.sub]
  );
  const row = r.rows[0];
  if (!row) {
    res.status(404).json({ error: 'User not found' });
    return;
  }
  res.json({
    data: {
      id: row.id,
      email: row.email,
      display_name: row.display_name,
      created_at: row.created_at,
    },
  });
});

export const meRouter = router;
