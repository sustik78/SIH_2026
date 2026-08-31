import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem('praman_token') || '');
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('praman_user');
    return saved ? JSON.parse(saved) : {
      id: 3,
      username: 'inspector',
      full_name: 'Shri Amit Sharma',
      role: 'INSPECTOR',
      badge_number: 'LM-INS-108',
      department: 'Field Inspection & Packaged Commodity Cell'
    };
  });

  // Auto-login demo inspector if token missing
  useEffect(() => {
    if (!token) {
      login('inspector', 'Inspect@123').catch(() => {});
    }
  }, []);

  const login = async (username, password) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData.toString()
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Login failed');
    }

    const data = await res.json();
    setToken(data.access_token);
    setUser(data.user);
    localStorage.setItem('praman_token', data.access_token);
    localStorage.setItem('praman_user', JSON.stringify(data.user));
    return data.user;
  };

  const logout = () => {
    setToken('');
    setUser(null);
    localStorage.removeItem('praman_token');
    localStorage.removeItem('praman_user');
  };

  const switchDemoRole = async (roleName) => {
    const roleCredentials = {
      INSPECTOR: { u: 'inspector', p: 'Inspect@123' },
      SUPERVISOR: { u: 'supervisor', p: 'Super@123' },
      ADMIN: { u: 'admin', p: 'Admin@123' }
    };
    const cred = roleCredentials[roleName];
    if (cred) {
      await login(cred.u, cred.p);
    }
  };

  return (
    <AuthContext.Provider value={{ token, user, login, logout, switchDemoRole }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
