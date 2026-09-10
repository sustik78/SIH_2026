import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { 
  Scale, 
  Lock, 
  Mail, 
  ShieldCheck, 
  Sparkles, 
  ArrowRight,
  AlertCircle,
  Eye,
  EyeOff,
  UserCheck,
  CheckCircle2,
  KeyRound,
  Building
} from 'lucide-react';

export const LoginPage = ({ onLoginSuccess }) => {
  const { login, quickLoginAs, rememberedEmail, officialUsers } = useAuth();
  
  const [identifier, setIdentifier] = useState(rememberedEmail || 'Soutik@email.com');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeQuickUser, setActiveQuickUser] = useState(null);

  useEffect(() => {
    if (rememberedEmail) {
      setIdentifier(rememberedEmail);
      // If remembered email corresponds to one of the 6 users, pre-fill password for rapid testing convenience
      const matched = officialUsers.find(u => u.email.toLowerCase() === rememberedEmail.toLowerCase() || u.name.toLowerCase() === rememberedEmail.toLowerCase());
      if (matched) {
        setPassword(matched.password);
      }
    }
  }, [rememberedEmail, officialUsers]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!identifier.trim()) {
      setError('Please enter your officer email or assigned username.');
      return;
    }
    if (!password) {
      setError('Please enter your account password.');
      return;
    }

    setError('');
    setLoading(true);
    try {
      await login(identifier, password, rememberMe);
      onLoginSuccess();
    } catch (err) {
      setError(err.message || 'Invalid enforcement credentials. Please verify your email/ID and password.');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectQuickUser = async (userObj) => {
    setIdentifier(userObj.email);
    setPassword(userObj.password);
    setActiveQuickUser(userObj.name);
    setError('');
    setLoading(true);
    try {
      await quickLoginAs(userObj);
      onLoginSuccess();
    } catch (err) {
      setError(err.message || 'Failed to authenticate user.');
    } finally {
      setLoading(false);
    }
  };

  const handlePopulateForm = (userObj) => {
    setIdentifier(userObj.email);
    setPassword(userObj.password);
    setActiveQuickUser(userObj.name);
    setError('');
  };

  return (
    <div className="max-w-xl mx-auto my-8 px-4 sm:px-6">
      <div className="bg-white rounded-3xl border border-slate-200/90 shadow-2xl p-6 sm:p-10 space-y-7 relative overflow-hidden">
        {/* Top Decorative Government Accent */}
        <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-blue-700 via-indigo-600 to-amber-500"></div>

        {/* Portal Header */}
        <div className="text-center space-y-2">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-[#0B192C] to-[#1E3E62] flex items-center justify-center mx-auto shadow-xl shadow-blue-950/20 text-white border border-blue-400/20">
            <Scale className="w-7 h-7 text-amber-400" />
          </div>
          
          <div>
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-blue-50 text-blue-800 border border-blue-200 text-[10px] font-bold uppercase tracking-wider mb-1">
              <span>National Enforcement Directorate</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 font-['Outfit'] tracking-tight">
              PRAMAN AI
            </h1>
            <p className="text-xs text-slate-500 font-medium max-w-sm mx-auto leading-relaxed mt-0.5">
              Packaging Regulations & Automated Metrology Audit Network
            </p>
          </div>
        </div>

        {/* Error Alert Message */}
        {error && (
          <div className="p-3.5 bg-rose-50 border border-rose-200/90 rounded-2xl text-xs text-rose-800 font-medium flex items-center gap-2.5 animate-shake">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span className="flex-1">{error}</span>
          </div>
        )}

        {/* Main Authentication Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Email / Officer ID Input */}
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5 flex items-center justify-between">
              <span>Officer Email / Username</span>
              {rememberedEmail && (
                <span className="text-[10px] font-normal text-blue-600 normal-case">
                  Remembered on this device
                </span>
              )}
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={identifier}
                onChange={(e) => setIdentifier(e.target.value)}
                placeholder="e.g., Soutik@email.com or Soutik"
                disabled={loading}
                autoComplete="email"
                required
                className="w-full text-xs pl-10 pr-4 py-3 bg-slate-50/80 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-600 focus:bg-white transition-all font-medium text-slate-900 placeholder:text-slate-400"
              />
            </div>
          </div>

          {/* Password Input with Show/Hide Toggle */}
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Security Passcode
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter authorized passcode"
                disabled={loading}
                autoComplete="current-password"
                required
                className="w-full text-xs pl-10 pr-11 py-3 bg-slate-50/80 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-600 focus:bg-white transition-all font-medium text-slate-900 placeholder:text-slate-400"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                tabIndex={-1}
                aria-label={showPassword ? 'Hide password' : 'Show password'}
                className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700 p-1"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {/* Remember Me Checkbox */}
          <div className="flex items-center justify-between pt-1">
            <label className="flex items-center gap-2 cursor-pointer text-xs text-slate-600 font-medium select-none">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500 border-slate-300 cursor-pointer"
              />
              <span>Remember officer identity on this device</span>
            </label>
            <span className="text-[11px] text-slate-400">SIH 2026 Secured</span>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className={`w-full py-3.5 px-6 rounded-xl font-bold text-xs shadow-md transition-all flex items-center justify-center gap-2 ${
              loading
                ? 'bg-slate-300 text-slate-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-700 to-indigo-700 hover:from-blue-600 hover:to-indigo-600 text-white shadow-blue-900/30 hover:scale-[1.01]'
            }`}
          >
            <ShieldCheck className="w-4 h-4" />
            <span>{loading ? 'Authenticating Officer Credentials...' : 'Sign In to Enforcement Portal'}</span>
            {!loading && <ArrowRight className="w-4 h-4" />}
          </button>
        </form>

        {/* 1-Click Authorized Demo Accounts Section */}
        <div className="pt-6 border-t border-slate-200/90 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1.5 text-[11px] font-bold text-slate-700 uppercase tracking-wider">
              <Sparkles className="w-3.5 h-3.5 text-amber-500" />
              <span>1-Click Authorized Officer Demo Access</span>
            </div>
            <span className="text-[10px] text-slate-400">SIH Evaluator Ready</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
            {officialUsers.map((u) => {
              const isSelected = activeQuickUser === u.name || identifier.toLowerCase() === u.email.toLowerCase();
              return (
                <button
                  key={u.email}
                  type="button"
                  onClick={() => handleSelectQuickUser(u)}
                  disabled={loading}
                  className={`p-2.5 rounded-xl text-left border transition-all relative ${u.color} ${
                    isSelected ? 'ring-2 ring-blue-500 shadow-sm' : 'border-slate-200 shadow-xs'
                  }`}
                >
                  <div className="flex items-center justify-between mb-0.5">
                    <span className="text-xs font-bold text-slate-900">{u.name}</span>
                    <span className="text-[9px] font-mono font-bold px-1.5 py-0.2 rounded bg-white/80 border border-slate-200">
                      {u.displayRole || u.role}
                    </span>
                  </div>
                  <div className="text-[10px] text-slate-600 truncate">{u.email}</div>
                  <div className="text-[9px] text-slate-400 font-mono mt-1 flex items-center justify-between">
                    <span>{u.badge}</span>
                    <span className="text-blue-700 font-bold">1-Click ➔</span>
                  </div>
                </button>
              );
            })}
          </div>

          <p className="text-[10px] text-slate-400 text-center leading-relaxed pt-1">
            Click any designated officer above to instantly test role-based enforcement workflows (Inspector, Supervisor, HQ Admin).
          </p>
        </div>
      </div>
    </div>
  );
};
