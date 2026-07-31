import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { authApi } from '../api/authApi';
import { AUTH_TOKEN_KEY } from '../api/axiosClient';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthLoading, setIsAuthLoading] = useState(true);

  const clearSession = useCallback(() => {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    setUser(null);
  }, []);

  useEffect(() => {
    let active = true;
    const restoreSession = async () => {
      const token = localStorage.getItem(AUTH_TOKEN_KEY);
      if (!token) {
        if (active) setIsAuthLoading(false);
        return;
      }
      try {
        const currentUser = await authApi.me();
        if (active) setUser(currentUser);
      } catch {
        clearSession();
      } finally {
        if (active) setIsAuthLoading(false);
      }
    };
    restoreSession();
    const handleUnauthorized = () => {
      clearSession();
      setIsAuthLoading(false);
    };
    window.addEventListener('talofood:unauthorized', handleUnauthorized);
    return () => {
      active = false;
      window.removeEventListener('talofood:unauthorized', handleUnauthorized);
    };
  }, [clearSession]);

  const login = useCallback(async (credentials) => {
    const data = await authApi.login(credentials);
    localStorage.setItem(AUTH_TOKEN_KEY, data.access_token);
    setUser(data.user);
    return data.user;
  }, []);

  const register = useCallback((payload) => authApi.register(payload), []);

  const logout = useCallback(() => {
    clearSession();
  }, [clearSession]);

  const updateProfile = useCallback(async (payload) => {
    const updated = await authApi.updateProfile(payload);
    setUser(updated);
    return updated;
  }, []);

  const value = useMemo(() => ({
    user,
    isAuthLoading,
    isAuthenticated: Boolean(user),
    isAdmin: user?.role === 'ADMIN',
    login,
    register,
    logout,
    updateProfile,
  }), [user, isAuthLoading, login, register, logout, updateProfile]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth phải được dùng bên trong AuthProvider');
  return context;
};
