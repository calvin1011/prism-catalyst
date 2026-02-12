/**
 * Test Supabase/Postgres connection.
 * Run from repo root: node backend/api-service/scripts/test-db-connection.cjs
 * Or from backend/api-service: node scripts/test-db-connection.cjs
 */
const path = require('path');
const { config } = require('dotenv');

const cwd = process.cwd();
config({ path: path.join(cwd, '.env') });
config({ path: path.join(cwd, '..', '..', '.env') });

const url = process.env.DATABASE_URL;
if (!url) {
  console.error('DATABASE_URL is not set. Check your .env in the repo root.');
  process.exit(1);
}

const { Pool } = require('pg');
const pool = new Pool({ connectionString: url });

pool.query('SELECT 1 as ok')
  .then(() => {
    console.log('OK: Database connection successful.');
    return pool.end();
  })
  .then(() => process.exit(0))
  .catch((err) => {
    console.error('Connection failed:', err.message);
    process.exit(1);
  });
