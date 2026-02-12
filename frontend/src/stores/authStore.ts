import { create } from 'zustand';

const TOKEN_KEY = 'prism_token';

interface AuthState {
  token: string | null;
  user: { id: string; email: string; display_name?: string | null } | null;
  setAuth: (token: string, user: AuthState['user']) => void;
  clearAuth: () => void;
  hydrate: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  user: null,
  setAuth: (token, user) => {
    try {
      localStorage.setItem(TOKEN_KEY, token);
    } catch { /* localStorage unavailable */ }
    set({ token, user });
  },
  clearAuth: () => {
    try {
      localStorage.removeItem(TOKEN_KEY);
    } catch { /* localStorage unavailable */ }
    set({ token: null, user: null });
  },
  hydrate: () => {
    try {
      const t = localStorage.getItem(TOKEN_KEY);
      if (t) set((s) => ({ ...s, token: t }));
    } catch { /* localStorage unavailable */ }
  },
}));
