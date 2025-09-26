'use client';

import { createContext, useContext, useEffect, useMemo, useState } from 'react';

interface AuthContextValue {
  token: string | null;
  setToken: (token: string | null) => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setTokenState] = useState<string | null>(null);

  useEffect(() => {
    const stored = typeof window !== 'undefined' ? window.localStorage.getItem('auth-token') : null;
    if (stored) {
      setTokenState(stored);
    }
  }, []);

  const setToken = (value: string | null) => {
    setTokenState(value);
    if (typeof window !== 'undefined') {
      if (value) {
        window.localStorage.setItem('auth-token', value);
      } else {
        window.localStorage.removeItem('auth-token');
      }
    }
  };

  const value = useMemo(() => ({ token, setToken }), [token]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
