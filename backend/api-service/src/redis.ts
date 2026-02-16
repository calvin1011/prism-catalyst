import { createClient, RedisClientType } from 'redis';
import { env } from './config.js';
import { logger } from './logger.js';

const QUOTE_KEY_PREFIX = 'quote:';

let client: RedisClientType | null = null;

function quoteKey(symbol: string): string {
  return `${QUOTE_KEY_PREFIX}${symbol.toUpperCase()}`;
}

export function hasRedis(): boolean {
  return Boolean(env.redisUrl);
}

export async function getCachedQuote(symbol: string): Promise<Record<string, unknown> | null> {
  if (!env.redisUrl) return null;
  try {
    if (!client) {
      client = createClient({ url: env.redisUrl });
      client.on('error', (err) => logger.error('Redis error', { error: String(err) }));
      await client.connect();
    }
    const key = quoteKey(symbol);
    const raw = await client.get(key);
    if (!raw) return null;
    return JSON.parse(raw) as Record<string, unknown>;
  } catch (e) {
    logger.error('Redis get quote failed', { symbol, error: String(e) });
    return null;
  }
}

export async function closeRedis(): Promise<void> {
  if (client) {
    await client.quit();
    client = null;
  }
}
