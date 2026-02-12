# Database Schemas

PostgreSQL is hosted on **Supabase**. Apply via Supabase SQL Editor or your migration tool using `DATABASE_URL`. Reference `.sql` files in this folder are gitignored; copy from below or keep local scripts as needed.

## PostgreSQL

### users
| Column         | Type         | Constraints |
|----------------|--------------|-------------|
| id             | UUID         | PK, default gen_random_uuid() |
| email          | VARCHAR(255) | UNIQUE, NOT NULL |
| password_hash  | VARCHAR(255) | NOT NULL |
| display_name   | VARCHAR(100) | |
| created_at     | TIMESTAMPTZ  | NOT NULL, default now() |
| updated_at     | TIMESTAMPTZ  | NOT NULL, default now() |

Index: `users_email_key` (UNIQUE on email).

Run in Supabase SQL Editor to create `users`:

```sql
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  display_name VARCHAR(100),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### portfolios
| Column     | Type         | Constraints |
|------------|--------------|-------------|
| id         | UUID         | PK, default gen_random_uuid() |
| user_id    | UUID         | FK users(id) ON DELETE CASCADE, NOT NULL |
| name       | VARCHAR(255) | NOT NULL |
| created_at | TIMESTAMPTZ  | NOT NULL, default now() |
| updated_at | TIMESTAMPTZ  | NOT NULL, default now() |

Index: `portfolios_user_id_idx` on user_id.

### holdings
Per-portfolio positions (quantity per symbol). Used with transactions to derive current positions; Phase 3 may maintain as materialized/cached view or table.
| Column       | Type         | Constraints |
|--------------|--------------|-------------|
| id           | UUID         | PK, default gen_random_uuid() |
| portfolio_id | UUID         | FK portfolios(id) ON DELETE CASCADE, NOT NULL |
| symbol       | VARCHAR(20)  | NOT NULL |
| quantity     | DECIMAL(24,8)| NOT NULL |
| updated_at   | TIMESTAMPTZ  | NOT NULL, default now() |

Unique: (portfolio_id, symbol). Index: portfolio_id.

### transactions
Audit trail for buys/sells; used to compute or reconcile holdings.
| Column       | Type          | Constraints |
|--------------|---------------|-------------|
| id           | UUID          | PK, default gen_random_uuid() |
| portfolio_id | UUID          | FK portfolios(id) ON DELETE CASCADE, NOT NULL |
| symbol       | VARCHAR(20)   | NOT NULL |
| side         | VARCHAR(4)    | NOT NULL, CHECK (side IN ('buy','sell')) |
| quantity     | DECIMAL(24,8) | NOT NULL |
| price        | DECIMAL(24,8) | NOT NULL |
| executed_at  | TIMESTAMPTZ   | NOT NULL, default now() |
| created_at   | TIMESTAMPTZ   | NOT NULL, default now() |

Indexes: portfolio_id, (portfolio_id, executed_at) for time-range queries.

---

## MongoDB (optional, future news/sentiment)

- **Collection: `news_articles`** — source, url, title, body/snippet, published_at, symbol(s), ingestion_id.
- **Collection: `sentiment_scores`** — reference to article or symbol, model_name, score, label, computed_at.

Stored in MongoDB for flexible schema and text search; Phase 4+.
