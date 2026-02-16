import path from 'node:path';
import { config } from 'dotenv';

const rootEnv = path.resolve(process.cwd(), '../../.env');
config({ path: rootEnv });
config();

export const env = {
  nodeEnv: process.env.NODE_ENV ?? 'development',
  port: Number(process.env.API_PORT) || 3000,
  jwtSecret: process.env.JWT_SECRET ?? '',
  databaseUrl: process.env.DATABASE_URL ?? '',
  redisUrl: process.env.REDIS_URL ?? '',
};
