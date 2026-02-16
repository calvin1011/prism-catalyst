import { Router } from 'express';
import { healthRouter } from './health.js';
import { authRouter } from './auth.js';
import { meRouter } from './me.js';
import { quotesRouter } from './quotes.js';

export const apiRouter = Router();
apiRouter.use(healthRouter);
apiRouter.use(authRouter);
apiRouter.use('/me', meRouter);
apiRouter.use(quotesRouter);