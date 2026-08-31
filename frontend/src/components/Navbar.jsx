import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useAccessibility } from '../context/AccessibilityContext';
import { 
  ShieldCheck, 
  Volume2, 
  VolumeX, 
  Eye, 
  Type, 
  UserCheck, 
  LogOut, 
  Sparkles,
  Scale
} from 'lucide-react';

export const Navbar = ({ onNavigate, currentTab }) => {
  const { user, logout, switchDemoRole } = useAuth();
  const { 
    seniorMode, 
    setSeniorMode, 
    highContrast, 
    setHighContrast, 
    audioGuidance, 
    setAudioGuidance,
    speakText 
  } = useAccessibility();

  const handleSeniorToggle = () => {
    const next = !seniorMode;
    setSeniorMode(next);
    speakText(next ? "Senior friendly large font mode activated." : "Standard font mode activated.");
  };

  const handleContrastToggle = () => {
    const next = !highContrast;
    setHighContrast(next);
    speakText(next ? "High contrast visual mode activated." : "Standard contrast mode activated.");
  };

  const handleAudioToggle = () => {
    const next = !audioGuidance;
    setAudioGuidance(next);
    if (next) {
      speakText("Voice guidance activated. Important inspection decisions will be spoken.");
    }
  };

  return (
    <header className="bg-[#0B192C] text-white border-b border-slate-700/60 sticky top-0 z-40 shadow-md">
      {/* Top Government Strip */}
      <div className="bg-[#07111E] px-4 py-1 border-b border-slate-800 text-[11px] flex justify-between items-center text-slate-300">
        <div className="flex items-center gap-2">
          <span className="font-semibold tracking-wide text-amber-400">सत्यमेव जयते</span>
          <span className="text-slate-400">|</span>
          <span>Ministry of Consumer Affairs, Food & Public Distribution</span>
          <span className="hidden md:inline text-slate-500">•</span>
          <span className="hidden md:inline text-slate-400">Legal Metrology Division (PCR 2011)</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-slate-400 text-[10px] hidden sm:inline">Smart India Hackathon 2026</span>
          <span className="bg-emerald-950 text-emerald-300 border border-emerald-700/60 text-[10px] px-2 py-0.5 rounded font-mono font-medium flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            SYSTEM ONLINE
          </span>
        </div>
      </div>

      {/* Main Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand & Tagline */}
        <div 
          onClick={() => onNavigate('landing')}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-lg bg-gradient-to-tr from-blue-700 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-900/40 border border-blue-400/30 group-hover:scale-105 transition-transform">
            <Scale className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-bold tracking-tight text-white font-['Outfit']">PRAMAN AI</span>
              <span className="text-[10px] uppercase tracking-wider bg-blue-900/80 text-blue-200 border border-blue-500/30 px-1.5 py-0.2 rounded font-semibold">
                Audit Network
              </span>
            </div>
            <p className="text-[11px] text-slate-300 font-medium tracking-wide">
              From Package Image to Compliance Decision.
            </p>
          </div>
        </div>

        {/* Accessibility & Role Controls */}
        <div className="flex items-center gap-2 sm:gap-4">
          {/* Senior Accessibility Toolbar */}
          <div className="hidden lg:flex items-center bg-slate-800/80 rounded-lg border border-slate-700/80 p-1 gap-1 text-xs">
            <button
              onClick={handleSeniorToggle}
              title="Large text mode for elderly/easy reading"
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded transition-colors ${
                seniorMode ? 'bg-blue-600 text-white font-bold' : 'text-slate-300 hover:text-white hover:bg-slate-700'
              }`}
            >
              <Type className="w-3.5 h-3.5" />
              <span>Large Text</span>
            </button>

            <button
              onClick={handleContrastToggle}
              title="High contrast mode"
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded transition-colors ${
                highContrast ? 'bg-amber-600 text-white font-bold' : 'text-slate-300 hover:text-white hover:bg-slate-700'
              }`}
            >
              <Eye className="w-3.5 h-3.5" />
              <span>High Contrast</span>
            </button>

            <button
              onClick={handleAudioToggle}
              title="Audio Voice Guidance"
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded transition-colors ${
                audioGuidance ? 'bg-emerald-600 text-white font-bold' : 'text-slate-300 hover:text-white hover:bg-slate-700'
              }`}
            >
              {audioGuidance ? <Volume2 className="w-3.5 h-3.5" /> : <VolumeX className="w-3.5 h-3.5" />}
              <span>Voice</span>
            </button>
          </div>

          {/* Quick Demo Switcher */}
          <div className="flex items-center bg-slate-800/90 rounded-lg border border-slate-700 p-1 text-xs">
            <span className="text-slate-400 px-2 font-medium hidden sm:inline">Role:</span>
            <select
              value={user?.role || 'INSPECTOR'}
              onChange={(e) => switchDemoRole(e.target.value)}
              className="bg-slate-900 text-amber-300 font-semibold border-0 rounded px-2 py-1 focus:ring-1 focus:ring-blue-500 text-xs cursor-pointer"
            >
              <option value="INSPECTOR">Inspector (Field)</option>
              <option value="SUPERVISOR">Supervisor (Review)</option>
              <option value="ADMIN">Admin (HQ)</option>
            </select>
          </div>

          {/* User Profile Badge */}
          {user ? (
            <div className="flex items-center gap-2 pl-2 border-l border-slate-700">
              <div className="text-right hidden md:block">
                <div className="text-xs font-semibold text-white leading-tight">{user.full_name}</div>
                <div className="text-[10px] text-slate-400 font-mono">{user.badge_number || user.role}</div>
              </div>
              <button
                onClick={logout}
                title="Logout / Switch User"
                className="p-2 text-slate-400 hover:text-red-400 hover:bg-slate-800 rounded-lg transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <button
              onClick={() => onNavigate('login')}
              className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold rounded-lg shadow"
            >
              Enforcement Login
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
