import { useEffect, useState } from 'react';
import { api } from '@/services/api';
import { useAuthStore } from '@/stores/authStore';

export function Dashboard() {
  const [health, setHealth] = useState<{ status?: string; db?: string } | null>(null);
  const [healthError, setHealthError] = useState<string | null>(null);
  const { user, setAuth, clearAuth, hydrate } = useAuthStore();

  useEffect(() => {
    hydrate();
  }, [hydrate]);

  useEffect(() => {
    api.getHealth().then((h) => setHealth(h ?? null)).catch((e) => setHealthError(String(e)));
  }, []);

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [authError, setAuthError] = useState<string | null>(null);
  const [isSignUp, setIsSignUp] = useState(false);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setAuthError(null);
    api
      .login(email, password)
      .then((data) => {
        if (data?.token && data?.user) setAuth(data.token, data.user);
      })
      .catch((err) => setAuthError(err.message));
  };

  const handleSignUp = (e: React.FormEvent) => {
    e.preventDefault();
    setAuthError(null);
    api
      .register(email, password)
      .then((data) => {
        if (data?.token && data?.user) setAuth(data.token, data.user);
      })
      .catch((err) => setAuthError(err.message));
  };

  return (
    <main style={{ padding: '2rem', maxWidth: 800, margin: '0 auto' }}>
      <h1>Prism Catalyst</h1>
      <p>Dashboard</p>
      <section>
        <h2>API health</h2>
        {healthError && <p style={{ color: 'crimson' }}>{healthError}</p>}
        {health && (
          <p>
            Status: {health.status}, DB: {health.db}
          </p>
        )}
      </section>
      <section>
        <h2>Auth</h2>
        {user ? (
          <p>
            {user.email} <button type="button" onClick={clearAuth}>Sign out</button>
          </p>
        ) : (
          <>
            <form onSubmit={isSignUp ? handleSignUp : handleLogin}>
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button type="submit">{isSignUp ? 'Sign up' : 'Sign in'}</button>
            </form>
            <button type="button" onClick={() => { setIsSignUp((v) => !v); setAuthError(null); }}>
              {isSignUp ? 'Already have an account? Sign in' : 'No account? Sign up'}
            </button>
            {authError && <p style={{ color: 'crimson' }}>{authError}</p>}
          </>
        )}
      </section>
    </main>
  );
}
