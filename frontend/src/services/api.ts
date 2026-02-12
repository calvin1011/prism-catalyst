const base = import.meta.env.VITE_API_URL ?? '';

async function request<T>(
  path: string,
  options?: RequestInit & { token?: string }
): Promise<T> {
  const { token, ...init } = options ?? {};
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(init.headers as Record<string, string>),
  };
  if (token) (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
  const res = await fetch(`${base}${path}`, { ...init, headers });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(body?.error ?? res.statusText);
  return body as T;
}

export interface HealthData {
  data?: { status?: string; db?: string };
}

export interface AuthUser {
  id: string;
  email: string;
  display_name?: string | null;
  created_at?: string;
}

export interface AuthResponse {
  data?: { user: AuthUser; token: string };
}

export const api = {
  getHealth(): Promise<HealthData['data'] | null> {
    return request<HealthData>('/api/v1/health').then((r) => r.data ?? null);
  },

  register(email: string, password: string, displayName?: string): Promise<AuthResponse['data']> {
    return request<AuthResponse>('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify({
        email,
        password,
        ...(displayName && { display_name: displayName }),
      }),
    }).then((r) => r.data ?? undefined);
  },

  login(email: string, password: string): Promise<AuthResponse['data']> {
    return request<AuthResponse>('/api/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }).then((r) => r.data ?? undefined);
  },

  getMe(token: string): Promise<AuthUser | undefined> {
    return request<{ data: AuthUser }>('/api/v1/me', { token }).then((r) => r.data);
  },
};
