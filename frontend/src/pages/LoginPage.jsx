import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { 
  Scale, 
  Lock, 
  User, 
  ShieldCheck, 
  Sparkles, 
  ArrowRight,
  AlertCircle
} from 'lucide-react';

export const LoginPage = ({ onLoginSuccess }) => {
  const { login, switchDemoRole } = useAuth();
  const [username, setUsername] = useState('inspector');
  const [password, setPassword] = useState('Inspect@123');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(username, password);
      onLoginSuccess();
    } catch (err) {
      setError(err.message || 'Invalid username or password.');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickRole = async (role) => {
    setLoading(true);
    setError('');
    try {
      await switchDemoRole(role);
      onLoginSuccess();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto my-12 p-8 bg-white rounded-3xl border border-slate-200 shadow-xl space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-blue-700 to-indigo-600 flex items-center justify-center mx-auto shadow-lg shadow-blue-900/30 text-white">
          <Scale className="w-6 h-6" />
        </div>
        <h2 className="text-2xl font-extrabold text-slate-900 font-['Outfit']">
          PRAMAN AI
        </h2>
        <p className="text-xs text-slate-500 font-medium">
          Legal Metrology Enforcement Directorate Access Portal
        </p>
      </div>

      {error && (
        <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-700 font-medium flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
            Officer Username / ID
          </label>
          <div className="relative">
            <User className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full text-xs pl-10 pr-4 py-3 bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 font-medium"
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">
            Security Passcode
          </label>
          <div className="relative">
            <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full text-xs pl-10 pr-4 py-3 bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 font-medium"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 bg-blue-700 hover:bg-blue-800 text-white font-bold text-xs rounded-xl shadow-md transition-all flex items-center justify-center gap-2"
        >
          <ShieldCheck className="w-4 h-4" />
          <span>{loading ? 'Authenticating...' : 'Sign In to Enforcement System'}</span>
        </button>
      </form>

      {/* 1-Click Role Switcher for Hackathon Demo */}
      <div className="pt-4 border-t border-slate-200">
        <div className="text-center text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-3">
          1-Click SIH Judge Demo Access
        </div>
        <div className="grid grid-cols-3 gap-2">
          {[
            { role: 'INSPECTOR', label: 'Inspector', color: 'bg-blue-50 hover:bg-blue-100 text-blue-800' },
            { role: 'SUPERVISOR', label: 'Supervisor', color: 'bg-amber-50 hover:bg-amber-100 text-amber-800' },
            { role: 'ADMIN', label: 'Admin (HQ)', color: 'bg-purple-50 hover:bg-purple-100 text-purple-800' }
          ].map((btn) => (
            <button
              key={btn.role}
              type="button"
              onClick={() => handleQuickRole(btn.role)}
              className={`p-2 rounded-xl text-xs font-bold transition-all text-center border border-slate-200 shadow-sm ${btn.color}`}
            >
              {btn.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};
