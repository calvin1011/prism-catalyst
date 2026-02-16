import { Router } from 'express';
import { getCachedQuote, hasRedis } from '../redis.js';
import { logger } from '../logger.js';

export const quotesRouter = Router();

quotesRouter.get('/quotes/:symbol', async (req, res) => {
  const symbol = (req.params.symbol ?? '').trim().toUpperCase();
  logger.info('GET /quotes/:symbol', { symbol });
  if (!symbol) {
    res.status(400).json({ error: 'Symbol is required' });
    return;
  }

  if (!hasRedis()) {
    res.status(503).json({
      error: 'Quote cache not configured',
      data: { hint: 'Set REDIS_URL and run the data-pipeline ingestion to populate cache.' },
    });
    return;
  }

  const quote = await getCachedQuote(symbol);
  if (!quote) {
    res.status(404).json({ error: 'Quote not found', data: { symbol } });
    return;
  }

  res.json({ data: quote });
});
