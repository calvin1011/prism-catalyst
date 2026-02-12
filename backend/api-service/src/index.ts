import express from 'express';
import { apiRouter } from './routes/index.js';
import { logger } from './logger.js';
import { env } from './config.js';

const app = express();
app.use(express.json());

app.use('/api/v1', apiRouter);

app.use((_req, res) => {
  res.status(404).json({ error: 'Not found' });
});

app.use((err: Error & { statusCode?: number }, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
  logger.error('Unhandled error', { error: String(err), stack: err.stack });
  const status = err.statusCode ?? 500;
  res.status(status).json({ error: err.message || 'Internal server error' });
});

const server = app.listen(env.port, () => {
  logger.info(`API listening on port ${env.port}`);
});

process.on('SIGTERM', () => {
  server.close(() => {
    import('./db.js').then(({ closePool }) => closePool()).then(() => process.exit(0));
  });
});
