const log = (level: string, msg: string, meta?: Record<string, unknown>) => {
  const line = meta ? `${new Date().toISOString()} [${level}] ${msg} ${JSON.stringify(meta)}` : `${new Date().toISOString()} [${level}] ${msg}`;
  if (level === 'error') console.error(line);
  else console.log(line);
};

export const logger = {
  info: (msg: string, meta?: Record<string, unknown>) => log('info', msg, meta),
  warn: (msg: string, meta?: Record<string, unknown>) => log('warn', msg, meta),
  error: (msg: string, meta?: Record<string, unknown>) => log('error', msg, meta),
};
