import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const OFFICIAL_USERS = [
  {
    name: 'Soutik',
    email: 'Soutik@email.com',
    password: 'Soutik1234',
    role: 'ADMIN',
    displayRole: 'HEAD ADMIN',
    roleLabel: 'Head Admin (Apex Command)',
    badge: 'LM-ADM-001',
    dept: 'Directorate of Legal Metrology, Central Headquarters & Apex Command',
    color: 'bg-purple-50 text-purple-900 border-purple-200 hover:bg-purple-100'
  },
  {
    name: 'Sayantan',
    email: 'Sayantan@email.com',
    password: 'Sayantan1234',
    role: 'SUPERVISOR',
    roleLabel: 'Review Supervisor',
    badge: 'LM-SUP-102',
    dept: 'Regional Standards & Enforcement Zone-I',
    color: 'bg-amber-50 text-amber-800 border-amber-200 hover:bg-amber-100'
  },
  {
    name: 'Jiya',
    email: 'Jiya@email.com',
    password: 'Jiya1234',
    role: 'INSPECTOR',
    roleLabel: 'Audit Inspector',
    badge: 'LM-INS-203',
    dept: 'Packaged Commodity Audit & Verification Cell',
    color: 'bg-indigo-50 text-indigo-800 border-indigo-200 hover:bg-indigo-100'
  },
  {
    name: 'Rimi',
    email: 'Rimi@email.com',
    password: 'Rimi1234',
    role: 'ADMIN',
    roleLabel: 'Central Admin (HQ)',
    badge: 'LM-ADM-004',
    dept: 'Directorate of Legal Metrology, HQ Central Command',
    color: 'bg-purple-50 text-purple-800 border-purple-200 hover:bg-purple-100'
  },
  {
    name: 'Debopriya',
    email: 'Debopriya@email.com',
    password: 'Debopriya1234',
    role: 'SUPERVISOR',
    roleLabel: 'Senior Supervisor',
    badge: 'LM-SUP-105',
    dept: 'Regional Standards & Legal Enforcement Zone-II',
    color: 'bg-emerald-50 text-emerald-800 border-emerald-200 hover:bg-emerald-100'
  },
  {
    name: 'Arkadip',
    email: 'Arkadip@email.com',
    password: 'Arkadip1234',
    role: 'INSPECTOR',
    roleLabel: 'Vigilance Inspector',
    badge: 'LM-INS-206',
    dept: 'Field Inspection & Metrological Vigilance Unit',
    color: 'bg-cyan-50 text-cyan-800 border-cyan-200 hover:bg-cyan-100'
  }
];

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem('praman_token') || '');
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('praman_user');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (_) {}
    }
    return null;
  });

  const [rememberedEmail, setRememberedEmail] = useState(() => {
    return localStorage.getItem('praman_remembered_email') || 'Soutik@email.com';
  });

  const login = async (identifier, password, rememberMe = true) => {
    const formData = new URLSearchParams();
    formData.append('username', identifier.trim());
    formData.append('password', password);

    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData.toString()
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Login failed. Please check your credentials.');
    }

    const data = await res.json();
    setToken(data.access_token);
    setUser(data.user);
    localStorage.setItem('praman_token', data.access_token);
    localStorage.setItem('praman_user', JSON.stringify(data.user));

    if (rememberMe) {
      localStorage.setItem('praman_remembered_email', identifier.trim());
      setRememberedEmail(identifier.trim());
    }

    return data.user;
  };

  const logout = () => {
    setToken('');
    setUser(null);
    localStorage.removeItem('praman_token');
    localStorage.removeItem('praman_user');
  };

  const quickLoginAs = async (userObj) => {
    return await login(userObj.email, userObj.password, true);
  };

  const switchDemoRole = async (roleName) => {
    const matchingUser = OFFICIAL_USERS.find(u => u.role === roleName) || OFFICIAL_USERS[0];
    if (matchingUser) {
      await login(matchingUser.email, matchingUser.password, true);
    }
  };

  return (
    <AuthContext.Provider value={{ 
      token, 
      user, 
      rememberedEmail,
      login, 
      logout, 
      quickLoginAs, 
      switchDemoRole,
      officialUsers: OFFICIAL_USERS 
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

